from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from scripts.preprocess import merge_process, get_seasons, split_data
from scripts.model import NorrisModel
from scripts.gather_data import get_current_data
from typing import Optional

import pandas as pd

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

    print("Processing data and training model...")
    train_data, curr_data = split_data(merge_process(data_src))
    estimator = NorrisModel()
    estimator.fit(train_data)

    print("Model fit.  Ready for prediction requests.")
    return estimator, curr_data


@app.get('/')
async def hello():
    return {"message": "Welcome to the home of Norris Trophy predictions!"}


@app.get('/update')
async def process_data():
    global model
    global current_data

    model, current_data = setup()

    return {"message": "Data processed."}


@app.get('/predict')
async def get_predictions(refresh: Optional[bool] = False):
    if refresh:
        await process_data()

    top_ten = model.predict(current_data)

    results = {i: top_ten[i] for i in range(10)}

    return {"results": results}


model, current_data = setup()

if __name__ == "__main__":
    uvicorn.run(app, port=8500)
