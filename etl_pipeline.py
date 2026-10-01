import sqlite3

import pandas as pd
import requests

# ---- Settings (change these without touching the logic) ----
LATITUDE = 30.0444    # Cairo
LONGITUDE = 31.2357
DB_NAME = "weather.db"
TABLE_NAME = "weather_data"
TIMEOUT_SECONDS = 10

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
)


def extract():
    """Pull current weather data from the Open-Meteo API."""
    print("1. [Extract] Pulling weather data...")
    response = requests.get(API_URL, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()  # raises an error if status is not 200
    data = response.json().get("current")
    if not data:
        raise ValueError("API response has no 'current' data")
    print("-> Extracted successfully.")
    return data


def transform(data):
    """Rename columns and add an extraction timestamp."""
    print("2. [Transform] Processing data...")
    df = pd.DataFrame([data])
    df = df.rename(columns={
        "temperature_2m": "Temperature_C",
        "wind_speed_10m": "Wind_Speed",
        "relative_humidity_2m": "Humidity",
    })
    df["Extraction_Time"] = pd.Timestamp.now()
    print(df)
    return df


def load(df):
    """Append the data to a SQLite table."""
    print("3. [Load] Saving to SQLite...")
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    print(f"-> Saved to {DB_NAME} successfully.")


def run_etl():
    try:
        data = extract()
        df = transform(data)
        load(df)
    except requests.RequestException as e:
        print(f"Extraction failed (network/API problem): {e}")
    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_etl()
