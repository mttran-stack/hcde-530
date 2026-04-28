import csv
import json
#os means operating system and is used when reading and writing files to the operating system.
import os
#creates a path to the .env file
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

#function to load the .env file
def load_env_file(file_name=".env"):
    env_path = Path(__file__).with_name(file_name)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ[key.strip().lstrip("\ufeff")] = value.strip()


load_env_file()
#stores the API key safely in the environment variable
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
#base url is the web address of the API that I send requests to. This is required for all request urls.
BASE_URL = "https://api.openweathermap.org/data/2.5"
#openweather responds with a JSON file and translates it into a python dictionary.
JSON_OUTPUT = "openweather.json"
CSV_OUTPUT = "OpenWeather.csv"

#west coast cities in the usa that I am requesting weather data for from the API
CITIES = [
    "Seattle, WA, US",
    "Portland, OR, US",
    "San Francisco, CA, US",
    "San Jose, CA, US",
    "Los Angeles, CA, US",
    "San Diego, CA, US",
    "Oakland, CA, US",
    "Sacramento, CA, US",
]

#city, temp min, temp max, and description are the fields that I am requesting from the API. These are the keys that the json file returns.
FIELD_CITY = "city name"
FIELD_TEMP_MIN = "temp min"
FIELD_TEMP_MAX = "temp max"
FIELD_DESCRIPTION = "description"

#checks if the API key is found in the .env file. If it is not found, then it raises a ValueError in the terminal.
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in .env")


def fetch_current_weather(city_query):
   #params is a python dictionary that the json file reads and translates using the base url. parameters (or query string) is required for the script to build a request url.
    params = {"q": city_query, "appid": API_KEY, "units": "imperial"}
    #'/weather' is the endpoint that I am requesting data from. This is also required to execute the request url.
    url = f"{BASE_URL}/weather?{urlencode(params)}"
    try:
        with urlopen(url, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as err:
        try:
            detail = json.loads(err.read().decode("utf-8"))
            message = detail.get("message", detail)
        except (json.JSONDecodeError, ValueError):
            message = err.reason
        raise RuntimeError(f"HTTP {err.code}: {message}") from err
    except URLError as err:
        raise RuntimeError(f"Network error: {err.reason}") from err

    cod = payload.get("cod")
    if cod not in (200, "200"):
        message = payload.get("message", payload)
        raise RuntimeError(f"OpenWeather API error (cod={cod}): {message}")
    return payload


def extract_record(payload):
   #payload is the variable that stores the dictionary that the json file returns.
    main = payload.get("main") or {}
    weather_list = payload.get("weather") or []
    desc = weather_list[0].get("description") if weather_list else None
    #you can verfiy that this is a dictionary by the curly brackets and colons.
    return {
        FIELD_CITY: payload.get("name"),
        FIELD_TEMP_MIN: main.get("temp_min"),
        FIELD_TEMP_MAX: main.get("temp_max"),
        FIELD_DESCRIPTION: desc,
    }


def write_json_file(records):
    with open(JSON_OUTPUT, "w", encoding="utf-8") as output:
        json.dump({"openweather": records}, output, indent=2)


def write_csv_file(rows):
    fieldnames = [
        FIELD_CITY,
        FIELD_TEMP_MIN,
        FIELD_TEMP_MAX,
        FIELD_DESCRIPTION,
    ]
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        if rows:
            writer.writerows(rows)


def main():
    records = []
    for city in CITIES:
        try:
            payload = fetch_current_weather(city)
        except RuntimeError as err:
            err_s = str(err)
            if "429" in err_s or "401" in err_s:
                print(f"Stopped while fetching {city}: {err}")
                break
            print(f"Skipping {city} due to error: {err}")
            continue
        records.append(extract_record(payload))

    #this function sorts the rows in order of the highest minimum temperature to the lowest minimum temperature.
    def _min_temp_sort_key(row):
        value = row.get(FIELD_TEMP_MIN)
        if value is None:
            return float("-inf")
        return float(value)

    records.sort(key=_min_temp_sort_key, reverse=True)

    write_json_file(records)
    write_csv_file(records)
    print(f"Saved {len(records)} rows to {CSV_OUTPUT}")
    print(f"Saved {len(records)} records to {JSON_OUTPUT}")


if __name__ == "__main__":
    main()
