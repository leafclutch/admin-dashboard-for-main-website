from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.projects.project import Project
from app.models.projects.feedback import ProjectFeedback
from app.schemas.projects import FeedbackCreate, FeedbackResponse
from app.auth.deps import get_current_user

router = APIRouter(
    prefix="/admin/projects",
    tags=["Project Feedbacks"],
)

@router.post(
    "/{project_id}/feedbacks",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_feedback(
    project_id: UUID,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Ensure project exists
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

    feedback = ProjectFeedback(
        project_id=project_id,
        client_name=payload.client_name,
        client_photo=payload.client_photo,
        feedback_description=payload.feedback_description,
        rating=payload.rating,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback

@router.get(
    "/{project_id}/feedbacks",
    response_model=list[FeedbackResponse],
)
def list_project_feedbacks(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Ensure project exists
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

    feedbacks = (
        db.query(ProjectFeedback)
        .filter(ProjectFeedback.project_id == project_id)
        .order_by(ProjectFeedback.created_at.desc())
        .all()
    )

    return feedbacks

@router.delete(
    "/feedbacks/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_feedback(
    feedback_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    feedback = (
        db.query(ProjectFeedback)
        .filter(ProjectFeedback.id == feedback_id)
        .first()
    )

    if not feedback:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found",
        )

    db.delete(feedback)
    db.commit()
    return


