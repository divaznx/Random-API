from fastapi import FastAPI
from app.providers.dog import get_random_dog
from app.providers.meal import get_random_meal
from app.providers.nasa import get_random_space
from app.services.random_engine import get_random_engine

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Random Engine API v1.0.0"}

@app.get("/random/dog")
async def get_random_dog_route():
    return await get_random_dog()

@app.get("/random/meal")
async def get_random_meal_route():
    return await get_random_meal()

@app.get("/random/space")
async def get_random_space_route():
    return await get_random_space()

@app.get("/random")
async def get_random_route():
    return await get_random_engine()
