import httpx
import os
from dotenv import load_dotenv
load_dotenv()

async def get_random_space():
    async with httpx.AsyncClient() as client:
        response = await client.get(os.getenv("NASA_API_URL"),
        params={
            "api_key":os.getenv("NASA_API_KEY")
        }
    
        )
        data = response.json()

        return {
            "type":"space",
            "title":data["title"],
            "image":data["url"],
            "description":data["explanation"],
            "date":data["date"],
            "status":response.status_code,
            "source":"NASA"
        }
