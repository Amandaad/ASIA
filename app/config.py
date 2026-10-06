from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "ASIA Studio AS"
    environment: str = "development"
    public_base_url: str = ""
    database_url: str
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"
    claude_max_tokens: int = 700
    meta_verify_token: str = ""
    meta_app_secret: str = ""
    meta_access_token: str = ""
    meta_page_id: str = ""
    meta_instagram_id: str = ""
    meta_phone_number_id: str = ""
    meta_graph_api_version: str = "v23.0"
    google_calendar_id: str = ""
    google_service_account_file: str = "/run/secrets/google-service-account.json"
    n8n_webhook_url: str = ""
    timezone: str = "America/Fortaleza"
    human_handoff_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
