import httpx
import os
from dotenv import load_dotenv
load_dotenv()

async def get_random_dog():
    async with httpx.AsyncClient() as client:
        response = await client.get(os.getenv("DOG_API_URL"))
        data = response.json()

        return {
            "type":"dog",
            "image":data["message"],
            "status":response.status_code,
            "source":"Dog CEO"
        }