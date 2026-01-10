from fastapi import APIRouter, Depends, HTTPException, status # Tools to build the API
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.projects.project import Project
from app.models.projects.feedback import ProjectFeedback
from app.schemas.projects import FeedbackCreate, FeedbackResponse
from app.auth.deps import get_current_user # To check if the user is logged in

# Setup the router for project reviews (feedbacks)
router = APIRouter(
    prefix="/admin/projects",
    tags=["Project Feedbacks"],
)

# 1. Add a new review to a project
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
    # Step 1: Ensure the project exists before adding feedback
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

    # Step 2: Create the feedback record
    feedback = ProjectFeedback(
        project_id=project_id,
        client_name=payload.client_name,
        client_photo=payload.client_photo,
        feedback_description=payload.feedback_description,
        rating=payload.rating,
    )

    # Step 3: Save to database
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback

# 2. Get all reviews for a specific project
@router.get(
    "/{project_id}/feedbacks",
    response_model=list[FeedbackResponse],
)
def list_project_feedbacks(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Step 1: Check if the project exists
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

    # Step 2: Get all reviews for this project, newest first
    feedbacks = (
        db.query(ProjectFeedback)
        .filter(ProjectFeedback.project_id == project_id)
        .order_by(ProjectFeedback.created_at.desc())
        .all()
    )

    return feedbacks

# 3. Delete a specific review
@router.delete(
    "/feedbacks/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_feedback(
    feedback_id: UUID,
    db: Session = Depends(get_db),
    admin = Depends(get_current_user),
):
    # Step 1: Find the review in the database
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

    # Step 2: Delete the review and save changes
    db.delete(feedback)
    db.commit()
    return


