"""Tests for the Map model."""
from decimal import Decimal
import pytest

from dungeon.models.direction import Direction
from dungeon.models.map import Map
from dungeon.models.room import Room
from dungeon.models.theme import Theme

@pytest.fixture
def theme():
    """Create a test theme."""
    return Theme(
        name="Test Theme",
        description="A test theme"
    )

@pytest.fixture
def room1(theme):
    """Create the first test room."""
    return Room(
        description="Room 1",
        theme=theme,
        is_dark=False
    )

@pytest.fixture
def room2(theme):
    """Create the second test room."""
    return Room(
        description="Room 2",
        theme=theme,
        is_dark=True
    )

@pytest.fixture
def room3(theme):
    """Create the third test room."""
    return Room(
        description="Room 3",
        theme=theme,
        is_dark=False
    )

@pytest.fixture
def dungeon_map():
    """Create a test map."""
    return Map()

def test_map_initialization(dungeon_map):
    """Test map initialization."""
    assert dungeon_map.rooms == []

def test_add_remove_room(dungeon_map, room1):
    """Test adding and removing rooms."""
    # Add room
    dungeon_map.add_room(room1)
    assert len(dungeon_map.rooms) == 1
    assert dungeon_map.rooms[0] == room1
    
    # Remove room
    dungeon_map.remove_room(room1.id)
    assert len(dungeon_map.rooms) == 0
    
    # Try to remove non-existent room
    with pytest.raises(KeyError):
        dungeon_map.remove_room(room1.id)

def test_connect_disconnect_rooms(dungeon_map, room1, room2):
    """Test connecting and disconnecting rooms."""
    # Add rooms
    dungeon_map.add_room(room1)
    dungeon_map.add_room(room2)
    
    # Connect rooms
    dungeon_map.connect_rooms(room1, room2, Direction.NORTH)
    
    # Check connections
    assert dungeon_map.get_connected_room(room1, Direction.NORTH) == room2
    assert dungeon_map.get_connected_room(room2, Direction.SOUTH) == room1
    
    # Disconnect rooms
    dungeon_map.disconnect_rooms(room1, room2, Direction.NORTH)
    
    # Check connections are removed
    assert dungeon_map.get_connected_room(room1, Direction.NORTH) is None
    assert dungeon_map.get_connected_room(room2, Direction.SOUTH) is None
    
    # Try to disconnect non-existent connection
    with pytest.raises(KeyError):
        dungeon_map.disconnect_rooms(room1, room2, Direction.NORTH)

def test_get_available_directions(dungeon_map, room1, room2, room3):
    """Test getting available directions."""
    # Add rooms
    dungeon_map.add_room(room1)
    dungeon_map.add_room(room2)
    dungeon_map.add_room(room3)
    
    # Connect rooms
    dungeon_map.connect_rooms(room1, room2, Direction.NORTH)
    dungeon_map.connect_rooms(room1, room3, Direction.EAST)
    
    # Check available directions
    directions = dungeon_map.get_available_directions(room1)
    assert len(directions) == 2
    assert Direction.NORTH in directions
    assert Direction.EAST in directions
    
    # Check room with no connections
    assert dungeon_map.get_available_directions(room3) == [Direction.WEST]

def test_find_path(dungeon_map, room1, room2, room3):
    """Test finding paths between rooms."""
    # Add rooms
    dungeon_map.add_room(room1)
    dungeon_map.add_room(room2)
    dungeon_map.add_room(room3)
    
    # Connect rooms in a chain: room1 -> room2 -> room3
    dungeon_map.connect_rooms(room1, room2, Direction.NORTH)
    dungeon_map.connect_rooms(room2, room3, Direction.EAST)
    
    # Find path from room1 to room3
    path = dungeon_map.find_path(room1, room3)
    assert path is not None
    assert len(path) == 2
    assert path[0] == (room2, Direction.NORTH)
    assert path[1] == (room3, Direction.EAST)
    
    # Find path to disconnected room
    dungeon_map.remove_room(room2)
    assert dungeon_map.find_path(room1, room3) is None

def test_to_dict(dungeon_map, room1, room2):
    """Test map to_dict method."""
    # Add and connect rooms
    dungeon_map.add_room(room1)
    dungeon_map.add_room(room2)
    dungeon_map.connect_rooms(room1, room2, Direction.NORTH)
    
    # Convert to dict
    map_dict = dungeon_map.to_dict()
    
    # Check rooms
    assert len(map_dict["rooms"]) == 2
    
    # Check connections
    assert len(map_dict["connections"]) == 2  # Two-way connection
    
    # Check connection details
    connection = next(
        c for c in map_dict["connections"]
        if c["direction"] == Direction.NORTH.name
    )
    assert connection["source_id"] == str(room1.id)
    assert connection["target_id"] == str(room2.id) 