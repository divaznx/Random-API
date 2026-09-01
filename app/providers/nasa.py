import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SOURCE = "NASA"

async def get_random_space():
    url = os.getenv("NASA_API_URL")
    api_key = os.getenv("NASA_API_KEY")
    if not url or not api_key:
        raise HTTPException(status_code=500, detail="Server is missing API configuration")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"api_key": api_key})
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail=f"Failed to reach {SOURCE}")

    if not response.is_success:
        raise HTTPException(
            status_code=502,
            detail=f"{SOURCE} returned {response.status_code}",
        )

    try:
        data = response.json()
        title = data["title"]
        image = data["url"]
        description = data["explanation"]
        date = data["date"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    required = (title, image, description, date)
    if any(not isinstance(value, str) or not value.strip() for value in required):
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    return {
        "type": "space",
        "title": title,
        "image": image,
        "description": description,
        "date": date,
        "status": response.status_code,
        "source": SOURCE,
    }
