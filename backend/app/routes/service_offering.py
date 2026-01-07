from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.deps import get_current_user
from app.models.services.service_offer import ServiceOffering
from app.schemas.service_offering import (
    ServiceOfferingCreate,
    ServiceOfferingResponse,
)

router = APIRouter(
    prefix="/admin/service-offerings",
    tags=["Service Offerings"],
)


@router.post(
    "",
    response_model=ServiceOfferingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_offering(
    payload: ServiceOfferingCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Avoid duplicate offerings to keep master data clean
    existing = (
        db.query(ServiceOffering)
        .filter(ServiceOffering.name == payload.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Service offering already exists",
        )

    offering = ServiceOffering(name=payload.name)

    db.add(offering)
    db.commit()
    db.refresh(offering)

    return offering

@router.get("", response_model=list[ServiceOfferingResponse])
def list_service_offerings(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Used by admin UI when creating services
    return db.query(ServiceOffering).all()
