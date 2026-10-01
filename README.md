# Mini Weather ETL Pipeline

A small ETL pipeline in Python that extracts current weather data for Cairo from a public API, transforms it with Pandas, and loads it into a local SQLite database.

## Tech Stack
- **Python**
- **Requests** (API extraction)
- **Pandas** (data transformation)
- **SQLite3** (local storage)

## Pipeline Architecture
1. **Extract**: `extract()` pulls current weather data from the [Open-Meteo API](https://open-meteo.com/) (with a timeout and error handling).
2. **Transform**: `transform()` renames columns and adds an extraction timestamp.
3. **Load**: `load()` appends the row to the `weather_data` table in `weather.db`.

## How to Run
```bash
pip install -r requirements.txt
python etl_pipeline.py
```

Each run adds one new row, so running it on a schedule builds a weather history.

## Example Output
```
1. [Extract] Pulling weather data...
-> Extracted successfully.
2. [Transform] Processing data...
               time  interval  Temperature_C  Wind_Speed  Humidity            Extraction_Time
0  2026-10-01T07:30       900           25.2         4.1        50 2026-10-01 10:35:26.896043
3. [Load] Saving to SQLite...
-> Saved to weather.db successfully.
```

## Reading the Data
```bash
sqlite3 weather.db "SELECT * FROM weather_data;"
```
or with Python:
```python
import sqlite3, pandas as pd
df = pd.read_sql("SELECT * FROM weather_data", sqlite3.connect("weather.db"))
print(df)
```

## Settings
Location (latitude/longitude), database name, and timeout are defined at the top of `etl_pipeline.py`.

## Possible Next Steps
- Schedule the pipeline to run every hour (cron / Task Scheduler)
- Build a dashboard on top of the collected data
