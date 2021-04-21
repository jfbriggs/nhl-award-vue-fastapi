import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from scripts.preprocess import merge_process, get_seasons, split_data
from scripts.model import NorrisModel
from scripts.gather_data import get_current_data, get_nhl_players
import datetime
import asyncio
import socket

app = FastAPI()
data_src = '../data'

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Functionality to execute upon server spin-up
def setup():
    print("Activating server and updating current season data...")
    current_year = str(int(get_seasons(data_src)[-1][-4:]) + 1)
    get_current_data(current_year)

    print("Gathering updated roster info from NHL API...")
    roster_data = get_nhl_players()

    print("Processing data and training model...")
    train_data, curr_data = split_data(merge_process(data_src))
    estimator = NorrisModel()
    estimator.fit(train_data)

    print("Updating date/time for data/model refresh...")
    d_naive = datetime.datetime.now()
    timezone = pytz.timezone("America/Los_Angeles")
    d_aware = timezone.localize(d_naive)
    current_dt = d_aware.strftime("%a, %b %w0 %I:%M%p PT")

    print("Model fit.  Ready for prediction requests.")
    return estimator, curr_data, roster_data, current_dt


# Takes prediction results dict, adds player headshot URL, player NHL.com page URL, team logo URL
def compile_output(results: dict) -> dict:
    print("Compiling output: prediction results + player information...")

    # Iterate through prediction results dict and add team logo URL, headshot URL
    for rank in results:
        team_abbrev = results[rank]["team"]

        # access NHL roster data, find player's ID and team-dashed string, form headshot, logo URLs, & NHL.com URL and add to dict
        team_roster = nhl_data[team_abbrev]
        for player_id in team_roster:
            if team_roster[player_id]["name"] == results[rank]["name"]:
                headshot_url = f"https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{player_id}.jpg"
                results[rank]["headshot_url"] = headshot_url

                logo_url = f"https://cdn.usteamcolors.com/images/nhl/{team_roster[player_id]['team_dashed']}.svg"
                results[rank]["team_logo_url"] = logo_url

                # create URL for player's NHL.com page
                name_dashed = team_roster[player_id]["name"].lower().replace(" ", "-")
                results[rank]["nhl_page"] = f"https://www.nhl.com/player/{name_dashed}-{player_id}"

    return results


@app.on_event('startup')
async def app_startup():

    # Repeating async task to refresh data/model after midnight each day
    async def update_data():
        while True:
            d_naive = datetime.datetime.now()
            timezone = pytz.timezone("America/Los_Angeles")
            d_aware = timezone.localize(d_naive)

            current_hr, current_min = d_aware.hour, d_aware.minute
            seconds_until_midnight = (1440 - (current_hr * 60 + current_min)) * 60

            print(f"Waiting {seconds_until_midnight} seconds until midnight to update data.")
            await asyncio.sleep(seconds_until_midnight)

            print("Time to update data now.")
            process_data()

    asyncio.create_task(update_data())


@app.get('/')
async def hello():
    return {"message": f"Welcome to the home of NHL award predictions!"}


def process_data() -> None:
    global model
    global current_data
    global nhl_data
    global last_updated

    print("Updating data...")

    model, current_data, nhl_data, last_updated = setup()

    print("Data and model updated/refreshed.")


@app.get('/predict')
async def get_predictions(players: int = 10) -> dict:  # players = number of players to provide in results

    top_results = model.predict(current_data, players)
    results = {i + 1: top_results[i] for i in range(len(top_results))}

    results = compile_output(results)

    return {"results": results, "updated": last_updated}


model, current_data, nhl_data, last_updated = setup()

if __name__ == "__main__":
    uvicorn.run(app, port=8500)