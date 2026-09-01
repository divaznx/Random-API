# Random Engine API

A FastAPI service that returns random content from public APIs: a dog photo, a meal recipe, or NASA’s Astronomy Picture of the Day. `GET /random` picks one of those providers at random.

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

### `GET /random/dog`

Fetches a random dog photo from [Dog CEO](https://dog.ceo/dog-api/).

**Live:** [https://random-insights-api.onrender.com/random/dog](https://random-insights-api.onrender.com/random/dog)

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

### `GET /random/meal`

Fetches a random recipe from [TheMealDB](https://www.themealdb.com/api.php), including name, image, first nine ingredients, and cooking instructions.

**Live:** [https://random-insights-api.onrender.com/random/meal](https://random-insights-api.onrender.com/random/meal)

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
| `ingredients` | Up to nine ingredient names (unused slots may be empty) |
| `instructions` | Cooking steps |
| `status` | Upstream HTTP status |
| `source` | `"The Meal DB"` |

### `GET /random/space`

Fetches NASA’s Astronomy Picture of the Day ([APOD](https://api.nasa.gov/)). Requires a `NASA_API_KEY` in the environment.

**Live:** [https://random-insights-api.onrender.com/random/space](https://random-insights-api.onrender.com/random/space)

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

### `GET /random`

Randomly chooses one of the three providers (`dog`, `meal`, or `space`) and returns that provider’s JSON. The `type` field tells you which one you got.

**Live:** [https://random-insights-api.onrender.com/random](https://random-insights-api.onrender.com/random)

## Project layout

```
app/
  main.py                 # FastAPI routes
  providers/
    dog.py
    meal.py
    nasa.py
  services/
    random_engine.py      # picks dog / meal / space
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
```

Get a NASA API key at [https://api.nasa.gov/](https://api.nasa.gov/). Do not commit `.env`.

## Run locally

```powershell
uvicorn app.main:app --reload --port 8000
```

Then open [http://127.0.0.1:8000/random](http://127.0.0.1:8000/random) or [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
