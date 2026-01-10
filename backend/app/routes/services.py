from fastapi import APIRouter, Depends, HTTPException, status # Tools to build the API
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.services.service import Service
from app.models.services.service_teck import ServiceTech
from app.models.services.service_tech_map import ServiceTechMap
from app.models.services.service_offer import ServiceOffering
from app.models.services.service_offer_map import ServiceOfferingMap
from app.schemas.Services import ServiceCreate, ServiceResponse, ServiceUpdate
from app.auth.deps import get_current_user # To check if the user is logged in

# Setup the router for all service-related links
router = APIRouter(prefix="/admin/services", tags=["Services"])

# 1. Create a new service
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
   payload: ServiceCreate,
   db: Session = Depends(get_db),
   admin = Depends(get_current_user),
):
     # Step 1: Create the main service record
    service = Service(
        title=payload.title,
        description=payload.description,
        photo_url=payload.photo_url,
        base_price=payload.base_price,
        discount_type=payload.discount_type,
        discount_value=payload.discount_value,
    )
    # Step 2: Save it temporarily to get an ID
    db.add(service)
    db.flush() # ensures service.id exists before mapping

    # Step 3: Find and check the technologies
    techs = (
        db.query(ServiceTech).filter(ServiceTech.id.in_(payload.tech_ids)).all()
    )
    if len(techs) != len(payload.tech_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more tech IDs are invalid",
        )
    
    # Step 4: Find and check the offerings
    offerings = (
        db.query(ServiceOffering).filter(ServiceOffering.id.in_(payload.offering_ids)).all()
    )
    if len(offerings) != len(payload.offering_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more offering IDs are invalid",
        )
    
    # Step 5: Link the service to the technologies and offerings
    for tech in techs:
        db.add(
            ServiceTechMap(
                service_id=service.id,
                tech_id=tech.id,
            )
        )

    for offering in offerings:
        db.add(
            ServiceOfferingMap(
                service_id=service.id,
                offering_id=offering.id,
            )
        )
    
    # Commit once to keep write atomic
    db.commit()
    db.refresh(service)

    # Explicit response to avoid leaking DB structure
    return ServiceResponse(
        id=service.id,
        title=service.title,
        description=service.description,
        photo_url=service.photo_url,
        techs=[tech.name for tech in techs],
        offerings=[offering.name for offering in offerings],
        base_price=service.base_price,
        effective_price=service.effective_price,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )

# List all services with their tech stacks and offerings
# 2. Get a list of all services
@router.get("/", response_model=list[ServiceResponse])
def list_services(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Step 1: Get all services from the database
    services = db.query(Service).all()
    responses = []

    for service in services:
        # Step 2: For each service, find its technology names
        techs = (
            db.query(ServiceTech.name)
            .join(ServiceTechMap)
            .filter(ServiceTechMap.service_id == service.id)
            .all()
        )

        # Step 3: Find all features (offerings) for this service
        offerings = (
            db.query(ServiceOffering.name)
            .join(ServiceOfferingMap)
            .filter(ServiceOfferingMap.service_id == service.id)
            .all()
        )

        # Step 4: Add the service details to the final list
        responses.append(
            ServiceResponse(
                id=service.id,
                title=service.title,
                description=service.description,
                photo_url=service.photo_url,
                techs=[t[0] for t in techs],
                offerings=[o[0] for o in offerings],
                base_price=service.base_price,
                effective_price=service.effective_price,
                created_at=service.created_at,
                updated_at=service.updated_at,
            )
        )

    return responses


# get service details by id
# 3. Get details of one specific service
@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Step 1: Find the service in the database
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    # Step 2: Find its technology names
    techs = (
        db.query(ServiceTech.name)
        .join(ServiceTechMap)
        .filter(ServiceTechMap.service_id == service.id)
        .all()
    )

    # Step 3: Find its features (offerings)
    offerings = (
        db.query(ServiceOffering.name)
        .join(ServiceOfferingMap)
        .filter(ServiceOfferingMap.service_id == service.id)
        .all()
    )

    return ServiceResponse(
        id=service.id,
        title=service.title,
        description=service.description,
        photo_url=service.photo_url,
        techs=[t[0] for t in techs],
        offerings=[o[0] for o in offerings],
        base_price=service.base_price,
        effective_price=service.effective_price,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )


# 4. Update an existing service
@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: UUID,
    payload: ServiceUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Fetch service or fail fast
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )
    # Step 1: Update simple fields (title, price, etc.)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field in ("tech_ids", "offering_ids"):
            continue
        setattr(service, field, value)

    # Step 2: Update the technology list if provided
    if payload.tech_ids is not None:
        # Clear existing tech relations
        db.query(ServiceTechMap).filter(
            ServiceTechMap.service_id == service.id
        ).delete()

        # Empty list means clear all
        if payload.tech_ids:
            techs = (
                db.query(ServiceTech)
                .filter(ServiceTech.id.in_(payload.tech_ids))
                .all()
            )

            if len(techs) != len(payload.tech_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more tech IDs are invalid",
                )

            for tech in techs:
                db.add(
                    ServiceTechMap(
                        service_id=service.id,
                        tech_id=tech.id,
                    )
                )
    # Step 3: Update the offerings list if provided
    if payload.offering_ids is not None:
        # Clear existing offering relations
        db.query(ServiceOfferingMap).filter(
            ServiceOfferingMap.service_id == service.id
        ).delete()

        if payload.offering_ids:
            offerings = (
                db.query(ServiceOffering)
                .filter(ServiceOffering.id.in_(payload.offering_ids))
                .all()
            )

            if len(offerings) != len(payload.offering_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more offering IDs are invalid",
                )

            for offering in offerings:
                db.add(
                    ServiceOfferingMap(
                        service_id=service.id,
                        offering_id=offering.id,
                    )
                )
    db.commit()
    db.refresh(service)

    techs = (
        db.query(ServiceTech.name)
        .join(ServiceTechMap)
        .filter(ServiceTechMap.service_id == service.id)
        .all()
    )

    offerings = (
        db.query(ServiceOffering.name)
        .join(ServiceOfferingMap)
        .filter(ServiceOfferingMap.service_id == service.id)
        .all()
    )

    return ServiceResponse(
        id=service.id,
        title=service.title,
        description=service.description,
        photo_url=service.photo_url,
        techs=[t[0] for t in techs],
        offerings=[o[0] for o in offerings],
        base_price=service.base_price,
        effective_price=service.effective_price,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )


# 5. Delete a service
@router.delete("/{service_id}")
def delete_service(
    service_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Step 1: Find the service in the database
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Step 2: Remove the links to technologies and features first
    db.query(ServiceTechMap).filter(
        ServiceTechMap.service_id == service_id
    ).delete()

    db.query(ServiceOfferingMap).filter(
        ServiceOfferingMap.service_id == service_id
    ).delete()

    # Step 3: Delete the service and save changes
    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully", "id": service_id}


