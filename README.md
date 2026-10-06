# ASIA 2.0 — Studio AS

Starter de produção assistida para atendimento com Claude, Meta Webhooks, Google Calendar,
FastAPI, PostgreSQL e n8n. Credenciais reais não estão incluídas.

## Requisitos
- Ubuntu 22.04/24.04 ou WSL2 com Docker Engine + Docker Compose
- Conta Meta Developer com app configurado e permissões aprovadas
- Chave Anthropic (Claude)
- Projeto Google Cloud com Google Calendar API habilitada e credencial OAuth/service account
- Domínio HTTPS público (Cloudflare Tunnel recomendado)

## Instalação rápida
```bash
cp .env.example .env
# Edite .env e preencha os segredos
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
```
API: http://localhost:8000  
n8n: http://localhost:5678  
Webhook Meta: `https://SEU-DOMINIO/webhook/meta`

## Configuração Meta
1. Crie um app em https://developers.facebook.com/ e adicione Messenger, Instagram e WhatsApp.
2. Configure o webhook de callback como `https://SEU-DOMINIO/webhook/meta`.
3. Use `META_VERIFY_TOKEN` como token de verificação.
4. Assine os campos necessários: `messages`, `messaging_postbacks` e eventos de mensagens do Instagram conforme o produto habilitado.
5. Configure `META_APP_SECRET`, tokens de acesso e IDs em `.env`.
6. Para produção, complete a revisão de permissões e use tokens de longa duração/renovação segura.
7. WhatsApp Cloud API exige número cadastrado, WABA ID e token com permissões apropriadas.

A disponibilidade de permissões e campos depende do tipo de conta, versão da Graph API e revisão da Meta.

## Claude
Defina `ANTHROPIC_API_KEY`. O modelo fica em `CLAUDE_MODEL`. Confira o nome de modelo disponível na sua conta Anthropic antes de usar.

## Google Calendar
Defina `GOOGLE_CALENDAR_ID` e `GOOGLE_SERVICE_ACCOUNT_FILE`.
Monte o arquivo JSON da service account em `secrets/google-service-account.json` e compartilhe a agenda com o e-mail da service account com permissão para criar/editar eventos.
Se usar OAuth de usuário, adapte `app/services/calendar.py` para o fluxo OAuth; não coloque tokens no Git.

## n8n
Abra `http://localhost:5678`, conclua o primeiro acesso e configure as credenciais. O workflow exportado em `n8n/studio-as-notifications.json` é um exemplo de entrada para notificações. Importe em Workflows > Import from File e ajuste a URL da API.
O backend funciona sem n8n; a integração n8n é complementar.

## Segurança antes de produção
- Troque todas as senhas e tokens de exemplo.
- Nunca publique `.env`, `secrets/` ou tokens no Git.
- Ative HTTPS e configure `PUBLIC_BASE_URL`.
- Configure política de privacidade, consentimento e retenção LGPD.
- Use Meta App Secret e valide assinatura X-Hub-Signature-256.
- Restrinja CORS, acesso ao n8n e ao PostgreSQL.
- Configure backup do banco e monitoramento.
- Faça testes com usuários de teste antes de habilitar mensagens reais.

## Endpoints
- `GET /health`
- `GET /webhook/meta` — verificação do webhook
- `POST /webhook/meta` — eventos Meta
- `GET /api/services`
- `POST /api/appointments/check`
- `POST /api/appointments`
- `POST /api/chat`

## Fluxo de agendamento
1. Cliente informa serviço, data e horário desejados.
2. ASIA identifica duração do serviço e consulta o Google Calendar.
3. Backend verifica conflito.
4. Cliente confirma os dados.
5. Backend verifica novamente e cria o evento.
6. Registro é persistido no PostgreSQL.
7. ASIA envia confirmação somente após sucesso da criação.

Este repositório é uma base funcional inicial. Antes de atender clientes reais, valide permissões Meta, credenciais Google, política de cancelamento, duração e buffers de cada serviço.
