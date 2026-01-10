import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class DiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    AMOUNT = "AMOUNT"


class ServiceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_ids: List[UUID]
    offering_ids: List[UUID]

    base_price: Decimal
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = None


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None

    tech_ids: Optional[List[UUID]] = None
    offering_ids: Optional[List[UUID]] = None

    base_price: Optional[Decimal] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = None


class ServiceResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    techs: List[str]
    offerings: List[str]

    base_price: Decimal
    effective_price: Decimal
    created_at: datetime
    updated_at: Optional[datetime]    
