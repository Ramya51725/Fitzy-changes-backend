from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from models.category import Category
from models.exemodel import Exercise
from models.dietmodel import DietVeg
from models.model import User
from models.nonveg_model import DietNonVeg
from routers import user, diet, nonveg_diet, exercise,category
from routers import progress
from routers import exercise_progress





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],
)

app.include_router(exercise_progress.router)
app.include_router(progress.router)
app.include_router(user.router)
app.include_router(diet.router)
app.include_router(nonveg_diet.router)
app.include_router(exercise.router)
app.include_router(category.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def get_home():
    return {"msg": "Welcome to Fitzy Lift.Sweat.Repeat"}


# real code 1