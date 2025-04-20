"""Tests for the key-related methods in the Map class."""
from uuid import uuid4
import pytest

from dungeon.models.direction import Direction
from dungeon.models.key import Key
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
def locked_room(theme):
    """Create a locked room."""
    return Room(
        description="Locked Room",
        theme=theme,
        is_locked=True
    )

@pytest.fixture
def key_room(theme, locked_room):
    """Create a room containing a key."""
    room = Room(
        description="Room with Key",
        theme=theme
    )
    key = Key(
        name="Test Key",
        description="A test key",
        unlocks_room_id=locked_room.id
    )
    room.add_treasure(key)
    return room

@pytest.fixture
def dungeon_map(locked_room, key_room):
    """Create a test map with locked room and key."""
    map_obj = Map()
    map_obj.add_room(locked_room)
    map_obj.add_room(key_room)
    map_obj.connect_rooms(key_room, locked_room, Direction.NORTH)
    return map_obj

def test_get_locked_rooms(dungeon_map, locked_room):
    """Test getting locked rooms."""
    locked_rooms = dungeon_map.get_locked_rooms()
    assert len(locked_rooms) == 1
    assert locked_rooms[0] == locked_room

def test_find_keys_in_map(dungeon_map, locked_room):
    """Test finding all keys in the map."""
    keys = dungeon_map.find_keys_in_map()
    assert len(keys) == 1
    assert keys[0].can_unlock(locked_room.id)

def test_find_key_for_room(dungeon_map, locked_room, key_room):
    """Test finding a specific key for a room."""
    # Find existing key
    result = dungeon_map.find_key_for_room(locked_room)
    assert result is not None
    containing_room, key = result
    assert containing_room == key_room
    assert key.can_unlock(locked_room.id)
    
    # Try to find non-existent key
    other_room = Room(
        description="Other Room",
        theme=key_room.theme,
        is_locked=True
    )
    dungeon_map.add_room(other_room)
    assert dungeon_map.find_key_for_room(other_room) is None

def test_is_path_accessible(dungeon_map, locked_room, key_room):
    """Test checking if a path is accessible with available keys."""
    # Create a path: key_room -> locked_room -> end_room
    end_room = Room(
        description="End Room",
        theme=key_room.theme
    )
    dungeon_map.add_room(end_room)
    dungeon_map.connect_rooms(locked_room, end_room, Direction.EAST)
    
    # Try without key
    assert not dungeon_map.is_path_accessible(key_room, end_room)
    
    # Try with key
    key = dungeon_map.find_keys_in_map()[0]
    assert dungeon_map.is_path_accessible(key_room, end_room, [key])

def test_find_accessible_path(dungeon_map, locked_room, key_room):
    """Test finding an accessible path with required keys."""
    # Create a path: key_room -> locked_room -> end_room
    end_room = Room(
        description="End Room",
        theme=key_room.theme
    )
    dungeon_map.add_room(end_room)
    dungeon_map.connect_rooms(locked_room, end_room, Direction.EAST)
    
    # Try without key
    assert dungeon_map.find_accessible_path(key_room, end_room) is None
    
    # Try with key
    key = dungeon_map.find_keys_in_map()[0]
    path = dungeon_map.find_accessible_path(key_room, end_room, [key])
    
    assert path is not None
    assert len(path) == 2
    
    # Check first step
    room1, direction1, key1 = path[0]
    assert room1 == locked_room
    assert direction1 == Direction.NORTH
    assert key1 == key
    
    # Check second step
    room2, direction2, key2 = path[1]
    assert room2 == end_room
    assert direction2 == Direction.EAST
    assert key2 is None  # No key needed for unlocked room

def test_complex_path_with_multiple_keys(theme):
    """Test finding a path requiring multiple keys."""
    # Create rooms
    start_room = Room(description="Start", theme=theme)
    middle_room = Room(description="Middle", theme=theme, is_locked=True)
    end_room = Room(description="End", theme=theme, is_locked=True)
    key_room1 = Room(description="Key Room 1", theme=theme)
    key_room2 = Room(description="Key Room 2", theme=theme)
    
    # Create keys
    key1 = Key(
        name="Key 1",
        description="First key",
        unlocks_room_id=middle_room.id
    )
    key2 = Key(
        name="Key 2",
        description="Second key",
        unlocks_room_id=end_room.id
    )
    
    # Add keys to rooms
    key_room1.add_treasure(key1)
    key_room2.add_treasure(key2)
    
    # Create map
    map_obj = Map()
    for room in [start_room, middle_room, end_room, key_room1, key_room2]:
        map_obj.add_room(room)
    
    # Connect rooms in a circle
    map_obj.connect_rooms(start_room, key_room1, Direction.NORTH)
    map_obj.connect_rooms(key_room1, middle_room, Direction.EAST)
    map_obj.connect_rooms(middle_room, key_room2, Direction.SOUTH)
    map_obj.connect_rooms(key_room2, end_room, Direction.WEST)
    
    # Try to find path with no keys
    assert map_obj.find_accessible_path(start_room, end_room) is None
    
    # Try with only first key
    assert map_obj.find_accessible_path(start_room, end_room, [key1]) is None
    
    # Try with both keys
    path = map_obj.find_accessible_path(start_room, end_room, [key1, key2])
    assert path is not None
    assert len(path) == 4  # start -> key_room1 -> middle -> key_room2 -> end
    
    # Verify keys are needed in correct rooms
    room_keys = [key for _, _, key in path]
    assert room_keys[0] is None  # key_room1 is unlocked
    assert room_keys[1] == key1  # middle room needs key1
    assert room_keys[2] is None  # key_room2 is unlocked
    assert room_keys[3] == key2  # end room needs key2 