from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
from uuid import UUID



class MemberRole(str, Enum):
    TEAM = "TEAM"
    INTERN = "INTERN"

class SocialMedia(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None
    twitter: Optional[str] = None



class MemberCreate(BaseModel):
    photo_url: Optional[str] = None
    name: str
    position: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    social_media: Optional[SocialMedia] = None
    contact_email: Optional[str] = None
    personal_email: Optional[str] = None
    contact_number: Optional[str] = None

    is_visible: bool = True
    role: MemberRole
 
   

class MemberUpdate(BaseModel):
    photo_url: Optional[str] = None
    name: Optional[str] = None
    position: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    social_media: Optional[SocialMedia] = None
    contact_email: Optional[str] = None
    personal_email: Optional[str] = None
    contact_number: Optional[str] = None

    is_visible: Optional[bool] = None
    role: Optional[MemberRole] = None
   


class MemberResponse(BaseModel):
    id: UUID
    photo_url: Optional[str]
    name: str
    position: Optional[str]

    start_date: Optional[date]
    end_date: Optional[date]

    social_media: Optional[dict]
    contact_email: Optional[str]
    personal_email: Optional[str]
    contact_number: Optional[str]

    is_visible: bool
    role: MemberRole
    created_at: datetime
    updated_at: Optional[datetime]   
