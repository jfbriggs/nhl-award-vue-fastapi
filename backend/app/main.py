from fastapi import FastAPI
import uvicorn
from scripts.preprocess import hello_world, merge_process

app = FastAPI()


@app.get('/')
async def hello():
    return hello_world()


@app.get('/process')
async def process_data():
    src = '../past_data'
    data, encodings = merge_process(src)

    print("Data processed.")
    return {"encodings": encodings}



@app.get('/predict')
async def get_predictions():
    return {"result": "OMG Predictions!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8500)
