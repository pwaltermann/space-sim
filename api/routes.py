"""
FastAPI routes for the space simulation game.
"""
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Literal, Dict, Optional
from physics_engine.game_state import GameState
import time
from collections import defaultdict

# Rate limiting configuration
RATE_LIMIT = 5  # requests per second
RATE_WINDOW = 1.0  # time window in seconds

class MoveRequest(BaseModel):
    player_id: str

class RotateRequest(BaseModel):
    player_id: str
    direction: str  # "left" or "right"

class FireRequest(BaseModel):
    player_id: str

class ShieldRequest(BaseModel):
    player_id: str

class RegisterRequest(BaseModel):
    player_id: str
    name: Optional[str] = None

def create_app(game_state: GameState) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Space Simulation API")
    
    # Rate limiting storage
    request_timestamps = defaultdict(list)
    
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        """Middleware to enforce rate limiting per player."""
        # Get player_id from request
        player_id = None
        if request.method == "GET":
            player_id = request.query_params.get("player_id")
        else:
            try:
                body = await request.json()
                player_id = body.get("player_id")
            except:
                pass
                
        if player_id:
            # Clean old timestamps
            current_time = time.time()
            request_timestamps[player_id] = [
                ts for ts in request_timestamps[player_id]
                if current_time - ts < RATE_WINDOW
            ]
            
            # Check if rate limit exceeded
            if len(request_timestamps[player_id]) >= RATE_LIMIT:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Maximum {RATE_LIMIT} requests per second."
                )
                
            # Add current timestamp
            request_timestamps[player_id].append(current_time)
            
        return await call_next(request)

    @app.post("/register")
    async def register_player(request: RegisterRequest) -> Dict:
        """Register a new player."""
        if not game_state.add_player(request.player_id, request.name):
            raise HTTPException(status_code=400, detail="Player already exists")
        return game_state.get_state()

    @app.post("/unregister")
    async def unregister_player(request: RegisterRequest) -> Dict:
        """Unregister a player."""
        game_state.remove_player(request.player_id)
        return {"success": True, "state": game_state.get_state()}

    @app.get("/state")
    async def get_state() -> Dict:
        """Get the complete game state (maintained for backward compatibility)."""
        return game_state.get_state()

    @app.get("/player_state")
    async def get_player_state() -> Dict:
        """Get the current state of all players."""
        return game_state.get_player_state()

    @app.get("/environment_state") 
    async def get_environment_state() -> Dict:
        """Get the current state of the game environment."""
        return game_state.get_environment_state()

    @app.post("/move")
    async def move_player(request: MoveRequest) -> Dict:
        """Move a player in the specified direction."""
        if not game_state.move_player(request.player_id):
            raise HTTPException(status_code=400, detail="Invalid move")
        return game_state.get_state()

    @app.post("/rotate")
    async def rotate_player(request: RotateRequest) -> Dict:
        """Rotate a player in the specified direction."""
        if request.direction not in ["left", "right"]:
            raise HTTPException(status_code=400, detail="Invalid rotation direction")
        if not game_state.rotate_player(request.player_id, request.direction):
            raise HTTPException(status_code=400, detail="Invalid rotation")
        return game_state.get_state()

    @app.post("/fire")
    async def fire_laser(request: FireRequest) -> Dict:
        """Fire a laser from a player."""
        if not game_state.fire_laser(request.player_id):
            raise HTTPException(status_code=400, detail="Cannot fire")
        return game_state.get_state()

    @app.post("/shield")
    async def activate_shield(request: ShieldRequest) -> Dict:
        """Activate shield for a player."""
        if not game_state.activate_shield(request.player_id):
            raise HTTPException(status_code=400, detail="Cannot activate shield")
        return game_state.get_state()

    return app 