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
  - `spinning_agent.py`: Random spinning and moving agent

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

### Rate Limiting

The API implements rate limiting to ensure fair play and prevent server overload:
- Each player is limited to 5 requests per second
- This limit applies to all endpoints (GET and POST requests)
- If the rate limit is exceeded, the API will return a 429 (Too Many Requests) error
- The rate limit is tracked per player_id
- Rate limiting applies to all game actions (move, rotate, fire, shield) and state requests

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

#### Get Player State
- **GET** `/player_state`
- **Response**:
  ```json
  {
    "players": {
      "player_id": {
        "position": [x, y],
        "rotation": number,
        "lifes": number,
        "shield_active": boolean,
        "active": boolean,
        "name": "string"
      }
    }
  }
  ```

#### Get Environment State  
- **GET** `/environment_state`
- **Response**:
  ```json
  {
    "walls": [[x, y], ...],    // Positions relative to player, only within 5 block radius
    "mines": [[x, y], ...],    // Positions relative to player, only within 5 block radius  
    "lasers": [[x, y], ...],   // Positions relative to player, only within 5 block radius
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


