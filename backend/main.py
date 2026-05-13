from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import handle_attack

app = FastAPI(title="SwarmForge API", version="1.0.0")

# Allow requests from any origin (for hackathon demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AttackEvent(BaseModel):
    ip: str = "127.0.0.1"
    type: str = "recon"         # recon / bruteforce / injection
    attempts: int = 1
    details: str = ""
    honeypot_count: int = 3

@app.post("/defend")
async def defend(event: AttackEvent):
    """
    Main defense endpoint.
    Receives attack event data → returns action, result, and explanation.
    """
    return handle_attack(event.dict())

@app.get("/health")
async def health():
    return {"status": "ok", "swarm": "active"}