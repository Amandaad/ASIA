from anthropic import Anthropic
from app.config import settings
from app.services.catalog import SERVICES

SYSTEM = '''Você é ASIA, atendente virtual do Studio AS. Fale em português brasileiro,
com carinho, clareza e profissionalismo. Nunca invente preços, disponibilidade ou políticas.
Use somente o catálogo fornecido. Para agendar, colete serviço, nome, contato, data e horário.
Não diga que está agendado: informe que vai consultar a agenda. Só confirme após retorno
positivo do sistema. Se a cliente pedir pessoa humana, demonstrar insatisfação ou houver dúvida
fora do escopo, encaminhe para atendente. Não solicite dados de cartão ou senhas.'''

def reply(message: str) -> str:
    if not settings.anthropic_api_key:
        return "Olá, maravilhosa! Sou a ASIA do Studio AS. Nosso atendimento inteligente está em configuração. Posso ajudar com serviços ou encaminhar você para nossa equipe."
    client = Anthropic(api_key=settings.anthropic_api_key)
    result = client.messages.create(
        model=settings.claude_model,
        max_tokens=settings.claude_max_tokens,
        system=SYSTEM + "\nCATÁLOGO: " + str(SERVICES),
        messages=[{"role":"user","content":message}]
    )
    return "".join(block.text for block in result.content if getattr(block, "type", "") == "text")
