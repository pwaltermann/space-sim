"""
Main entry point for the space simulation game.
Coordinates the game loop and API server.
"""
import asyncio
import pygame
import uvicorn
import os
import sys
from threading import Thread, Event
import time
import requests

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics_engine.game_state import GameState
from visualization.renderer import GameRenderer
from config.game_config import FPS
from api.routes import create_app

class Game:
    def __init__(self):
        """Initialize the game components."""
        pygame.init()
        self.game_state = GameState()
        self.renderer = GameRenderer(self.game_state)
        self.clock = pygame.time.Clock()
        self.running = True
        self.server_ready = Event()

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def run(self):
        """Main game loop."""
        try:
            while self.running:
                # Calculate delta time
                current_time = time.time()
                dt = current_time - self.game_state.last_time
                self.game_state.last_time = current_time
                
                self.handle_events()
                self.game_state.update(dt)
                self.renderer.render()
                self.clock.tick(FPS)
        except Exception as e:
            print(f"Error in game loop: {e}")
        finally:
            pygame.quit()

def run_api(game_instance):
    """Run the FastAPI server."""
    try:
        app = create_app(game_instance.game_state)
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Error in API server: {e}")

def wait_for_server():
    """Wait for the server to be ready."""
    max_retries = 30  # 30 seconds maximum wait time
    retry_interval = 1  # Check every second
    
    for _ in range(max_retries):
        try:
            response = requests.get("http://127.0.0.1:8000/player_state")
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(retry_interval)
            continue
    
    print("Server failed to start within the timeout period")
    return False

if __name__ == "__main__":
    game = Game()
    
    # Start API server in a separate thread
    api_thread = Thread(target=run_api, args=(game,), daemon=True)
    api_thread.start()
    
    # Wait for server to be ready
    if not wait_for_server():
        print("Exiting due to server initialization failure")
        sys.exit(1)
    
    # Run game loop
    game.run() 