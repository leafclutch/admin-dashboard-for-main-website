from pydantic import BaseModel
from uuid import UUID

class ServiceTechCreate(BaseModel):
    name: str

class ServiceTechResponse(BaseModel):
    id: UUID
    name: str
