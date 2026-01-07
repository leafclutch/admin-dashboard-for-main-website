import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

class Project(Base):
    """
    Represents a project displayed on the platform.
    """

    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Unique project ID

    photo_url = Column(String)
    # Main project image

    title = Column(String, nullable=False)
    # Project title

    description = Column(String)
    # Project details

    project_link = Column(String)
    # External link (GitHub, live demo, etc.)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
