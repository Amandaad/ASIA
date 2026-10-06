import hashlib, hmac, json
from datetime import timedelta
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.db import Base, engine, get_db
from app.models import Conversation, Appointment
from app.schemas import ChatRequest, CheckRequest, AppointmentRequest
from app.services.claude import reply
from app.services.catalog import SERVICES, find_service
from app.services.calendar import check_slot, create_event
from app.services.meta import send_text

app = FastAPI(title="ASIA 2.0 — Studio AS", version="2.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status":"ok","service":"ASIA 2.0"}

@app.get("/api/services")
def services():
    return {"services": SERVICES}

@app.post("/api/chat")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    answer = reply(payload.message)
    db.add(Conversation(channel=payload.channel, external_id=payload.customer_id,
                        message=payload.message, response=answer))
    db.commit()
    return {"reply": answer}

@app.post("/api/appointments/check")
def appointment_check(payload: CheckRequest):
    service = find_service(payload.service_name)
    if not service:
        raise HTTPException(404, "Serviço não encontrado no catálogo")
    try:
        available = check_slot(payload.start_at, service["duration_minutes"])
    except Exception as exc:
        raise HTTPException(503, f"Não foi possível consultar a agenda: {exc}")
    return {"available":available, "service":service, "start_at":payload.start_at}

@app.post("/api/appointments")
def appointment_create(payload: AppointmentRequest, db: Session = Depends(get_db)):
    service = find_service(payload.service_name)
    if not service:
        raise HTTPException(404, "Serviço não encontrado")
    try:
        # Reconsulta imediatamente antes de criar para reduzir risco de conflito.
        if not check_slot(payload.start_at, service["duration_minutes"]):
            raise HTTPException(409, "Esse horário não está mais disponível")
        event = create_event(
            f"{service['name']} — {payload.customer_name}",
            payload.start_at, service["duration_minutes"],
            f"Contato: {payload.customer_contact}\nObservações: {payload.notes or ''}"
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, f"Falha ao criar evento no Google Agenda: {exc}")
    row = Appointment(service_name=service["name"], start_at=payload.start_at,
        end_at=payload.start_at + timedelta(minutes=service["duration_minutes"]),
        google_event_id=event.get("id"), status="confirmed", notes=payload.notes)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"confirmed":True,"appointment_id":row.id,"google_event_id":event.get("id"),
            "message":"Agendamento criado e confirmado."}

def verify_meta_signature(raw: bytes, signature: str | None):
    if not settings.meta_app_secret:
        return settings.environment != "production"
    if not signature or not signature.startswith("sha256="):
        return False
    expected = hmac.new(settings.meta_app_secret.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256="+expected, signature)

@app.get("/webhook/meta")
def meta_verify(request: Request):
    q = request.query_params
    if q.get("hub.mode") == "subscribe" and q.get("hub.verify_token") == settings.meta_verify_token:
        return int(q.get("hub.challenge", ""))
    raise HTTPException(403, "Token de verificação inválido")

@app.post("/webhook/meta")
async def meta_webhook(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    if not verify_meta_signature(raw, request.headers.get("x-hub-signature-256")):
        raise HTTPException(403, "Assinatura Meta inválida")
    data = json.loads(raw or b"{}")
    # Normaliza eventos de mensagens comuns. Cada produto Meta pode ter payload próprio.
    for entry in data.get("entry", []):
        for messaging in entry.get("messaging", []):
            sender = (messaging.get("sender") or {}).get("id")
            message = messaging.get("message") or {}
            text = message.get("text")
            if sender and text and not message.get("is_echo"):
                answer = reply(text)
                db.add(Conversation(channel="instagram_or_facebook", external_id=sender,
                                    message=text, response=answer))
                db.commit()
                # Instagram/Facebook: o endpoint específico depende do objeto do webhook.
                channel = "instagram" if data.get("object") == "instagram" else "facebook"
                await send_text(channel, sender, answer)
        # WhatsApp Cloud API usa entry.changes.value.messages, não entry.messaging.
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                sender = msg.get("from")
                body = (msg.get("text") or {}).get("body")
                if sender and body:
                    answer = reply(body)
                    db.add(Conversation(channel="whatsapp", external_id=sender,
                                        message=body, response=answer))
                    db.commit()
                    await send_text("whatsapp", sender, answer)
    return {"received":True}
