from fastapi import FastAPI
import uvicorn
from scripts.preprocess import hello_world

app = FastAPI()


@app.get('/')
def hello():
    return hello_world()


@app.get('/predict')
def get_predictions():
    return {"result": "OMG Predictions!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8500)
