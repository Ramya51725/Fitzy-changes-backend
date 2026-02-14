from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.exercise_progress import ExerciseProgress
from schemas.exercise_progress import (
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse
)

router = APIRouter(
    prefix="/progress",
    tags=["Exercise Progress"]
)


# 🔥 CREATE PROGRESS
@router.post("/create", response_model=ProgressResponse)
def create_progress(progress: ProgressCreate, db: Session = Depends(get_db)):

    existing = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == progress.user_id,
        ExerciseProgress.level == progress.level
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Progress already exists")

    new_progress = ExerciseProgress(**progress.dict())

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return new_progress


# 🔥 GET PROGRESS
@router.get("/{user_id}/{level}", response_model=ProgressResponse)
def get_progress(user_id: int, level: str, db: Session = Depends(get_db)):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    return progress


# 🔥 UPDATE PROGRESS (Partial Update)
@router.put("/update/{user_id}/{level}", response_model=ProgressResponse)
def update_progress(
    user_id: int,
    level: str,
    progress_update: ProgressUpdate,
    db: Session = Depends(get_db)
):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    update_data = progress_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(progress, key, value)

    db.commit()
    db.refresh(progress)

    return progress
