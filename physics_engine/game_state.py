"""
Game state module for managing the game state and logic.
"""
from typing import Dict, List, Optional, Tuple
import time
import math
from physics_engine.position import Position
from physics_engine.physics import PhysicsEngine
from config.game_config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE,
    SHIELD_DURATION, INITIAL_LIFES, LASER_SPEED,
    WALLS, MINES, FLASH_DURATION, GRID_WIDTH, GRID_HEIGHT
)
from entities.spaceship import Spaceship
from entities.laser import Laser
from entities.mine import Mine

class GameState:
    """Manages the game state and logic."""
    
    def __init__(self):
        """Initialize game state."""
        self.last_time = time.time()
        self.physics_engine = PhysicsEngine(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
        self.players: Dict[str, Spaceship] = {}
        self.is_flashing = False
        self.flash_start_time = 0
        self.reset()
        
    def reset(self):
        """Reset game state to initial values."""
        self.last_time = time.time()
        self.game_over = False
        self.lasers: List[Laser] = []
        self.mines = [Mine(Position(x, y), CELL_SIZE) for x, y in MINES]
        self.walls = [Position(x, y) for x, y in WALLS]
        self.players.clear()
        self.is_flashing = False
        self.flash_start_time = 0
        
    def add_player(self, player_id: str, name: str = None) -> bool:
        """Add a new player to the game."""
        if player_id in self.players:
            return False
            
        # Calculate center of the screen in grid coordinates
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        
        # Define spawn positions around the center
        spawn_positions = [
            (center_x, center_y),      # Center
            (center_x + 3, center_y),  # Right of center
            (center_x - 3, center_y),  # Left of center
            (center_x, center_y + 3)   # Below center
        ]
        
        # Find first available spawn position
        spawn_pos = None
        for pos in spawn_positions:
            # Check if position is valid and not occupied
            if (self.physics_engine.is_valid_move(Position(pos[0], pos[1]), self.walls) and
                not any(p.position.x == pos[0] and p.position.y == pos[1] for p in self.players.values())):
                spawn_pos = pos
                break
        
        if spawn_pos is None:
            return False  # No valid spawn position found
            
        # Create new player at the chosen spawn position
        player = Spaceship(CELL_SIZE, name)
        player.position = Position(spawn_pos[0], spawn_pos[1])
        player.lifes = INITIAL_LIFES
        player.shield_available = True
        player.shield_used = False  # Track if shield has been used
        player.id = player_id
        
        # Set default name if none provided
        if not player.name:
            player_count = len(self.players) + 1
            player.name = f"Player {player_count}"
            
        self.players[player_id] = player
        return True
        
    def remove_player(self, player_id: str) -> bool:
        """Remove a player from the game."""
        if player_id not in self.players:
            return False
        del self.players[player_id]
        return True
        
    def update(self, dt: float):
        """Update game state."""
        if self.game_over:
            return
            
        # Update lasers
        for laser in self.lasers[:]:
            if not laser.active:
                self.lasers.remove(laser)
                continue
                
            # Update laser position
            if not self.physics_engine.update_laser_position(laser, dt):
                laser.active = False
                continue
                
            # Check for collisions
            if self.physics_engine.check_wall_collision(laser.position, self.walls):
                laser.active = False
                continue
                
            # Check for mine collisions
            for mine in self.mines[:]:
                if self.physics_engine.check_mine_collision(laser.position, mine.position):
                    self.mines.remove(mine)
                    laser.active = False
                    break
                    
        # Update players
        for player in self.players.values():
            if player.shield_active and time.time() - player.shield_start_time > SHIELD_DURATION:
                player.shield_active = False
        
        # Update flash effect
        if self.is_flashing and time.time() - self.flash_start_time > FLASH_DURATION:
            self.is_flashing = False
        
        # Check player collisions
        self._check_collisions()
        
    def _check_collisions(self):
        """Check for collisions between players and other objects."""
        for player in self.players.values():
            if not player.active:
                continue
                
            # Check mine collisions
            for mine in self.mines[:]:
                if self.physics_engine.check_mine_collision(player.position, mine.position):
                    if not player.shield_active:
                        player.lifes -= 3  # Lose 3 lifes when hitting a mine
                        if player.lifes <= 0:
                            player.active = False
                        self.is_flashing = True
                        self.flash_start_time = time.time()
                    self.mines.remove(mine)
                    break
                    
            # Check laser collisions
            for laser in self.lasers[:]:
                if (laser.active and 
                    laser.owner_id != player.id and 
                    self.physics_engine.check_laser_collision(laser.position, player.position)):
                    if not player.shield_active:
                        player.lifes -= 1  # Lose 1 life when hit by laser
                        if player.lifes <= 0:
                            player.active = False
                        self.is_flashing = True
                        self.flash_start_time = time.time()
                    laser.active = False
                    break
                    
    def activate_shield(self, player_id: str) -> bool:
        """Activate shield for a player."""
        player = self.players.get(player_id)
        if not player or not player.shield_available or player.shield_used:
            return False
            
        player.shield_active = True
        player.shield_available = False
        player.shield_used = True  # Mark shield as used
        player.shield_start_time = time.time()
        return True
        
    def move_player(self, player_id: str) -> bool:
        """Move a player forward in their current direction."""
        player = self.players.get(player_id)
        if not player or not player.active:
            return False
            
        # Calculate new position based on player's rotation
        direction = player.get_direction_vector()
        new_position = Position(
            int(player.position.x + direction.x),
            int(player.position.y + direction.y)
        )
            
        # Check if move is valid
        if self.physics_engine.is_valid_move(new_position, self.walls):
            player.position = new_position
            return True
        return False
        
    def fire_laser(self, player_id: str) -> bool:
        """Fire a laser from a player."""
        player = self.players.get(player_id)
        if not player or not player.active:
            return False
            
        # Calculate laser direction based on player's rotation
        angle = math.radians(player.rotation)
        direction = Position(
            round(math.sin(angle)),  # Use sin for x to match game's coordinate system
            -round(math.cos(angle))  # Negative cos for y because y increases downward
        )
        
        # Create new laser
        laser = Laser(player.position, direction, CELL_SIZE, player_id)
        self.lasers.append(laser)
        return True
        
    def rotate_player(self, player_id: str, direction: str) -> bool:
        """Rotate a player in the specified direction."""
        player = self.players.get(player_id)
        if not player or not player.active:
            return False
            
        if direction == "right":
            player.rotation = (player.rotation + 90) % 360
        elif direction == "left":
            player.rotation = (player.rotation - 90) % 360
        else:
            return False
            
        return True
        
    def get_player_state(self) -> Dict:
        """Get the current state of all players."""
        return {
            'players': {pid: {
                'position': [p.position.x, p.position.y],
                'rotation': p.rotation,
                'lifes': p.lifes,
                'shield_active': p.shield_active,
                'shield_available': p.shield_available,
                'active': p.active,
                'name': p.name
            } for pid, p in self.players.items()}
        }

    def get_environment_state(self) -> Dict:
        """Get the current state of the game environment."""
        # Get positions relative to each player and only within 5 block radius
        environment_states = {}
        for player_id, player in self.players.items():
            walls_relative = []
            mines_relative = []
            lasers_relative = []
            
            # Calculate relative positions for walls within radius
            for wall in self.walls:
                dx = wall.x - player.position.x
                dy = wall.y - player.position.y
                if abs(dx) <= 5 and abs(dy) <= 5:
                    walls_relative.append([dx, dy])
                    
            # Calculate relative positions for mines within radius    
            for mine in self.mines:
                dx = mine.position.x - player.position.x
                dy = mine.position.y - player.position.y
                if abs(dx) <= 5 and abs(dy) <= 5:
                    mines_relative.append([dx, dy])
                    
            # Calculate relative positions for lasers within radius
            for laser in self.lasers:
                dx = laser.position.x - player.position.x
                dy = laser.position.y - player.position.y
                if abs(dx) <= 5 and abs(dy) <= 5:
                    lasers_relative.append([dx, dy])
                    
            environment_states[player_id] = {
                'walls': walls_relative,
                'mines': mines_relative, 
                'lasers': lasers_relative,
                'game_over': self.game_over
            }
            
        return environment_states

    def get_state(self) -> Dict:
        """Get the complete game state combining player and environment state.
        This method is maintained for backward compatibility with existing agents."""
        return {
            **self.get_player_state(),
            **self.get_environment_state()
        }
