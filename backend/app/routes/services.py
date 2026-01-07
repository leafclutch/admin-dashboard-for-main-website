from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.services.service import Service
from app.models.services.service_teck import ServiceTech
from app.models.services.service_tech_map import ServiceTechMap
from app.models.services.service_offer import ServiceOffering
from app.models.services.service_offer_map import ServiceOfferingMap
from app.schemas.Services import ServiceCreate, ServiceResponse, ServiceUpdate
from app.auth.deps import get_current_user

router = APIRouter(prefix="/admin/services", tags=["Services"])

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
   payload: ServiceCreate,
   db: Session = Depends(get_db),
   admin = Depends(get_current_user),
):
     # Create core service first (source-of-truth data only)
    service = Service(
        title=payload.title,
        description=payload.description,
        photo_url=payload.photo_url,
        base_price=payload.base_price,
        discount_type=payload.discount_type,
        discount_value=payload.discount_value,
    )
    # Add to session early to generate service.id
    db.add(service)
    db.flush() # ensures service.id exists before mapping

    # Validate that all provided tech IDs exist
    techs = (
        db.query(ServiceTech).filter(ServiceTech.id.in_(payload.tech_ids)).all()
    )
    # Reject request if any tech ID is invalid
    if len(techs) != len(payload.tech_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more tech IDs are invalid",
        )
    
    # Validate that all provided offering IDs exist
    offerings = (
        db.query(ServiceOffering).filter(ServiceOffering.id.in_(payload.offering_ids)).all()
    )
    # Reject request if any offering ID is invalid
    if len(offerings) != len(payload.offering_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more offering IDs are invalid",
        )
    
    # Attach technologies via normalized join table
    for tech in techs:
        db.add(
            ServiceTechMap(
                service_id=service.id,
                tech_id=tech.id,
            )
        )

    # Attach offerings via normalized join table
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
@router.get("/", response_model=list[ServiceResponse])
def list_services(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    services = db.query(Service).all()
    responses = []

    for service in services:
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
@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: UUID,
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
        # Update only provided scalar fields
    for field, value in payload.model_dump(exclude_unset=True).items():
        # Relationships handled separately
        if field in ("tech_ids", "offering_ids"):
            continue
        setattr(service, field, value)

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


@router.delete("/{service_id}")
def delete_service(
    service_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Remove relations first (safe cleanup)
    db.query(ServiceTechMap).filter(
        ServiceTechMap.service_id == service_id
    ).delete()

    db.query(ServiceOfferingMap).filter(
        ServiceOfferingMap.service_id == service_id
    ).delete()

    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully", "id": service_id}


