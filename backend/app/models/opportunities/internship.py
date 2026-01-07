
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class InternshipDetail(Base):
    __tablename__ = "internship_details"

    opportunity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        primary_key=True
    )

    duration_months = Column(Integer)
    stipend = Column(String)
