import requests
import pandas as pd


CITIES = [
    "Riyadh",
    "Salalah",
    "Amman",
    "Istanbul",
    "London",
    "Munich",
    "Zurich",
    "Cairo",
    "Khartoum",
]

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_locations(cities=CITIES):
    locations = []

    for city in cities:
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        result = response.json()

        if "results" not in result or not result["results"]:
            raise ValueError(f"Location not found: {city}")

        location = result["results"][0]

        locations.append({
            "city": city,
            "country": location["country"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "timezone": location["timezone"],
        })

    return pd.DataFrame(locations)