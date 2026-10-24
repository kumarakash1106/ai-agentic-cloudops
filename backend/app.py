from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.graph import investigate
from backend.agents.state import IncidentState

app = FastAPI(
    title="AI Agentic CloudOps",
    description="An AI-powered incident investigation assistant",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class IncidentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10, max_length=2000)
    service: str = Field(min_length=2, max_length=100)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "AI Agentic CloudOps backend is running!"
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Agentic CloudOps!",
        "next_step": "Submit an incident for investigation."
    }


@app.post("/incidents/investigate")
def investigate_incident(incident: IncidentRequest):
    state: IncidentState = {
        "title": incident.title,
        "description": incident.description,
        "service": incident.service,
        "evidence": [],
        "runbooks": [],
        "status": "received"
    }

    return investigate(state)
