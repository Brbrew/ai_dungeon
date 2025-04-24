from fastapi import FastAPI, HTTPException, Request, Response, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Optional, Any
import uuid
import os
import json
import nltk
from pathlib import Path
from uuid import UUID

from src.dungeon.models.dungeon import Dungeon
from src.dungeon.models.map import Map
from src.dungeon.models.room import Room
from src.dungeon.models.direction import Direction

# Download NLTK data
try:
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print("NLTK averaged_perceptron_tagger downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Dungeon Game API",
    description="API for a multi-user dungeon game with session management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/dungeon/api/static"), name="static")
#app.mount("/static/dungeon", StaticFiles(directory="src/dungeon/api/static"), name="static")


# Initialize templates
templates = Jinja2Templates(directory="src/dungeon/api/templates")

# In-memory storage for sessions
sessions: Dict[str, Dict] = {}

class CommandRequest(BaseModel):
    """Request model for command parsing."""
    command: str
    
    class Config:
        schema_extra = {
            "example": {
                "command": "look around"
            }
        }

class DungeonResponse(BaseModel):
    """Response model for dungeon data."""
    id: str
    name: str
    description: str
    session_id: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Player's Dungeon",
                "description": "A dungeon created for Player",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }

class MessageResponse(BaseModel):
    """Response model for message endpoints."""
    message: str
    room_img: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

class MapLoadResponse(BaseModel):
    """Response model for map loading."""
    message: str
    room_count: int
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Map loaded successfully",
                "room_count": 15
            }
        }

@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def root(request: Request):
    """Root endpoint that redirects to login if no session exists.
    
    Returns:
        HTMLResponse: The login page HTML
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", tags=["Authentication"])
async def login(request: Request, username: str = Form(...)):
    """Handle user login and create a new session with dungeon.
    
    Args:
        request: The FastAPI request object
        username: The username provided in the form
        
    Returns:
        RedirectResponse: Redirects to the game page with a session cookie
        
    Raises:
        HTTPException: If username is empty
    """
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    # Generate a new session ID
    session_id = str(uuid.uuid4())
    
    # Create a new dungeon for this session
    dungeon = Dungeon(
        name=f"{username}'s Dungeon",
        description=f"A dungeon created for {username}",
        session_id=session_id
    )
    
    # Debug: Check if the map was loaded correctly
    print(f"DEBUG: Dungeon created for {username}")
    print(f"DEBUG: Map loaded: {dungeon.map is not None}")
    if dungeon.map:
        print(f"DEBUG: Number of rooms in map: {len(dungeon.map.get_all_rooms())}")
        print(f"DEBUG: Current room ID: {dungeon.current_room_id}")
        if dungeon.current_room_id:
            try:
                current_room = dungeon.map.get_room_by_id(UUID(dungeon.current_room_id))
                print(f"DEBUG: Current room name: {current_room.name}")
                print(f"DEBUG: Current room ref_id: {current_room.room_ref_id}")
            except Exception as e:
                print(f"DEBUG: Error getting current room: {e}")
    else:
        print("DEBUG: No map loaded!")
    
    # Store the session
    sessions[session_id] = {
        "username": username,
        "dungeon": dungeon
    }
    
    # Create a response with a redirect to the game page
    response = RedirectResponse(url="/game", status_code=303)
    
    # Set the session cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600  # 1 hour
    )
    
    return response

@app.get("/game", response_class=HTMLResponse, tags=["UI"])
async def game(request: Request):
    """Game page that requires a valid session.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        HTMLResponse: The game page HTML
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/", status_code=303)
    
    # Get the session data
    session_data = sessions[session_id]
    dungeon = session_data["dungeon"]
    username = session_data["username"]
    
    # Get the current room image
    room_img = "/static/img/interface/default_room.webp"
    if dungeon.map and dungeon.current_room_id:
        try:
            current_room = dungeon.map.get_room_by_id(UUID(dungeon.current_room_id))
            if current_room.room_img:
                room_img = current_room.room_img
        except Exception as e:
            print(f"DEBUG: Error getting current room: {e}")
    
    # Debug: Check if the map is still available
    print(f"DEBUG: Game page loaded for {username}")
    print(f"DEBUG: Map loaded: {dungeon.map is not None}")
    if dungeon.map:
        print(f"DEBUG: Number of rooms in map: {len(dungeon.map.get_all_rooms())}")
        print(f"DEBUG: Current room ID: {dungeon.current_room_id}")
        if dungeon.current_room_id:
            try:
                current_room = dungeon.map.get_room_by_id(UUID(dungeon.current_room_id))
                print(f"DEBUG: Current room name: {current_room.name}")
                print(f"DEBUG: Current room ref_id: {current_room.room_ref_id}")
                print(f"DEBUG: Current room image: {current_room.room_img}")
            except Exception as e:
                print(f"DEBUG: Error getting current room: {e}")
    else:
        print("DEBUG: No map loaded!")
    
    return templates.TemplateResponse(
        "game.html", 
        {
            "request": request,
            "username": username,
            "dungeon": dungeon,
            "room_img": room_img
        }
    )

@app.post("/parser/", response_model=MessageResponse, tags=["Game"])
async def parse_command(request: Request, command_request: CommandRequest):
    """Parse a command and return a response.
    
    Args:
        request: The FastAPI request object
        command_request: The command to parse
        
    Returns:
        MessageResponse: The parsed command response
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    result = dungeon.parse_command(command_request.command)
    
    return {
        "message": result.get("message", "Command processed"),
        "room_img": result.get("room_img", "/static/img/interface/default_room.webp")
    }

@app.get("/api/dungeon", response_model=DungeonResponse, tags=["API"])
async def get_dungeon(request: Request):
    """Get the current dungeon data.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        DungeonResponse: The dungeon data
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    return {
        "id": dungeon.id,
        "name": dungeon.name,
        "description": dungeon.description,
        "session_id": dungeon.session_id
    }

@app.post("/api/dungeon/save", response_model=MessageResponse, tags=["API"])
async def save_dungeon(request: Request):
    """Save the current dungeon state.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    dungeon.save()
    return {"message": "Dungeon saved successfully"}

@app.post("/api/dungeon/load", response_model=MessageResponse, tags=["API"])
async def load_dungeon(request: Request):
    """Load a saved dungeon state.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    dungeon.load()
    return {"message": "Dungeon loaded successfully"}

@app.post("/api/dungeon/load-map", response_model=MapLoadResponse, tags=["API"])
async def load_map(request: Request, file: UploadFile = File(...)):
    """Load a map from a JSON file.
    
    Args:
        request: The FastAPI request object
        file: The map file to load
        
    Returns:
        MapLoadResponse: Success message and room count
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    
    # Read the file content
    content = await file.read()
    map_data = json.loads(content)
    
    # Load the map
    dungeon.load_map(map_data)
    
    return {
        "message": "Map loaded successfully",
        "room_count": len(dungeon.map.get_all_rooms())
    }

@app.get("/show_map", response_class=HTMLResponse, tags=["UI"])
async def show_map(request: Request):
    """Show the SVG representation of the current map.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        HTMLResponse: HTML page with the SVG map
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    
    # Get the current room ID from the dungeon and convert it to UUID
    current_room_id = None
    if dungeon.current_room_id:
        try:
            current_room_id = UUID(dungeon.current_room_id)
        except ValueError:
            print(f"DEBUG: Invalid UUID format for current_room_id: {dungeon.current_room_id}")
    
    # Generate the SVG representation of the map
    svg_map = dungeon.map.to_svg(current_room_id=current_room_id)
    
    # Create an HTML page that displays the SVG
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dungeon Map</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f0f0;
            }}
            .container {{
                max-width: 95%;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .map-container {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
                overflow: auto;
                max-height: 80vh;
            }}
            .map-container svg {{
                max-width: 100%;
                height: auto;
            }}
            .back-button {{
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                text-align: center;
                width: 200px;
            }}
            .back-button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Map of {dungeon.scenario.name}</h1>
            <div class="map-container">
                {svg_map}
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/api/map/svg", response_class=HTMLResponse, tags=["API"])
async def get_map_svg(request: Request):
    """Get the SVG representation of the current map.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        HTMLResponse: The SVG content
        
    Raises:
        HTTPException: If no active session
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=404, detail="No active dungeon session")
    
    dungeon = sessions[session_id]["dungeon"]
    
    # Get the current room ID from the dungeon and convert it to UUID
    current_room_id = None
    if dungeon.current_room_id:
        try:
            current_room_id = UUID(dungeon.current_room_id)
        except ValueError:
            print(f"DEBUG: Invalid UUID format for current_room_id: {dungeon.current_room_id}")
    
    # Generate the SVG representation of the map
    svg_map = dungeon.map.to_svg(current_room_id=current_room_id)
    
    return HTMLResponse(content=svg_map) 