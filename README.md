# Space Simulation Game

A 2D simulation game featuring spaceships navigating through a world with walls, controlled via agents on  REST API. The game supports up to 4 agents with different behaviors.

## Features

- 2D grid-based world with walls
- Spaceship controlled by REST API
- Multiple agents with different behaviors can play against each other
- REST API for world state and movement control
- Collision detection with walls and other entities
- Shield system for protection
- Mine and laser hazards
- Player names in scoreboard


## Project Structure

Responsibility: Philipp Gallé
- `physics_engine/`: Core game physics and state management
  - `game_state.py`: Manages game state, collisions and player actions
  - `physics.py`: Physics engine for collision detection and movement validation
  - `position.py`: Position class for coordinate handling


Responsibility: Michael Sanin
- `visualization/`: Game rendering and visualization
  - `renderer.py`: Game visualization and rendering of game state
- `entities/`: Game entities (spaceships, lasers, mines)
  - `spaceship.py`: Spaceship entity with movement and combat capabilities
  - `mine.py`: Mine entity with collision detection
  - `laser.py`: Laser projectile entity with movement and collision


Responsibility: Philipp Waltermann
- `api/`: REST API server and routes
  - `routes.py`: FastAPI routes for player registration and game actions
- `assets/`: Game assets (images, etc.)
- `config/`: Game configuration and constants
  - `game_config.py`: Core game settings and parameters
- `dummy_agents/`: AI agents with different behaviors
  - `stupid_agent.py`: Random movement agent
  - `spinning_agent.py`: Wall-following agent

- `main.py`: Game initialization and main loop


## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the game and API server:
```bash
python main.py
```

2. Run individual agents:
```bash
python dummy_agents/stupid_agent.py
python dummy_agents/spinning_agent.py

```

## Game Rules

1. **Movement**:
   - Grid-based movement
   - Cannot move through walls
   - Rotation in 90-degree increments

2. **Combat**:
   - Lasers move in straight lines
   - Lasers disappear on wall impact
   - Players lose 1 life when hit by a laser
   - Players lose 3 lives when hit by a mine

3. **Shield**:
   - Provides temporary protection for 3 seconds
   - Can only be activated once per player in the game
   - Protects against both laser and mine damage

4. **Game Over**:
   - When a player loses all lives
   - Can be restarted with new players



## API Documentation

### Endpoints

#### Register Player
- **POST** `/register`
- **Request Body**:
  ```json
  {
    "player_id": "string",
    "name": "string"  // Optional. If not provided, will be set to "Player N" where N is the player number
  }
  ```
- **Response**: Game state object

#### Unregister Player
- **POST** `/unregister`
- **Request Body**:
  ```json
  {
    "player_id": "string"
  }
  ```
- **Response**: Game state object

#### Get Game State
- **GET** `/state`
- **Response**:
  ```json
  {
    "players": {
      "player_id": {
        "position": [x, y],
        "rotation": number,
        "lifes": number,
        "shield_active": boolean,
        "active": boolean
      }
    },
    "walls": [[x, y], ...],
    "mines": [[x, y], ...],
    "lasers": [[x, y], ...],
    "game_over": boolean
  }
  ```

#### Move Player
- **POST** `/move`
- **Request Body**:
  ```json
  {
    "player_id": "string"
  }
  ```
- **Response**: Game state object

#### Rotate Player
- **POST** `/rotate`
- **Request Body**:
  ```json
  {
    "player_id": "string",
    "direction": "left" | "right"
  }
  ```
- **Response**: Game state object

#### Fire Laser
- **POST** `/fire`
- **Request Body**:
  ```json
  {
    "player_id": "string"
  }
  ```
- **Response**: Game state object

#### Activate Shield
- **POST** `/shield`
- **Request Body**:
  ```json
  {
    "player_id": "string"
  }
  ```
- **Response**: Game state object


