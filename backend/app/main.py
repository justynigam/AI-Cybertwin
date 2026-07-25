"""
FastAPI Main Application entrypoint for CyberTwin AI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.router import api_router

app = FastAPI(
    title="CyberTwin AI Backend",
    description="Autonomous Cyber Digital Twin Threat Detection & Defense System",
    version="1.0.0"
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "CyberTwin AI Threat Intelligence & Digital Twin Defense Engine",
        "version": "1.0.0"
    }
