"""
FastAPI routes for the space simulation game.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Dict, Optional
from physics_engine.game_state import GameState

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
    async def get_game_state() -> Dict:
        """Get the current state of the game."""
        return game_state.get_state()

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