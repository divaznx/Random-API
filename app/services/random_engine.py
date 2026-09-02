import random
from fastapi import HTTPException
from app.providers.aqi import get_random_aqi
from app.providers.dog import get_random_dog
from app.providers.fact import get_random_fact
from app.providers.meal import get_random_meal
from app.providers.nasa import get_random_space

VALID_CATEGORIES = ("dog", "meal", "space", "fact", "aqi")

_PROVIDERS = {
    "dog": get_random_dog,
    "meal": get_random_meal,
    "space": get_random_space,
    "fact": get_random_fact,
    "aqi": get_random_aqi,
}

async def get_random_engine(category: str | None = None):
    if category is None:
        category = random.choice(VALID_CATEGORIES)
    elif category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}.",
        )

    return await _PROVIDERS[category]()
