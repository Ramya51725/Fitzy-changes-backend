from pydantic import BaseModel


class ProgressCreate(BaseModel):
    user_id: int
    level: str
    category_id: int


class ProgressUpdate(BaseModel):
    current_month: int
    current_week: int
    current_day: int
    completed_days: int
    completed_exercises: int
    is_month_completed: bool
    is_level_completed: bool


class ProgressResponse(BaseModel):
    progress_id: int
    user_id: int
    level: str
    category_id: int
    current_month: int
    current_week: int
    current_day: int
    completed_days: int
    completed_exercises: int
    is_month_completed: bool
    is_level_completed: bool

    class Config:
        orm_mode = True
