import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.member.member import Member
from app.schemas.members import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
    MemberRole,
)
from app.auth.deps import get_current_user

router = APIRouter(prefix="/admin/members", tags=["Members"])


@router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Create member as a single source-of-truth entity
    member = Member(
        photo_url=payload.photo_url,
        name=payload.name,
        position=payload.position,
        start_date=payload.start_date,
        end_date=payload.end_date,
        social_media=payload.social_media.model_dump()
        if payload.social_media else None,
        contact_email=payload.contact_email,
        personal_email=payload.personal_email,
        contact_number=payload.contact_number,
        is_visible=payload.is_visible,
        role=payload.role,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

@router.get("", response_model=list[MemberResponse])
def list_members(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Admin view: show all members regardless of visibility
    return db.query(Member).all()

@router.get("/teams", response_model=list[MemberResponse])
def list_team_members(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    return (
        db.query(Member)
        .filter(
            Member.role == MemberRole.TEAM,
            Member.is_visible == True,
        )
        .all()
    )

@router.get("/interns", response_model=list[MemberResponse])
def list_intern_members(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    return (
        db.query(Member)
        .filter(
            Member.role == MemberRole.INTERN,
            Member.is_visible == True,
        )
        .all()
    )

@router.patch("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: UUID,
    payload: MemberUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    member = (
        db.query(Member)
        .filter(Member.id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )
    for field, value in payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    ).items():
        setattr(member, field, value)
    
    member.updated_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(member)

    return member


@router.get("/team/{member_id}", response_model=MemberResponse)
def get_team_member(
    member_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.role == MemberRole.TEAM,
            Member.is_visible == True,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Team member not found",
        )

    return member

@router.get("/intern/{member_id}", response_model=MemberResponse)
def get_intern_member(
    member_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.role == MemberRole.INTERN,
            Member.is_visible == True,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Intern not found",
        )

    return member


@router.get("/{member_id}", response_model=MemberResponse)
def get_member_admin(
    member_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Admin must be able to fetch any member (visible or hidden)
    member = (
        db.query(Member)
        .filter(Member.id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member




