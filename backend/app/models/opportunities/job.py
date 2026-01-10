
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class JobDetail(Base):
    __tablename__ = "job_details"

    opportunity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True
    )

    employment_type = Column(String)  # Full-time, Part-time
    salary_range = Column(String)
