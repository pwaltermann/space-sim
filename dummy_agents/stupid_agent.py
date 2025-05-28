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
RATE_LIMIT_DELAY = 0.6  # seconds to wait after rate limit (slightly more than 0.5 to ensure we're under limit)
MOVE_DELAY = 0.1  # seconds between moves (reduced from 0.5 to make it faster than spinning agent)

class GameAgent:
    """Simple agent that follows walls and fires periodically."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the agent."""
        self.base_url = base_url
        self.player_id = "stupid"
        self.name = "Stupid"  # Changed to "Stupid"
        self.last_move_time = 0
        self.last_fire_time = 0
        self.current_direction = "right"  # Start moving right
        self.last_request_time = 0  # Track last request time for rate limiting
        
    def _make_request(self, method: str, endpoint: str, json_data: dict = None, retry: bool = True) -> Optional[dict]:
        """Make an API request with rate limit handling and retries."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        # If less than 0.5 seconds since last request, wait
        if time_since_last_request < 0.5:
            time.sleep(0.5 - time_since_last_request)
            
        for attempt in range(MAX_RETRIES):
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}/{endpoint}")
                else:
                    response = requests.post(f"{self.base_url}/{endpoint}", json=json_data)
                    
                response.raise_for_status()
                self.last_request_time = time.time()
                return response.json()
                
            except RequestException as e:
                # Check if we have a response object and if it's a rate limit error
                if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429 and retry:
                    print(f"Rate limit exceeded, waiting {RATE_LIMIT_DELAY} seconds...")
                    time.sleep(RATE_LIMIT_DELAY)
                    continue
                print(f"Request failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                return None
                
        return None
        
    def register(self) -> bool:
        """Register the agent with the game server."""
        response = self._make_request("POST", "register", {"player_id": self.player_id, "name": self.name})
        if response:
            print(f"Registered with ID: {self.player_id}")
            return True
        return False
            
    def unregister(self) -> bool:
        """Unregister the agent from the game server."""
        if not self.player_id:
            return True
            
        response = self._make_request("POST", "unregister", {"player_id": self.player_id})
        if response:
            print("Unregistered successfully")
            return True
        return False
            
    def get_state(self) -> Optional[Dict]:
        """Get the current game state."""
        # Get player state
        player_state = self._make_request("GET", "player_state")
        if not player_state:
            return None
            
        # Get environment state
        env_state = self._make_request("GET", "environment_state")
        if not env_state:
            return None
            
        # Combine states
        return {
            "players": player_state["players"],
            "environment": env_state.get(self.player_id, {})
        }
            
    def move(self, direction: str) -> bool:
        """Move the agent in the specified direction."""
        if not self.player_id:
            return False
            
        current_time = time.time()
        if current_time - self.last_move_time < MOVE_DELAY:
            return False
            
        response = self._make_request("POST", "move", {"player_id": self.player_id, "direction": direction})
        if response:
            self.last_move_time = current_time
            return True
        return False
            
    def rotate(self, direction: str) -> bool:
        """Rotate the agent by the specified direction."""
        if not self.player_id:
            return False
            
        response = self._make_request("POST", "rotate", {"player_id": self.player_id, "direction": direction})
        return response is not None
            
    def fire(self) -> bool:
        """Fire a laser."""
        if not self.player_id:
            return False
            
        current_time = time.time()
        if current_time - self.last_fire_time < FIRE_INTERVAL:
            return False
            
        response = self._make_request("POST", "fire", {"player_id": self.player_id})
        if response:
            self.last_fire_time = current_time
            return True
        return False
            
    def step(self) -> bool:
        """Execute one step of the agent's behavior."""
        # Check if we need to fire
        current_time = time.time()
        if current_time - self.last_fire_time >= FIRE_INTERVAL:
            self.fire()
            
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