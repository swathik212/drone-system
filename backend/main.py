from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import EnvironmentRequest, PathResponse
from algorithms import Environment, search

app = FastAPI(title="Drone Navigation API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/pathfind", response_model=PathResponse)
def pathfind(req: EnvironmentRequest):
    env = Environment(
        bounds=req.bounds,
        start=req.start,
        goal=req.goal,
        obstacles=req.obstacles,
        no_fly_zones=req.no_fly_zones
    )
    result = search(env, req.algorithm)
    return result
