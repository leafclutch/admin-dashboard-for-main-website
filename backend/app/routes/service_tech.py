from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.deps import get_current_user
from app.models.services.service_teck import ServiceTech
from app.schemas.service_tech import (
    ServiceTechCreate,
    ServiceTechResponse,
)

router = APIRouter(
    prefix="/admin/service-techs",
    tags=["Service Techs"],
)

@router.post(
    "",
    response_model=ServiceTechResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_tech(
    payload: ServiceTechCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Prevent duplicate tech names (master data must be unique)
    existing = (
        db.query(ServiceTech)
        .filter(ServiceTech.name == payload.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Service tech already exists",
        )

    tech = ServiceTech(name=payload.name)

    db.add(tech)
    db.commit()
    db.refresh(tech)

    return tech

@router.get("", response_model=list[ServiceTechResponse])
def list_service_techs(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Simple list for admin selection
    return db.query(ServiceTech).all()
