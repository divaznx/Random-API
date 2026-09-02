import os
import random

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SOURCE = "API Ninjas"
CITIES = ("London", "Chennai", "New York", "Tokyo", "Paris", "Delhi")

async def get_random_aqi():
    url = os.getenv("NINJA_AQI_URL")
    api_key = os.getenv("NINJA_API_KEY")
    if not url or not api_key:
        raise HTTPException(status_code=500, detail="Server is missing API configuration")

    city = random.choice(CITIES)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"city": city},
                headers={"X-Api-Key": api_key},
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail=f"Failed to reach {SOURCE}")

    if not response.is_success:
        raise HTTPException(
            status_code=502,
            detail=f"{SOURCE} returned {response.status_code}",
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail=f"{SOURCE} returned an invalid response")

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"No air quality data found for {city}",
        )

    return {
        "type": "aqi",
        "city": city,
        "overall_aqi": data.get("overall_aqi"),
        "pollutants": {key: value for key, value in data.items() if key != "overall_aqi"},
        "status": response.status_code,
        "source": SOURCE,
    }
