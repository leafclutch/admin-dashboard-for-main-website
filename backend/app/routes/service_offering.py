from fastapi import APIRouter, Depends, HTTPException, status # Tools to build the API
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.deps import get_current_user # To check if the user is logged in
from app.models.services.service_offer import ServiceOffering
from app.schemas.service_offering import (
    ServiceOfferingCreate,
    ServiceOfferingResponse,
)

# Setup the router for service features (offerings)
router = APIRouter(
    prefix="/admin/service-offerings",
    tags=["Service Offerings"],
)


# 1. Create a new service feature
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
    # Step 1: Check if this name already exists to avoid duplicates
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

    # Step 2: Create the new offering record
    offering = ServiceOffering(name=payload.name)

    # Step 3: Save to database
    db.add(offering)
    db.commit()
    db.refresh(offering)

    return offering

# 2. Get a list of all service features
@router.get("", response_model=list[ServiceOfferingResponse])
def list_service_offerings(
    db: Session = Depends(get_db),
    
):
    # Step 1: Get all service features from the database
    return db.query(ServiceOffering).all()
