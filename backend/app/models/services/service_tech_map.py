import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class ServiceTechMap(Base):
    __tablename__ = "service_tech_map"

    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), primary_key=True)
    tech_id = Column(UUID(as_uuid=True), ForeignKey("service_techs.id"), primary_key=True)
