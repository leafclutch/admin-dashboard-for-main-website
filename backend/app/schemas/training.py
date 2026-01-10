from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from uuid import UUID


class DiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    AMOUNT = "AMOUNT"


class MentorInput(BaseModel):
    name: str
    photo_url: Optional[str]


class TrainingCreate(BaseModel):
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    base_price: float
    discount_type: Optional[DiscountType]
    discount_value: Optional[float]

    benefits: List[str]
    mentor_ids: List[UUID] = Field(default_factory=list)


class TrainingUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    photo_url: Optional[str]

    base_price: Optional[float]
    discount_type: Optional[DiscountType]
    discount_value: Optional[float]

    benefits: Optional[List[str]]
    mentor_ids: Optional[List[UUID]]


class MentorResponse(BaseModel):
    name: str
    photo_url: Optional[str]


class TrainingResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    photo_url: Optional[str]

    base_price: float
    effective_price: float

    benefits: List[str]
    mentors: List[MentorResponse]
    created_at: datetime
    updated_at: Optional[datetime]
