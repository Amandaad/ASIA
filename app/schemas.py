from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    channel: str = "web"
    customer_id: str = "demo"
    customer_name: str | None = None

class CheckRequest(BaseModel):
    service_name: str
    start_at: datetime

class AppointmentRequest(CheckRequest):
    customer_name: str
    customer_contact: str
    notes: str | None = None
