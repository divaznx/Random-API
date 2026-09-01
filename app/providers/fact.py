import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SOURCE = "API Ninjas"

async def get_random_fact():
    url = os.getenv("NINJA_FACTS_URL")
    api_key = os.getenv("NINJA_API_KEY")
    if not url or not api_key:
        raise HTTPException(status_code=500, detail="Server is missing API configuration")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"X-Api-Key": api_key})
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail=f"Failed to reach {SOURCE}")

    if not response.is_success:
        raise HTTPException(
            status_code=502,
            detail=f"{SOURCE} returned {response.status_code}",
        )

    try:
        data = response.json()
        fact = data[0]["fact"]
    except (ValueError, KeyError, TypeError, IndexError):
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    if not isinstance(fact, str) or not fact.strip():
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    return {
        "type": "fact",
        "fact": fact,
        "status": response.status_code,
        "source": SOURCE,
    }
