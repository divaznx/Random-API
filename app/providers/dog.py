import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SOURCE = "Dog CEO"

async def get_random_dog():
    url = os.getenv("DOG_API_URL")
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
        image = data["message"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    if not isinstance(image, str) or not image.strip():
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    return {
        "type": "dog",
        "image": image,
        "status": response.status_code,
        "source": SOURCE,
    }
