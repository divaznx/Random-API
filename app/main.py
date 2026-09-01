from fastapi import FastAPI, HTTPException
from app.services.random_engine import VALID_CATEGORIES, get_random_engine

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Random Engine API v1.0.0"}

@app.get("/random")
async def get_random_route():
    return await get_random_engine()

@app.get("/random/{category}")
async def get_random_category_route(category: str):
    category = category.strip().lower()
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}.",
        )
    return await get_random_engine(category)
