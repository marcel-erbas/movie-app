import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
URL = "https://www.omdbapi.com/"


def fetch_movie(title: str):
    """Fetch movie data from the OMDb API"""
    params = {
        "apikey": API_KEY,
        "t": title
    }
    response = requests.get(URL, params=params, timeout=10)

    data = response.json()

    if data.get("Error") == "Movie not found!":
        raise ValueError("Movie not found!")

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return data['Title'], data['Year'], data['imdbRating'], data['Poster']