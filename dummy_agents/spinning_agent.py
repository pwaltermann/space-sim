"""
Example of a slow-moving agent that moves in a single direction until hitting a wall,
then turns 90 degrees clockwise and continues moving.
"""
import requests
import time
import signal
import sys
from typing import Optional

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
MOVE_DELAY = 0.5  # seconds between moves
FIRE_DELAY = 2.0  # seconds between shots

class SpinningAgent:
    def __init__(self, player_id: str = "player1"):
        """Initialize the agent with a player ID."""
        self.player_id = "spinnin"
        self.name = "Spinnin"  # Updated name

        self.base_url = "http://127.0.0.1:8000"
        self.registered = False
        self.last_fire_time = 0
        self.last_move_time = 0
        
    def register(self) -> bool:
        """Register the agent with the game server."""
        for attempt in range(MAX_RETRIES):
            try:
                print(f"Registration attempt {attempt + 1}/{MAX_RETRIES}")
                response = requests.post(
                    f"{self.base_url}/register",
                    json={"player_id": self.player_id, "name": self.name}
                )
                response.raise_for_status()
                self.registered = True
                print(f"Successfully registered as {self.name}")
                return True
            except requests.RequestException as e:
                print(f"Registration attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        return False
        
    def unregister(self):
        """Unregister the agent from the game server."""
        if self.registered:
            try:
                requests.post(
                    f"{self.base_url}/unregister",
                    json={"player_id": self.player_id}
                )
                self.registered = False
                print(f"Unregistered {self.name}")
            except requests.RequestException as e:
                print(f"Error unregistering: {e}")
                
    def get_state(self) -> Optional[dict]:
        """Get the current game state."""
        try:
            response = requests.get(f"{self.base_url}/state")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting state: {e}")
            return None
            
    def move(self) -> bool:
        """Move the agent forward in its current direction."""
        current_time = time.time()
        if current_time - self.last_move_time < MOVE_DELAY:
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/move",
                json={"player_id": self.player_id}
            )
            response.raise_for_status()
            self.last_move_time = current_time
            return True
        except requests.RequestException as e:
            print(f"Error moving: {e}")
            return False
            
    def rotate(self, direction: str) -> bool:
        """Rotate the agent in the specified direction."""
        try:
            response = requests.post(
                f"{self.base_url}/rotate",
                json={"player_id": self.player_id, "direction": direction}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error rotating: {e}")
            return False
            
    def fire(self) -> bool:
        """Fire a laser."""
        current_time = time.time()
        if current_time - self.last_fire_time < FIRE_DELAY:
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/fire",
                json={"player_id": self.player_id}
            )
            response.raise_for_status()
            self.last_fire_time = current_time
            return True
        except requests.RequestException as e:
            print(f"Error firing: {e}")
            return False
            
    def activate_shield(self) -> bool:
        """Activate the shield."""
        try:
            response = requests.post(
                f"{self.base_url}/shield",
                json={"player_id": self.player_id}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error activating shield: {e}")
            return False

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