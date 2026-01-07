import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from .enums import OpportunityType

class Opportunity(Base):
    """
    Represents both Jobs and Internships.
    Docs say both have the same structure,
    so we store them in one table with a type.
    """

    __tablename__ = "opportunities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Unique identifier

    title = Column(String, nullable=False)
    # Required

    description = Column(String)
    # Job or internship descriptionts

    location = Column(String)
    # Location or remote

    type = Column(Enum(OpportunityType), nullable=False)
    # JOB or INTERNSHIP

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
