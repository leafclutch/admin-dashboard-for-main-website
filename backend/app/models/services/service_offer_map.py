import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class ServiceOfferingMap(Base):
    __tablename__ = "service_offering_map"

    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), primary_key=True)
    offering_id = Column(UUID(as_uuid=True), ForeignKey("service_offerings.id"), primary_key=True)
