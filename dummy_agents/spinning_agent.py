"""
Example of a slow-moving agent that moves in a single direction until hitting a wall,
then turns 90 degrees clockwise and continues moving.
"""
import requests
import time
import signal
import sys
from typing import Optional
from requests.exceptions import RequestException

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
MOVE_DELAY = 0.5  # seconds between moves
FIRE_DELAY = 2.0  # seconds between shots
RATE_LIMIT_DELAY = 0.6  # seconds to wait after rate limit (slightly more than 0.5 to ensure we're under limit)

class SpinningAgent:
    def __init__(self, player_id: str = "player1"):
        """Initialize the agent with a player ID."""
        self.player_id = "spinnin"
        self.name = "Spinnin"  # Updated name
        self.base_url = "http://127.0.0.1:8000"
        self.registered = False
        self.last_fire_time = 0
        self.last_move_time = 0
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
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and retry:  # Rate limit exceeded
                    print(f"Rate limit exceeded, waiting {RATE_LIMIT_DELAY} seconds...")
                    time.sleep(RATE_LIMIT_DELAY)
                    continue
                print(f"HTTP error: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                return None
            except RequestException as e:
                print(f"Request failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                return None
                
        return None
        
    def register(self) -> bool:
        """Register the agent with the game server."""
        response = self._make_request("POST", "register", {"player_id": self.player_id, "name": self.name})
        if response:
            self.registered = True
            print(f"Successfully registered as {self.name}")
            return True
        return False
        
    def unregister(self):
        """Unregister the agent from the game server."""
        if self.registered:
            self._make_request("POST", "unregister", {"player_id": self.player_id})
            self.registered = False
            print(f"Unregistered {self.name}")
                
    def get_state(self) -> Optional[dict]:
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
            
    def move(self) -> bool:
        """Move the agent forward in its current direction."""
        current_time = time.time()
        if current_time - self.last_move_time < MOVE_DELAY:
            return False
            
        response = self._make_request("POST", "move", {"player_id": self.player_id})
        if response:
            self.last_move_time = current_time
            return True
        return False
            
    def rotate(self, direction: str) -> bool:
        """Rotate the agent in the specified direction."""
        response = self._make_request("POST", "rotate", {"player_id": self.player_id, "direction": direction})
        return response is not None
            
    def fire(self) -> bool:
        """Fire a laser."""
        current_time = time.time()
        if current_time - self.last_fire_time < FIRE_DELAY:
            return False
            
        response = self._make_request("POST", "fire", {"player_id": self.player_id})
        if response:
            self.last_fire_time = current_time
            return True
        return False
            
    def activate_shield(self) -> bool:
        """Activate the shield."""
        response = self._make_request("POST", "shield", {"player_id": self.player_id})
        return response is not None

def main():
    """Main function to run the agent."""
    # Create and register the agent
    agent = SpinningAgent()
    
    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down agent...")
        agent.unregister()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # Register the agent
    if not agent.register():
        print("Failed to register agent. Exiting...")
        return
        
    print("Agent registered successfully. Press Ctrl+C to exit.")
    print("Moving in a single direction until hitting a wall, then turning 90 degrees clockwise.")
    print("Firing laser every 2 seconds.")
    
    try:
        while True:
            # Try to move forward
            if not agent.move():
                # If move failed (hit wall), rotate 90 degrees clockwise
                agent.rotate("right")
                
            # Fire laser periodically
            agent.fire()
            
            # Small delay to prevent overwhelming the server
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down agent...")
    finally:
        agent.unregister()

if __name__ == "__main__":
    main() 