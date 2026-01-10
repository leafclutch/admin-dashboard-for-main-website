from fastapi import APIRouter, Depends, HTTPException, status # Tools to build the API
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.deps import get_current_user # To check if the user is logged in
from app.models.services.service_teck import ServiceTech
from app.schemas.service_tech import (
    ServiceTechCreate,
    ServiceTechResponse,
)

# Setup the router for technologies (tech stack)
router = APIRouter(
    prefix="/admin/service-techs",
    tags=["Service Techs"],
)

# 1. Create a new technology name
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
    # Step 1: Check if this technology name already exists
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

    # Step 2: Create the new technology record
    tech = ServiceTech(name=payload.name)

    # Step 3: Save to database
    db.add(tech)
    db.commit()
    db.refresh(tech)

    return tech

# 2. Get a list of all technologies
@router.get("", response_model=list[ServiceTechResponse])
def list_service_techs(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Simple list for admin selection
    return db.query(ServiceTech).all()
