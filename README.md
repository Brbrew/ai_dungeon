![Dungeon Crawler](/src/dungeon/api/static/img/interface/logo.webp)

# AI Dungeon Crawler

## Goals
The goal of this project is to have a creative way for to learn more complex Python interactions and coding, and more importantly to see how far things can go with AI.

In order to make this project, I had a specific goal in mind, specific interactions and interfaces, and a specific art style I wanted to implement. The game takes it's main insperation from command line games like Zork, layered in with other more modern JRPGs/RPGS. Most of the art, about 60% of the code, and the flavor text has been AI generated, using multiple tools.

The other part of the project is to make it configrable, so any number of "dungeons" can be added based on a JSON template.

## Tools Used:
- MS Co-pilot for the basic art generation (it's suprisingly good for that), along with heavy Photoshop for clean up, up-scaling, and generative-fill (VERY powerful tool.)
- Cursor AI for much of the code base (with signicant changes to clean up things and work appropriately)
- For the flavor text, it's using the deepseek-r1-distill-llama-70b model via [GROQ](https://groq.com/); mainly b/c the API is free...for now.
- The ai_generator.py expects an OS variable GROQ_API_KEY, more on that [here](https://console.groq.com/docs/quickstart).


## Lessons Learned (so far)
AI is an awesome and very powerful tool, however it can only do what you tell it to do, it's not magic. 

## TODO
- Add changelog.md and version control
- Clean up parse_command for futher seperation of concern
- Remove multiple charecters and only have one player charecter
- Add inventory to player charecter
- Modify help to use ENUM classes to build help text
- Move help to modal window
- Add icons under room (Inventory, Map, Help)
- Add doors/path blockers to rooms (door, mud slide, blizzard, etc.)
- Add keys to unlock doors
- Add portals (not drawn on map, but can "warp" to any room)
- Add map validation to check for loop-backs (east-west-east)
- Add containers (can be treasure chests or other things ike wardrobes)
- Add levels to map generator
- Clean up interface
- Add database for session management (e.g. Redis?)
- Add item interactions
- Add NPCs
- Dynamic NPC interaction with AI, like a chat bot with a specific personality, and one that can interact with game elements.
- Add default rooms/images in a template so that new dungeons can be created based on existing art assets.
- Add Items
- Combat
- Add weapons/armor
- Charecter classes
- Music

### Updates


Added additional rooms and map functionality; fixed minor interface issues.
Created a general map navigation and basic classes to be used later. Directions are "North", "South", "East", "West", "Up", and "Down". 
The SVG generator currently only takes cardinal directions, and functionality to add "level" will be added.

# AI Dungeon Crawler API

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