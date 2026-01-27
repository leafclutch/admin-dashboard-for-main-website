import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship  # needed for ORM navigation
from app.db.base import Base
from app.models.pricing.enums import DiscountType

class Training(Base):
    """
    Represents a training program.
    This table stores ONLY the core data.
    Calculated and list-like data are handled elsewhere.
    """

    __tablename__ = "trainings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # UUID is used instead of integer for better security and scalability

    photo_url = Column(String)
    # Image URL for training thumbnail

    title = Column(String, nullable=False)
    # Title is required because training without name makes no sense

    description = Column(String)
    # Long text description of the training

    base_price = Column(Numeric(10, 2), nullable=False)
    # Base price is the source of truth for pricing

    enroll_from_price = Column(Numeric(10, 2), nullable=True)
    # Price for enrollment

    discount_type = Column(Enum(DiscountType), nullable=True)
    # Discount type is optional because not all trainings have discounts

    discount_value = Column(Numeric(10, 2), nullable=True)
    # Discount value depends on discount_type

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Stored for audit and sorting

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ---------------- ORM RELATIONSHIPS ----------------
    # allows: training.benefits
    benefits = relationship(
        "TrainingBenefit",
        back_populates="training",
        cascade="all, delete-orphan",
    )

    # allows: training.training_mentors -> mentor
    training_mentors = relationship(
        "TrainingMentor",
        back_populates="training",
        cascade="all, delete-orphan",
    )

    @property
    def effective_price(self):
        """
        This follows the pricing rule from the docs:
        effective_price = base_price − discount
        """
        if not self.discount_type or not self.discount_value:
            return self.base_price

        if self.discount_type == DiscountType.PERCENTAGE:
            return self.base_price * (1 - self.discount_value / 100)

        return self.base_price - self.discount_value

