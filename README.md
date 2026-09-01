# Random Engine API

A FastAPI service that returns random content from public APIs: a dog photo, a meal recipe, or NASA’s Astronomy Picture of the Day. `GET /random` picks one of those providers at random.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Version message |
| GET | `/dog/random` | Random dog image ([Dog CEO](https://dog.ceo/dog-api/)) |
| GET | `/meal/random` | Random meal ([TheMealDB](https://www.themealdb.com/api.php)) |
| GET | `/space/random` | NASA Astronomy Picture of the Day |
| GET | `/random` | Randomly calls one of the three providers |

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

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

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

Then open [http://127.0.0.1:8000/random](http://127.0.0.1:8000/random) or [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Example response (`/dog/random`)

```json
{
  "type": "dog",
  "image": "https://images.dog.ceo/breeds/...",
  "status": 200,
  "source": "Dog CEO"
}
```

`/random` returns the same JSON shape as whichever provider was chosen. `type` is `dog`, `meal`, or `space`.
