from fastapi import FastAPI
import json


app = FastAPI(
    title="AgentIT Doctor API",
    version="0.4.0"
)


@app.get("/")
def root():

    return {
        "status": "online",
        "application": "AgentIT Doctor"
    }


@app.get("/diagnosis")
def diagnosis():

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        return json.load(file)
