
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class ProjectTechMap(Base):
    """
    Join table between projects and service techs.
    """

    __tablename__ = "project_tech_map"

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )

    tech_id = Column(
        UUID(as_uuid=True),
        ForeignKey("service_techs.id"),
        primary_key=True,
    )
