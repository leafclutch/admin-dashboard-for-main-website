from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.opportunities.opportunity import Opportunity
from app.models.opportunities.job import JobDetail
from app.models.opportunities.internship import InternshipDetail
from app.models.opportunities.requirement import OpportunityRequirement
from app.models.opportunities.enums import OpportunityType
from app.schemas.opportunities import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityResponse,
)
from app.auth.deps import get_current_user

router = APIRouter(
    prefix="/api/admin/opportunities",
    tags=["Admin Opportunities"],
)

def opportunity_response(
    opportunity_obj: Opportunity,
    db: Session,
) -> OpportunityResponse:
    requirements = (
        db.query(OpportunityRequirement)
        .filter_by(opportunity_id=opportunity_obj.id)
        .order_by(OpportunityRequirement.order)
        .all()
    )

    job_details = None
    internship_details = None

    if opportunity_obj.type == OpportunityType.JOB:
        job = db.query(JobDetail).filter_by(
            opportunity_id=opportunity_obj.id
        ).first()
        if job:
            job_details = {
                "employment_type": job.employment_type,
                "salary_range": job.salary_range,
            }

    if opportunity_obj.type == OpportunityType.INTERNSHIP:
        internship = db.query(InternshipDetail).filter_by(
            opportunity_id=opportunity_obj.id
        ).first()
        if internship:
            internship_details = {
                "duration_months": internship.duration_months,
                "stipend": internship.stipend,
            }

    return OpportunityResponse(
        id=str(opportunity_obj.id),
        title=opportunity_obj.title,
        description=opportunity_obj.description,
        location=opportunity_obj.location,
        type=opportunity_obj.type,
        job_details=job_details,
        internship_details=internship_details,
        requirements=[r.text for r in requirements],
    )


@router.post(
    "",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user),
):
    new_opportunity = Opportunity(
        title=payload.title,
        description=payload.description,
        location=payload.location,
        type=payload.type,
    )
    db.add(new_opportunity)
    db.flush()  # get new_opportunity.id

    if payload.type == OpportunityType.JOB:
        db.add(
            JobDetail(
                opportunity_id=new_opportunity.id,
                employment_type=payload.job_details.employment_type,
                salary_range=payload.job_details.salary_range,
            )
        )

    elif payload.type == OpportunityType.INTERNSHIP:
        db.add(
            InternshipDetail(
                opportunity_id=new_opportunity.id,
                duration_months=payload.internship_details.duration_months,
                stipend=payload.internship_details.stipend,
            )
        )

    for idx, text in enumerate(payload.requirements):
        db.add(
            OpportunityRequirement(
                opportunity_id=new_opportunity.id,
                text=text,
                order=idx,
            )
        )

    db.commit()
    db.refresh(new_opportunity)

    return opportunity_response(new_opportunity, db)


@router.get(
    "",
    response_model=list[OpportunityResponse],
)
def list_opportunities(
    type: OpportunityType | None = None,
    location: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    query = db.query(Opportunity)
    if type is not None:
        query = query.filter(Opportunity.type == type)

    if location:
        query = query.filter(
            Opportunity.location.ilike(f"%{location}%")
        )

    if search:
        query = query.filter(
            Opportunity.title.ilike(f"%{search}%")
        )

    opportunities = query.order_by(
        Opportunity.created_at.desc()
    ).all()

    return [
        opportunity_response(op, db)
        for op in opportunities
    ]


@router.get(
    "/{opportunity_id}",
    response_model=OpportunityResponse,
)
def get_opportunity(
    opportunity_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    opportunity_obj = db.get(Opportunity, opportunity_id)
    if not opportunity_obj:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return opportunity_response(opportunity_obj, db)


@router.patch(
    "/{opportunity_id}",
    response_model=OpportunityResponse,
)
def update_opportunity(
    opportunity_id: UUID,
    payload: OpportunityUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    opportunity_obj = db.get(Opportunity, opportunity_id)
    if not opportunity_obj:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    for field in ("title", "description", "location"):
        value = getattr(payload, field)
        if value is not None:
            setattr(opportunity_obj, field, value)

    if opportunity_obj.type == OpportunityType.JOB and payload.job_details:
        job = db.query(JobDetail).filter_by(
            opportunity_id=opportunity_obj.id
        ).first()
        if job:
            job.employment_type = payload.job_details.employment_type
            job.salary_range = payload.job_details.salary_range

    if opportunity_obj.type == OpportunityType.INTERNSHIP and payload.internship_details:
        internship = db.query(InternshipDetail).filter_by(
            opportunity_id=opportunity_obj.id
        ).first()
        if internship:
            internship.duration_months = payload.internship_details.duration_months
            internship.stipend = payload.internship_details.stipend

    if payload.requirements is not None:
        db.query(OpportunityRequirement).filter_by(
            opportunity_id=opportunity_obj.id
        ).delete()

        for idx, text in enumerate(payload.requirements):
            db.add(
                OpportunityRequirement(
                    opportunity_id=opportunity_obj.id,
                    text=text,
                    order=idx,
                )
            )

    db.commit()
    db.refresh(opportunity_obj)
    return opportunity_response(opportunity_obj, db)


@router.delete(
    "/{opportunity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_opportunity(
    opportunity_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    opportunity_obj = db.get(Opportunity, opportunity_id)
    if not opportunity_obj:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    db.delete(opportunity_obj)
    db.commit()
