from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
def hello():
    return "Yeah, NHL Norris Trophy predictions!"


@app.get('/predict')
def get_predictions():
    return {"result": "OMG Predictions!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8500)
