from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.projects.project import Project
from app.models.projects.feedback import ProjectFeedback
from app.models.projects.project_tech_map import ProjectTechMap
from app.models.services.service_teck import ServiceTech
from app.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate
from app.auth.deps import get_current_user

router = APIRouter(prefix="/admin/projects", tags=["Projects"])

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Create the core project first (source of truth)
    project = Project(
        title=payload.title,
        description=payload.description,
        photo_url=payload.photo_url,
        project_link=payload.project_link,
    )

    db.add(project)
    db.flush()  # ensures project.id is available

    techs = (
        db.query(ServiceTech)
        .filter(ServiceTech.id.in_(payload.tech_ids))
        .all()
    )

    # Reject if any tech_id is invalid
    if len(techs) != len(payload.tech_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more tech IDs are invalid",
        )
    
    for tech in techs:
        db.add(
            ProjectTechMap(
                project_id=project.id,
                tech_id=tech.id,
            )
        )
    
    db.commit()
    db.refresh(project)

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        photo_url=project.photo_url,
        techs=[tech.name for tech in techs],
        project_link=project.project_link,
        feedbacks=[],  # feedbacks are added later
        created_at=project.created_at,
        updated_at=project.updated_at,
    )

@router.get("", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    projects = db.query(Project).all()
    responses = []

    for project in projects:
        # Fetch tech names via join table
        techs = (
            db.query(ServiceTech.name)
            .join(ProjectTechMap, ProjectTechMap.tech_id == ServiceTech.id)
            .filter(ProjectTechMap.project_id == project.id)
            .all()
        )

        # Fetch feedbacks for this project
        feedbacks = (
            db.query(ProjectFeedback)
            .filter(ProjectFeedback.project_id == project.id)
            .all()
        )

        responses.append(
            ProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                photo_url=project.photo_url,
                techs=[t[0] for t in techs],
                project_link=project.project_link,
                feedbacks=[
                    {
                        "id": f.id,
                        "client_name": f.client_name,
                        "client_photo": f.client_photo,
                        "feedback_description": f.feedback_description,
                        "rating": f.rating,
                    }
                    for f in feedbacks
                ],
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        )

    return responses

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_detail(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    # Fetch tech names
    techs = (
        db.query(ServiceTech.name)
        .join(ProjectTechMap, ProjectTechMap.tech_id == ServiceTech.id)
        .filter(ProjectTechMap.project_id == project.id)
        .all()
    )

    # Fetch feedbacks
    feedbacks = (
        db.query(ProjectFeedback)
        .filter(ProjectFeedback.project_id == project.id)
        .all()
    )

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        photo_url=project.photo_url,
        techs=[t[0] for t in techs],
        project_link=project.project_link,
        feedbacks=[
            {
                "id": f.id,
                "client_name": f.client_name,
                "client_photo": f.client_photo,
                "feedback_description": f.feedback_description,
                "rating": f.rating,
            }
            for f in feedbacks
        ],
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    # Update simple fields
    for field, value in payload.model_dump(
        exclude_unset=True,
        exclude_none=True,
    ).items():
        if field != "tech_ids":
            setattr(project, field, value)
    
    if payload.tech_ids is not None:
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

        # Remove old mappings
        db.query(ProjectTechMap).filter(
            ProjectTechMap.project_id == project.id
        ).delete()

        # Add new mappings
        for tech in techs:
            db.add(
                ProjectTechMap(
                    project_id=project.id,
                    tech_id=tech.id,
                )
            )
            
    db.commit()
    db.refresh(project)

    techs = (
        db.query(ServiceTech.name)
        .join(ProjectTechMap, ProjectTechMap.tech_id == ServiceTech.id)
        .filter(ProjectTechMap.project_id == project.id)
        .all()
    )

    feedbacks = (
        db.query(ProjectFeedback)
        .filter(ProjectFeedback.project_id == project.id)
        .all()
    )

    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        photo_url=project.photo_url,
        techs=[t[0] for t in techs],
        project_link=project.project_link,
        feedbacks=[
            {
                "id": f.id,
                "client_name": f.client_name,
                "client_photo": f.client_photo,
                "feedback_description": f.feedback_description,
                "rating": f.rating,
            }
            for f in feedbacks
        ],
        created_at=project.created_at,
        updated_at=project.updated_at,
    )

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    # Remove tech mappings explicitly
    db.query(ProjectTechMap).filter(
        ProjectTechMap.project_id == project_id
    ).delete()

    # Feedbacks are deleted automatically via CASCADE
    db.delete(project)
    db.commit()

    return
