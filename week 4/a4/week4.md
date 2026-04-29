C4 — APIs and Data Acquisition

## What I built

**Q1.** For A4, I am using the OpenWeatherMap API key to call out 4 fields in my python script called **week 4/a4/west_coast_weather.py**. The 4 fields I chose were city names, minimum temperature, maximum temperature, and description of the weather.

## Request URL (my wording)

**Q2.** My script builds a request URL that is sent to OpenWeather. The 3 components needed for the request URL are:

1. base url which is the web address the script is sending the request to
2. endpoint which is the specific path of the web address that I am requesting from
3. parameters which come at the end of the url and tells the server what I want in my request (example: city, temp, description)

## Request parameters

My script sends these query parameters after the `?` in the URL

- `q` — the city / location string I am asking about.
- `appid` — my OpenWeather API key (loaded from the environment, not pasted in the code).
- `units` — set to `imperial` so temperatures come back in Fahrenheit.

## JSON and my four fields

**Q3.** The response body is **JSON format**.

**Q4.** I parse that text with **`json.loads(...)`** and store the result in a Python dictionary called **`payload`**.

**Q5.** Here is how my four saved fields map onto the JSON inside `payload`:

| What I save | JSON location (in `payload`) |
|-------------|------------------------------|
| City name | `name` |
| Minimum temperature | `main` → `temp_min` |
| Maximum temperature | `main` → `temp_max` |
| Weather description | `weather` (a list) → first item → `description` |

Summary: The API returns JSON. I parse it into `payload`. I read `name` for the city, `main.temp_min` and `main.temp_max` for temperatures, and the first `weather` item’s `description` for the condition text.

## API key safety

**Q6.** My API key is stored in `.env' in NAME=API_KEY_STRING (`OPENWEATHER_API_KEY=<my secret key>`). The left side is the environment variable name which is used when calling the API KEY in the python script. The right side is the actual secret string. My script never pastes the secret directly into the Python file—it reads it through that variable name after `.env` is loaded.

**Q7.** After `load_env_file()` runs, my script reads the key with `os.environ.get("OPENWEATHER_API_KEY")`

**Q8.** My `.gitignore` file lists `.env`, so Git will not track the secrets file if this folder is put under version control. That helps keep the API key out of a public repo.

## Endpoint return + what I did with the data

**Q9.** OpenWeather’s `/data/2.5/weather` endpoint returns one current snapshot for the location in `q` (current conditions at request time), not a multi-day forecast. That matches the “current weather” API and my `fetch_current_weather` function, which calls the `/weather` path.

**Q10.** I write `OpenWeather.csv` and `openweather.json`. After I build one row per city, I sort the rows from highest minimum temperature to lowest.

**Q11.** I picked these West Coast cities to compare the weather during the spring and see which place feels “best” to me. In my script, I wanted to rank cities by highest `temp_min` first so that I can determine whether I am able to withstand the minimum temperature if I visit.

