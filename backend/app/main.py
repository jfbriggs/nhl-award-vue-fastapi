from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from scripts.preprocess import merge_process, get_seasons, split_data
from scripts.model import NorrisModel
from scripts.gather_data import get_current_data, get_nhl_players
from typing import Optional
import datetime

app = FastAPI()
data_src = '../past_data'

origins = ["http://localhost:8080", "http://localhost"]

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
    current_dt = datetime.datetime.now()
    current_dt = current_dt.strftime("%a, %b %w0 %I:%M%p PT")

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


@app.get('/')
async def hello():
    return {"message": "Welcome to the home of Norris Trophy predictions!"}


@app.get('/update')
async def process_data():
    global model
    global current_data
    global nhl_data
    global last_updated

    model, current_data, nhl_data, last_updated = setup()

    return {"message": "Data processed."}


@app.get('/predict')
async def get_predictions(refresh: Optional[bool] = False):
    if refresh:
        await process_data()

    top_ten = model.predict(current_data)
    results = {i + 1: top_ten[i] for i in range(10)}

    results = compile_output(results)

    return {"results": results, "updated": last_updated}


model, current_data, nhl_data, last_updated = setup()

if __name__ == "__main__":
    uvicorn.run(app, port=8500)
