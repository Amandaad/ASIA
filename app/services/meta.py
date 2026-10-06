import httpx
from app.config import settings

async def send_text(channel: str, recipient_id: str, message: str):
    token = settings.meta_access_token
    version = settings.meta_graph_api_version
    if not token:
        return {"skipped": True, "reason": "META_ACCESS_TOKEN não configurado"}
    if channel == "whatsapp":
        url = f"https://graph.facebook.com/{version}/{settings.meta_phone_number_id}/messages"
        payload = {"messaging_product":"whatsapp","to":recipient_id,"type":"text","text":{"body":message}}
    elif channel == "instagram":
        url = f"https://graph.facebook.com/{version}/{settings.meta_instagram_id}/messages"
        payload = {"recipient":{"id":recipient_id},"message":{"text":message}}
    else:
        url = f"https://graph.facebook.com/{version}/{settings.meta_page_id}/messages"
        payload = {"recipient":{"id":recipient_id},"message":{"text":message}}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(url, params={"access_token":token}, json=payload)
        response.raise_for_status()
        return response.json()
