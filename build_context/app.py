import json

import joblib
import pandas as pd
from fastapi import FastAPI, Request

model = joblib.load("model.joblib")
with open("feature_columns.json") as handle:
    feature_columns = json.load(handle)

app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/v1/models/{model_name}:predict")
async def predict(model_name: str, request: Request):
    payload = await request.json()
    frame = pd.DataFrame(payload["instances"])
    for column in feature_columns:
        if column not in frame.columns:
            frame[column] = 0
    frame = frame[feature_columns]
    predictions = model.predict(frame).tolist()
    return {"predictions": predictions}
