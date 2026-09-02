# Random Engine API

A FastAPI service that returns random content from public APIs: a dog photo, a meal recipe, NASA’s Astronomy Picture of the Day, a trivia fact, or city air quality. `GET /random` picks one of those providers at random.

## Live demo

This API is deployed on [Render](https://render.com/). Base URL:

**https://random-insights-api.onrender.com**

Interactive OpenAPI docs: [https://random-insights-api.onrender.com/docs](https://random-insights-api.onrender.com/docs)

> Render free-tier services spin down after idle time. The first request after a pause can take 30–60 seconds to wake up.

## Endpoints

All routes are `GET` and return JSON. No authentication is required.

### `GET /`

Health / version check. Confirms the service is running.

**Live:** [https://random-insights-api.onrender.com/](https://random-insights-api.onrender.com/)

```json
{
  "message": "Random Engine API v1.0.0"
}
```

### `GET /random/{category}`

Fetches a random item for one category. Valid values: `dog`, `meal`, `space`, `fact`, `aqi` (case-insensitive).

**Live examples:**
- [https://random-insights-api.onrender.com/random/dog](https://random-insights-api.onrender.com/random/dog)
- [https://random-insights-api.onrender.com/random/meal](https://random-insights-api.onrender.com/random/meal)
- [https://random-insights-api.onrender.com/random/space](https://random-insights-api.onrender.com/random/space)
- [https://random-insights-api.onrender.com/random/fact](https://random-insights-api.onrender.com/random/fact)
- [https://random-insights-api.onrender.com/random/aqi](https://random-insights-api.onrender.com/random/aqi)
- [https://random-insights-api.onrender.com/random/aqi?city=Chennai](https://random-insights-api.onrender.com/random/aqi?city=Chennai)

Invalid values (for example `/random/cat`) return **400**:

```json
{
  "detail": "Invalid category 'cat'. Must be one of: dog, meal, space, fact, aqi."
}
```

If an upstream API is unreachable or returns bad data, the API returns **502**. Missing server configuration returns **500**.

#### `dog`

Random dog photo from [Dog CEO](https://dog.ceo/dog-api/).

```json
{
  "type": "dog",
  "image": "https://images.dog.ceo/breeds/...",
  "status": 200,
  "source": "Dog CEO"
}
```

| Field | Meaning |
|-------|---------|
| `type` | Always `"dog"` |
| `image` | URL of a random dog photo |
| `status` | Upstream HTTP status |
| `source` | `"Dog CEO"` |

#### `meal`

Random recipe from [TheMealDB](https://www.themealdb.com/api.php), including name, image, up to nine non-empty ingredients, and cooking instructions.

```json
{
  "type": "meal",
  "name": "Beef Wellington",
  "image": "https://www.themealdb.com/images/media/meals/...",
  "ingredients": ["Beef Fillet", "Mushrooms", "..."],
  "instructions": "Preheat the oven...",
  "status": 200,
  "source": "The Meal DB"
}
```

| Field | Meaning |
|-------|---------|
| `type` | Always `"meal"` |
| `name` | Recipe title |
| `image` | Thumbnail URL |
| `ingredients` | Up to nine non-empty ingredient names |
| `instructions` | Cooking steps |
| `status` | Upstream HTTP status |
| `source` | `"The Meal DB"` |

#### `space`

NASA’s Astronomy Picture of the Day ([APOD](https://api.nasa.gov/)). Requires a `NASA_API_KEY` in the environment.

```json
{
  "type": "space",
  "title": "The Andromeda Galaxy",
  "image": "https://apod.nasa.gov/apod/image/...",
  "description": "Explanation of the image...",
  "date": "2026-09-01",
  "status": 200,
  "source": "NASA"
}
```

| Field | Meaning |
|-------|---------|
| `type` | Always `"space"` |
| `title` | APOD title |
| `image` | Image or media URL |
| `description` | NASA explanation text |
| `date` | Observation / publish date (`YYYY-MM-DD`) |
| `status` | Upstream HTTP status |
| `source` | `"NASA"` |

#### `fact`

A random trivia fact from [API Ninjas](https://www.api-ninjas.com/api/facts). Requires `NINJA_API_KEY` and `NINJA_FACTS_URL` in the environment.

```json
{
  "type": "fact",
  "fact": "Honey never spoils.",
  "status": 200,
  "source": "API Ninjas"
}
```

| Field | Meaning |
|-------|---------|
| `type` | Always `"fact"` |
| `fact` | Trivia sentence |
| `status` | Upstream HTTP status |
| `source` | `"API Ninjas"` |

#### `aqi`

Air quality for a city from [API Ninjas Air Quality](https://www.api-ninjas.com/api/airquality). Requires `NINJA_API_KEY` and `NINJA_AQI_URL` in the environment.

`GET /random/aqi` picks a city at random. Pass `?city=Chennai` (or another city name) to request a specific place.

```json
{
  "type": "aqi",
  "city": "Chennai",
  "overall_aqi": 54,
  "pollutants": {},
  "status": 200,
  "source": "API Ninjas"
}
```

| Field | Meaning |
|-------|---------|
| `type` | Always `"aqi"` |
| `city` | City used for the lookup |
| `overall_aqi` | Combined air quality index |
| `pollutants` | Per-pollutant concentration and AQI |
| `status` | Upstream HTTP status |
| `source` | `"API Ninjas"` |

Unknown cities return **404**.

### `GET /random`

Randomly chooses one of the five providers (`dog`, `meal`, `space`, `fact`, or `aqi`) and returns that provider’s JSON. The `type` field tells you which one you got.

**Live:** [https://random-insights-api.onrender.com/random](https://random-insights-api.onrender.com/random)

## Project layout

```
app/
  main.py                 # FastAPI routes
  providers/
    aqi.py
    dog.py
    fact.py
    meal.py
    nasa.py
  services/
    random_engine.py      # picks dog / meal / space / fact / aqi
.env                      # local secrets (not committed)
requirements.txt
```

## Setup

Python 3.11 or newer. From the project root:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with `source venv/bin/activate`.

Create a `.env` file in the project root:

```
DOG_API_URL=https://dog.ceo/api/breeds/image/random
MEAL_API_URL=https://www.themealdb.com/api/json/v1/1/random.php
NASA_API_URL=https://api.nasa.gov/planetary/apod
NASA_API_KEY=your_nasa_api_key
NINJA_FACTS_URL=https://api.api-ninjas.com/v1/facts
NINJA_AQI_URL=https://api.api-ninjas.com/v1/airquality
NINJA_API_KEY=your_api_ninjas_key
```

Get a NASA API key at [https://api.nasa.gov/](https://api.nasa.gov/) and an API Ninjas key at [https://www.api-ninjas.com/](https://www.api-ninjas.com/). Do not commit `.env`. On Render, set the same variables in the service environment.

## Run locally

```powershell
uvicorn app.main:app --reload --port 8000
```

Then open [http://127.0.0.1:8000/random](http://127.0.0.1:8000/random) or [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
