from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import random
import time

app = FastAPI()

@app.get("/weather")
def get_weather(q: str = Query(..., alias="q"), appid: str = Query(...)):
    # Simulate coordinates for a few cities
    city_coords = {
        "Nashville": {"lon": -86.7844, "lat": 36.1659, "country": "US", "id": 4644585},
        "London": {"lon": -0.1257, "lat": 51.5085, "country": "GB", "id": 2643743},
        "Delhi": {"lon": 77.2167, "lat": 28.6667, "country": "IN", "id": 1273294},
        "Tokyo": {"lon": 139.6917, "lat": 35.6895, "country": "JP", "id": 1850147},
    }
    city = city_coords.get(q, city_coords["Nashville"])
    now = int(time.time())
    sunrise = now - 3600
    sunset = now + 3600

    response = {
        "coord": {"lon": city["lon"], "lat": city["lat"]},
        "weather": [{
            "id": random.choice([800, 801, 802, 803, 804]),
            "main": random.choice(["Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm"]),
            "description": random.choice(["clear sky", "few clouds", "scattered clouds", "broken clouds", "shower rain"]),
            "icon": random.choice(["01d", "02d", "03d", "04d", "09d", "10d", "11d"])
        }],
        "base": "stations",
        "main": {
            "temp": round(random.uniform(280, 310), 2),
            "feels_like": round(random.uniform(280, 310), 2),
            "temp_min": round(random.uniform(278, 308), 2),
            "temp_max": round(random.uniform(282, 312), 2),
            "pressure": random.randint(980, 1050),
            "humidity": random.randint(40, 100),
            "sea_level": random.randint(980, 1050),
            "grnd_level": random.randint(950, 1040),
        },
        "visibility": 10000,
        "wind": {
            "speed": round(random.uniform(0, 10), 2),
            "deg": random.randint(0, 360),
            "gust": round(random.uniform(0, 15), 2)
        },
        "clouds": {"all": random.randint(0, 100)},
        "dt": now,
        "sys": {
            "type": 2,
            "id": random.randint(1000, 3000),
            "country": city["country"],
            "sunrise": sunrise,
            "sunset": sunset
        },
        "timezone": -18000,
        "id": city["id"],
        "name": q,
        "cod": 200
    }
    return JSONResponse(content=response)