import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base
from app.models.pricing.enums import DiscountType
from decimal import Decimal

class Service(Base):
    """
    Represents a service offered by the company.
    Similar to Training, but without mentors or benefits.
    """

    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # UUID used for security and scalability

    photo_url = Column(String)
    # Service image

    title = Column(String, nullable=False)
    # Required: service must have a name

    description = Column(String)
    # Detailed explanation of service

    base_price = Column(Numeric(10, 2), nullable=False)
    # Main pricing value

    discount_type = Column(Enum(DiscountType), nullable=True)
    # Optional discount

    discount_value = Column(Numeric(10, 2), nullable=True)
    # Discount amount or percentage

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    @property
    def effective_price(self):
        """
        Calculated dynamically to avoid inconsistent data.
        """
        if not self.discount_type or not self.discount_value:
            return self.base_price

        if self.discount_type == DiscountType.PERCENTAGE:
            return self.base_price * (
            Decimal("1") - self.discount_value / Decimal("100")
        )

        return max(Decimal("0"), self.base_price - self.discount_value)
