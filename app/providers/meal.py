import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SOURCE = "The Meal DB"

async def get_random_meal():
    url = os.getenv("MEAL_API_URL")
    if not url:
        raise HTTPException(status_code=500, detail="Server is missing API configuration")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail=f"Failed to reach {SOURCE}")

    if not response.is_success:
        raise HTTPException(
            status_code=502,
            detail=f"{SOURCE} returned {response.status_code}",
        )

    try:
        data = response.json()
        meals = data["meals"]
        meal = meals[0]
        name = meal["strMeal"]
        image = meal["strMealThumb"]
        instructions = meal["strInstructions"]
    except (ValueError, KeyError, TypeError, IndexError):
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    if not meals or not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")
    if not isinstance(image, str) or not image.strip():
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")
    if not isinstance(instructions, str) or not instructions.strip():
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    ingredients = [
        meal.get(f"strIngredient{i}")
        for i in range(1, 10)
        if meal.get(f"strIngredient{i}")
    ]

    return {
        "type": "meal",
        "name": name,
        "image": image,
        "ingredients": ingredients,
        "instructions": instructions,
        "status": response.status_code,
        "source": SOURCE,
    }
