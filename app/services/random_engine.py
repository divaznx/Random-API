import random
from fastapi import HTTPException
from app.providers.dog import get_random_dog
from app.providers.meal import get_random_meal
from app.providers.nasa import get_random_space

VALID_CATEGORIES = ("dog", "meal", "space")

async def get_random_engine(category: str | None = None):
    if category is None:
        category = random.choice(VALID_CATEGORIES)
    elif category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category '{category}'. Must be one of: dog, meal, space.",
        )

    if category == "dog":
        return await get_random_dog()

    if category == "meal":
        return await get_random_meal()

    return await get_random_space()
