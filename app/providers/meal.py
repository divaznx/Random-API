import httpx
import os
from dotenv import load_dotenv
load_dotenv()

async def get_random_meal():
    async with httpx.AsyncClient() as client:
        response = await client.get(os.getenv("MEAL_API_URL"))
        data = response.json()
        meal = data["meals"][0]

        return {
            "type":"meal",
            "name":meal["strMeal"],
            "image":meal["strMealThumb"],
            "ingredients":[
                meal["strIngredient1"],
                meal["strIngredient2"],
                meal["strIngredient3"],
                meal["strIngredient4"],
                meal["strIngredient5"],
                meal["strIngredient6"],
                meal["strIngredient7"],
                meal["strIngredient8"],
                meal["strIngredient9"],
            ],
            "instructions":meal["strInstructions"],
            "status":response.status_code,
            "source":"The Meal DB"
        }
