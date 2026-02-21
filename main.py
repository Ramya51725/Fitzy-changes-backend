from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from models.category import Category
from models.exemodel import Exercise
from models.dietmodel import DietVeg
from models.model import User
from models.nonveg_model import DietNonVeg
from models.exercise_log import ExerciseLog
from models.exercise_progress import ExerciseProgress
from routers import user, diet, nonveg_diet, exercise,category, exercise_log
from routers import progress
from routers import exercise_progress


app = FastAPI()

# Allow both localhost and 127.0.0.1 for CORS
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],
)

app.router.redirect_slashes = False # Prevent unwanted redirects

app.include_router(exercise_progress.router)
app.include_router(exercise_log.router)
app.include_router(progress.router)
app.include_router(user.router)
app.include_router(diet.router)
app.include_router(nonveg_diet.router)
app.include_router(exercise.router)
app.include_router(category.router)

# 🔥 Tables & Migrations on Startup
@app.on_event("startup")
def startup_event():
    try:
        print("DEBUG: Starting table creation...")
        Base.metadata.create_all(bind=engine)
        print("DEBUG: Table creation finished.")
        
        # 🔥 MANUAL MIGRATIONS (Ensure new columns exist)
        from sqlalchemy import text
        with engine.connect() as conn:
            # 1. Update user_progress
            try:
                conn.execute(text("ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();"))
                conn.commit()
            except Exception as e:
                print(f"Migration 1 error: {e}")

            # 2. Update exercise_progress
            try:
                conn.execute(text("ALTER TABLE exercise_progress ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();"))
                conn.execute(text("ALTER TABLE exercise_progress ADD COLUMN IF NOT EXISTS last_completed_date TIMESTAMPTZ;"))
                conn.commit()
            except Exception as e:
                print(f"Migration 2 error: {e}")
            
        print("Database synced successfully ✅")
    except Exception as e:
        print(f"Database sync error during startup: {e}")

@app.get("/")
def get_home():
    return {"msg": "Welcome to Fitzy Lift.Sweat.Repeat"}


# real code 1