"""
Main entry point for the space simulation game.
Coordinates the game loop and API server.
"""
import asyncio
import pygame
import uvicorn
import os
import sys
from threading import Thread
import time

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

def run_api():
    """Run the FastAPI server."""
    try:
        app = create_app(game.game_state)
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Error in API server: {e}")

if __name__ == "__main__":
    game = Game()
    
    # Start API server in a separate thread
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run game loop
    game.run() 