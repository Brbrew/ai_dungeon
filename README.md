# Dungeon Game API

A FastAPI-based REST API for a dungeon game system. This API provides endpoints for managing game entities such as characters, maps, rooms, weapons, armor, and more.

## Features

- Theme management (create, list, get themes)
- Room creation and management
- Map creation with room connections
- Character creation and management
- Weapon and armor creation
- Dice rolling functionality
- NPC and enemy creation
- Blackbox endpoints for external service integration
- CORS support for web clients

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the server with:
```bash
uvicorn src.dungeon.api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Endpoints

### Themes
- `POST /themes/` - Create a new theme
- `GET /themes/` - List all themes
- `GET /themes/{theme_id}` - Get a theme by ID

### Rooms
- `POST /rooms/` - Create a new room

### Maps
- `POST /maps/` - Create a new map
- `GET /maps/` - List all maps
- `GET /maps/{map_id}` - Get a map by ID
- `POST /maps/{map_id}/rooms/{room_id}` - Add a room to a map
- `POST /maps/{map_id}/connect` - Connect two rooms in a map

### Characters
- `POST /characters/` - Create a new character
- `GET /characters/` - List all characters
- `GET /characters/{character_id}` - Get a character by ID

### NPCs
- `POST /npcs/` - Create a new NPC
- `GET /npcs/` - List all NPCs
- `GET /npcs/{npc_id}` - Get an NPC by ID

### Enemies
- `POST /enemies/` - Create a new enemy
- `GET /enemies/` - List all enemies
- `GET /enemies/{enemy_id}` - Get an enemy by ID

### Weapons
- `POST /weapons/` - Create a new weapon

### Armor
- `POST /armor/` - Create a new armor

### Dice
- `POST /dice/roll` - Roll dice

### Generation Endpoints
- `POST /generate/room` - Generate a room using an external service
- `POST /generate/npc` - Generate an NPC using an external service
- `POST /generate/enemy` - Generate an enemy using an external service

## Data Models

### Theme
```