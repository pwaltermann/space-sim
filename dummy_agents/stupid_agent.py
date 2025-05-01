"""
Example aggressive agent for the space simulation game API.
"""
import requests
import time
import json
import math
from requests.exceptions import RequestException
from typing import Dict, List, Tuple, Optional
import sys

API_BASE_URL = "http://127.0.0.1:8000"
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
FIRE_INTERVAL = 2  # seconds

class GameAgent:
    """Simple agent that follows walls and fires periodically."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the agent."""
        self.base_url = base_url
        self.player_id = "stupid"
        self.name = "Stupid"  # Changed to "Stupid"
        self.last_action_time = 0
        self.action_delay = 0.1  # Minimum time between actions
        self.last_fire_time = 0
        self.current_direction = "right"  # Start moving right
        
    def register(self) -> bool:
        """Register the agent with the game server."""
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={"player_id": self.player_id, "name": self.name}
            )
            response.raise_for_status()
            print(f"Registered with ID: {self.player_id}")
            return True
        except requests.RequestException as e:
            print(f"Failed to register: {e}")
            return False
            
    def unregister(self) -> bool:
        """Unregister the agent from the game server."""
        if not self.player_id:
            return True
            
        try:
            response = requests.post(f"{API_BASE_URL}/unregister", json={"player_id": self.player_id})
            response.raise_for_status()
            print("Unregistered successfully")
            return True
        except requests.RequestException as e:
            print(f"Failed to unregister: {e}")
            return False
            
    def get_state(self) -> Optional[Dict]:
        """Get the current game state."""
        try:
            response = requests.get(f"{API_BASE_URL}/state")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to get state: {e}")
            return None
            
    def move(self, direction: str) -> bool:
        """Move the agent in the specified direction."""
        if not self.player_id:
            return False
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/move",
                json={"player_id": self.player_id, "direction": direction}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to move: {e}")
            return False
            
    def rotate(self, direction: str) -> bool:
        """Rotate the agent by the specified direction."""
        if not self.player_id:
            return False
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/rotate",
                json={"player_id": self.player_id, "direction": direction}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to rotate: {e}")
            return False
            
    def fire(self) -> bool:
        """Fire a laser."""
        if not self.player_id:
            return False
            
        try:
            response = requests.post(
                f"{API_BASE_URL}/fire",
                json={"player_id": self.player_id}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to fire: {e}")
            return False
            
    def step(self) -> bool:
        """Execute one step of the agent's behavior."""
        state = self.get_state()
        if not state:
            return False
            
        # Get current player state
        player_state = state["players"].get(self.player_id)
        if not player_state:
            return False
            
        # Check if we need to fire
        current_time = time.time()
        if current_time - self.last_fire_time >= FIRE_INTERVAL:
            self.fire()
            self.last_fire_time = current_time
            
        # Try to move in current direction
        if not self.move(self.current_direction):
            # If move failed (hit wall), rotate 90 degrees clockwise
            self.rotate("right")
            # Update direction based on new rotation
            if self.current_direction == "right":
                self.current_direction = "down"
            elif self.current_direction == "down":
                self.current_direction = "left"
            elif self.current_direction == "left":
                self.current_direction = "up"
            else:  # up
                self.current_direction = "right"
                
        return True

def main():
    """Main function to run the agent."""
    agent = GameAgent()
    
    # Register with retries
    for attempt in range(MAX_RETRIES):
        print(f"Attempting to register (attempt {attempt + 1}/{MAX_RETRIES})...")
        if agent.register():
            break
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)
    else:
        print("Failed to register after maximum retries")
        return
        
    try:
        print("Agent started. Press Ctrl+C to quit.")
        while True:
            if not agent.step():
                print("Step failed, stopping agent")
                break
                
            time.sleep(0.1)  # Small delay to prevent overwhelming the server
            
    except KeyboardInterrupt:
        print("\nStopping agent...")
    finally:
        agent.unregister()

if __name__ == "__main__":
    main() 