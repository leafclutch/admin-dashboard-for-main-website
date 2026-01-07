from pydantic import BaseModel
from uuid import UUID

class ServiceOfferingCreate(BaseModel):
    name: str

class ServiceOfferingResponse(BaseModel):
    id: UUID
    name: str
