from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from sim.traffic_env import TrafficEnvironment

import pickle
import os

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI()

# -----------------------------------
# Load RL Policy
# -----------------------------------

policy_path = "policies/policy_v1.pkl"

if os.path.exists(policy_path):

    q_table = pickle.load(open(policy_path, "rb"))

else:

    q_table = {}

# -----------------------------------
# Environment
# -----------------------------------

env = TrafficEnvironment()

# -----------------------------------
# Frontend Files
# -----------------------------------

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# -----------------------------------
# Request Model
# -----------------------------------

class ActionRequest(BaseModel):
    action: int

# -----------------------------------
# Homepage
# -----------------------------------

@app.get("/")
def home():

    return FileResponse("frontend/index.html")

# -----------------------------------
# Current State
# -----------------------------------

@app.get("/state")
def get_state():

    return {
        "queues": env.queues,
        "phase": env.phase,
        "state": env.get_state()
    }

# -----------------------------------
# Manual Control
# -----------------------------------

@app.post("/step")
def step(data: ActionRequest):

    next_state, reward = env.step(data.action)

    return {
        "next_state": next_state,
        "reward": reward,
        "queues": env.queues,
        "phase": env.phase
    }

# -----------------------------------
# RL Auto Control
# -----------------------------------

@app.get("/auto")
def auto_step():

    state = env.get_state()

    if state in q_table:

        action = int(q_table[state].argmax())

    else:

        action = 0

    next_state, reward = env.step(action)

    return {
        "action": action,
        "reward": reward,
        "queues": env.queues,
        "phase": env.phase,
        "next_state": next_state
    }

# -----------------------------------
# Reset Environment
# -----------------------------------

@app.post("/reset")
def reset_env():

    env.reset()

    return {
        "message": "Environment Reset",
        "queues": env.queues,
        "phase": env.phase,
        "reward": 0
    }