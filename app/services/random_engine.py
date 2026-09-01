import random
from app.providers.dog import get_random_dog
from app.providers.meal import get_random_meal
from app.providers.nasa import get_random_space

async def get_random_engine():

    categories = random.choice(["dog", "meal", "space"])

    if categories == "dog":
        return await get_random_dog()

    elif categories == "meal":
        return await get_random_meal()

    else:
        return await get_random_space()


