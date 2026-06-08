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

**Q6.** My API key is stored in `.env` in NAME=API_KEY_STRING (`OPENWEATHER_API_KEY=<my secret key>`). The left side is the environment variable name which is used when calling the API KEY in the python script. The right side is the actual secret string. My script never pastes the secret directly into the Python file—it reads it through that variable name after `.env` is loaded.

**Q7.** After `load_env_file()` runs, my script reads the key with `os.environ.get("OPENWEATHER_API_KEY")`

**Q8.** My `.gitignore` file lists `.env`, so Git will not track the secrets file if this folder is put under version control. That helps keep the API key out of a public repo.

## Endpoint return + what I did with the data

**Q9.** OpenWeather’s `/data/2.5/weather` endpoint returns one current snapshot for the location in `q` (current conditions at request time), not a multi-day forecast. That matches the “current weather” API and my `fetch_current_weather` function, which calls the `/weather` path.

**Q10.** I write `OpenWeather.csv` and `openweather.json`. After I build one row per city, I sort the rows from highest minimum temperature to lowest.

**Q11.** I picked these West Coast cities to compare current conditions during spring. I ranked by highest `temp_min` first because that is the constraint I cared about for the decision — whether I could tolerate the coldest end of the range in each place. That same pattern shows up in HCD work: you pull external data, then sort or filter by the variable that matters for the question you are trying to answer.

---

## HCD reflection — how this connects to human-centered design practice

### Why APIs matter in UX research and design

Much of the data HCD practitioners work with does not start in a spreadsheet on your laptop. It lives in survey platforms, analytics dashboards, recruiting panels, repository tools, or public review feeds. Getting that data into a repeatable analysis usually means **reading API documentation**, choosing the fields that answer your question, making an HTTP request, and parsing structured JSON — not copying rows by hand. Week 4 was practice for that workflow, even though my OpenWeather dataset is not itself a user study.

### What I practiced with `west_coast_weather.py`

In `week 4/a4/west_coast_weather.py`, I worked through the same steps I would use for a research or product API:

1. **Read the docs** to learn what the endpoint returns and which query parameters it accepts (`q`, `appid`, `units`).
2. **Scope the fields** I actually need — city name, min/max temp, description — instead of saving the entire JSON blob unexamined.
3. **Parse nested JSON** (`main.temp_min`, `weather[0].description`) into flat columns I can sort and export.
4. **Write repeatable output** (`OpenWeather.csv`, `openweather.json`) so I can compare cities without re-running manual steps.

That mirrors how I would pull, for example, participant metadata from an export API or filter a large response down to the columns needed for synthesis. The weather use case is personal, but the **acquisition pipeline** is the same skill.

### Professional judgment: credentials and scoping

Two choices in this script map directly to professional HCD practice:

- **API key in `.env`, listed in `.gitignore`:** On a team project or public repo, credentials cannot live in the script file. Loading `OPENWEATHER_API_KEY` through the environment is the same habit I would use for a client’s survey token or analytics key.
- **Sorting by `temp_min`:** I made an explicit analysis decision — rank cities by the variable that matched my decision criterion. In research, that is analogous to ranking segments by response rate, filtering tools by a feature requirement, or ordering themes by frequency. The code does not decide what matters; I do, and the script encodes that choice.

### In-class work: app reviews API (`fetch_app_reviews.py`)

I also used the course **HCDE 530 reviews API** in `week 4/fetch_app_reviews.py`, which returns fabricated app reviews for UX research tools. Each review includes a **category** (`field research`, `user research`, `research repository`) and **helpful votes**. I saved the results to `app review data.json` and `category_helpful_votes.csv`.

That exercise is closer to a real HCD task: **landscape or competitive analysis** — gathering many opinions about research tools in one pass, grouped by the type of work they support. An API lets me collect hundreds of rows repeatably; from there I could compare which categories get the most helpful votes or which pain points recur in review text. I am not making product decisions from this demo data alone, but I am practicing the acquisition step that would feed a synthesis or stakeholder readout.

### Competency claim (C4 + HCD)

I claim **C4 — APIs and data acquisition**: I found an API, read what the endpoint returns, made an HTTP request in Python, parsed JSON, kept my key out of version control, and wrote a short explanation of what I chose to do with the response. The HCD connection is that this is how practitioners **bring external evidence into a study or design process** — scoped fields, safe credentials, repeatable exports — whether the source is weather, app reviews, or a research platform I use on a project.

