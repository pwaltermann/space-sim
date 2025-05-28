"""
Renderer module for handling all visualization aspects of the game.
"""
import pygame
import os
import time
from typing import List, Dict, Tuple
from physics_engine.position import Position
from physics_engine.game_state import GameState
from config.game_config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE,
    BLACK, WHITE, GRAY, BLUE, RED,
    FPS, SHIELD_DURATION, FLASH_DURATION,
    PLAYER_CIRCLE_RADIUS_FACTOR, SHIELD_RADIUS_FACTOR,
    UI_CIRCLE_RADIUS, TRANSPARENCY_ALPHA
)

# Player colors
PLAYER_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0)   # Yellow
]

class GameRenderer:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Game")
        
        # Load and scale background
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load and scale mine image
        self.mine_image = pygame.image.load("assets/mine.png")
        self.mine_image = pygame.transform.scale(self.mine_image, (CELL_SIZE, CELL_SIZE))
        
        # Load and scale spaceship image
        self.spaceship_image = pygame.image.load("assets/spaceship.png")
        self.spaceship_image = pygame.transform.scale(self.spaceship_image, (CELL_SIZE, CELL_SIZE))
        
        # Load and scale rock image for walls
        self.rock_image = pygame.image.load("assets/rock.png")
        self.rock_image = pygame.transform.scale(self.rock_image, (CELL_SIZE, CELL_SIZE))
        
        # Initialize fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Track player colors
        self.player_colors = {}

    def render(self):
        """Render the current game state."""
        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw walls
        self._render_walls()

        # Draw mines
        self._render_mines()

        # Draw lasers
        self._render_lasers()

        # Draw players and their shields
        self._render_players()

        # Draw flash effect
        if self.game_state.is_flashing:
            self._render_flash()

        # Draw UI
        self._render_ui()

        # Update display
        pygame.display.flip()

    def _render_walls(self):
        """Render the walls."""
        # First render a black background for the score area (first row)
        pygame.draw.rect(
            self.screen,
            BLACK,
            (0, 0, SCREEN_WIDTH, CELL_SIZE)
        )
        
        # Then render the walls
        for wall in self.game_state.walls:
            # Draw rock image centered in the cell
            self.screen.blit(
                self.rock_image,
                (wall.x * CELL_SIZE, wall.y * CELL_SIZE)
            )

    def _render_mines(self):
        """Render the mines."""
        for mine in self.game_state.mines:
            if mine.active:
                # Draw mine image centered in the cell
                self.screen.blit(
                    self.mine_image,
                    (mine.position.x * CELL_SIZE, mine.position.y * CELL_SIZE)
                )

    def _render_lasers(self):
        """Render the lasers."""
        for laser in self.game_state.lasers:
            if laser.active:
                # Draw laser with owner's color
                color = self.player_colors.get(laser.owner_id, WHITE)
                pygame.draw.line(
                    self.screen,
                    color,
                    (laser.position.x * CELL_SIZE + CELL_SIZE // 2,
                     laser.position.y * CELL_SIZE + CELL_SIZE // 2),
                    ((laser.position.x + laser.direction.x) * CELL_SIZE + CELL_SIZE // 2,
                     (laser.position.y + laser.direction.y) * CELL_SIZE + CELL_SIZE // 2),
                    2
                )

    def _render_players(self):
        """Render all players and their shields."""
        # Update player colors if needed
        for i, (player_id, player) in enumerate(self.game_state.players.items()):
            if player_id not in self.player_colors:
                self.player_colors[player_id] = PLAYER_COLORS[i % len(PLAYER_COLORS)]
        
        for player_id, player in self.game_state.players.items():
            if not player.active:
                continue
                
            x = player.position.x * CELL_SIZE + CELL_SIZE // 2
            y = player.position.y * CELL_SIZE + CELL_SIZE // 2
            
            # Draw colored circle for player identification
            color = self.player_colors.get(player_id, WHITE)
            circle_radius = int(CELL_SIZE * PLAYER_CIRCLE_RADIUS_FACTOR)
            circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*color, TRANSPARENCY_ALPHA), (circle_radius, circle_radius), circle_radius)
            self.screen.blit(circle_surface, (x - circle_radius, y - circle_radius))
            
            # Draw shield if active
            if player.shield_active:
                shield_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                shield_radius = int(SHIELD_RADIUS_FACTOR * CELL_SIZE)
                pygame.draw.circle(
                    shield_surface,
                    (*BLUE, TRANSPARENCY_ALPHA),
                    (x, y),
                    shield_radius
                )
                self.screen.blit(shield_surface, (0, 0))
            
            # Draw spaceship image
            rotated_image = pygame.transform.rotate(self.spaceship_image, -player.rotation)
            rect = rotated_image.get_rect(center=(x, y))
            self.screen.blit(rotated_image, rect)

    def _render_flash(self):
        """Render the flash effect."""
        # Create a semi-transparent red overlay
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash_surface.fill((*RED, 128))  # Red with 50% transparency
        self.screen.blit(flash_surface, (0, 0))

    def _get_remaining_time(self) -> str:
        """Calculate and format the remaining game time."""
        if self.game_state.game_start_time is None:
            return "2:00"
            
        elapsed_time = time.time() - self.game_state.game_start_time
        remaining_time = max(0, self.game_state.GAME_TIME_LIMIT - elapsed_time)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        return f"{minutes}:{seconds:02d}"

    def _render_ui(self):
        """Render the UI elements."""
        # Draw black background for score area
        pygame.draw.rect(
            self.screen,
            BLACK,
            (0, 0, SCREEN_WIDTH, CELL_SIZE)
        )
        
        # Calculate total width needed for all player info
        total_width = 0
        player_info = []
        for player_id, player in self.game_state.players.items():
            color = self.player_colors.get(player_id, WHITE)
            name_text = self.font.render(player.name, True, color)
            lifes_text = self.font.render(f"Lifes: {player.lifes}", True, color)
            width = UI_CIRCLE_RADIUS * 2 + name_text.get_width() + lifes_text.get_width() + 20
            player_info.append((player_id, player, color, name_text, lifes_text, width))
            total_width += width
        
        # Calculate starting x position to center everything
        x_offset = (SCREEN_WIDTH - total_width) // 2
        
        # Draw player info
        for player_id, player, color, name_text, lifes_text, width in player_info:
            # Draw player identifier circle
            pygame.draw.circle(
                self.screen,
                color,
                (x_offset + UI_CIRCLE_RADIUS, CELL_SIZE // 2),
                UI_CIRCLE_RADIUS
            )
            
            # Draw player name and lifes
            self.screen.blit(name_text, (x_offset + UI_CIRCLE_RADIUS * 2 + 10, 5))
            self.screen.blit(lifes_text, (x_offset + UI_CIRCLE_RADIUS * 2 + name_text.get_width() + 20, 5))
            x_offset += width
            
        # Draw time counter in top right corner
        time_text = self.font.render(self._get_remaining_time(), True, WHITE)
        time_x = SCREEN_WIDTH - time_text.get_width() - 20  # 20 pixels padding from right edge
        self.screen.blit(time_text, (time_x, 5))

        # Draw game over message
        if self.game_state.game_over:
            text = self.font.render("Game Over!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect) 