"""Tests for the Room model."""
from decimal import Decimal
import pytest

from dungeon.models.character import Character
from dungeon.models.item import Item
from dungeon.models.npc import NPC
from dungeon.models.room import Room
from dungeon.models.theme import Theme
from dungeon.models.trap import Trap

@pytest.fixture
def theme():
    """Create a test theme."""
    return Theme(
        name="Test Theme",
        description="A test theme"
    )

@pytest.fixture
def room(theme):
    """Create a test room."""
    return Room(
        description="A test room",
        theme=theme,
        is_dark=False
    )

@pytest.fixture
def npc():
    """Create a test NPC."""
    return NPC(
        name="Test NPC",
        description="A test NPC",
        health=Decimal("50.0"),
        is_hostile=False
    )

@pytest.fixture
def item():
    """Create a test item."""
    return Item(
        name="Test Item",
        description="A test item",
        value=10.0
    )

@pytest.fixture
def trap():
    """Create a test trap."""
    return Trap(
        name="Test Trap",
        description="A test trap",
        damage=15.0
    )

def test_room_initialization(room, theme):
    """Test room initialization."""
    assert room.description == "A test room"
    assert room.theme == theme
    assert room.is_dark is False
    assert room.visited is False
    assert room.npcs == []
    assert room.treasures == []
    assert room.traps == []

def test_room_attributes(room):
    """Test room attribute setters and getters."""
    # Test is_dark
    room.is_dark = True
    assert room.is_dark is True
    
    # Test visited
    room.visited = True
    assert room.visited is True

def test_room_npcs(room, npc):
    """Test room NPC operations."""
    # Add NPC
    room.add_npc(npc)
    assert len(room.npcs) == 1
    assert room.npcs[0] == npc
    
    # Remove NPC
    room.remove_npc(npc)
    assert len(room.npcs) == 0
    
    # Try to remove non-existent NPC
    with pytest.raises(ValueError):
        room.remove_npc(npc)

def test_room_treasures(room, item):
    """Test room treasure operations."""
    # Add treasure
    room.add_treasure(item)
    assert len(room.treasures) == 1
    assert room.treasures[0] == item
    
    # Remove treasure
    room.remove_treasure(item)
    assert len(room.treasures) == 0
    
    # Try to remove non-existent treasure
    with pytest.raises(ValueError):
        room.remove_treasure(item)

def test_room_traps(room, trap):
    """Test room trap operations."""
    # Add trap
    room.add_trap(trap)
    assert len(room.traps) == 1
    assert room.traps[0] == trap
    
    # Remove trap
    room.remove_trap(trap)
    assert len(room.traps) == 0
    
    # Try to remove non-existent trap
    with pytest.raises(ValueError):
        room.remove_trap(trap)

def test_room_to_dict(room, theme, npc, item, trap):
    """Test room to_dict method."""
    # Add content to room
    room.add_npc(npc)
    room.add_treasure(item)
    room.add_trap(trap)
    
    # Convert to dict
    room_dict = room.to_dict()
    
    # Check basic attributes
    assert room_dict["description"] == "A test room"
    assert room_dict["is_dark"] is False
    assert room_dict["visited"] is False
    
    # Check theme
    assert room_dict["theme"]["name"] == "Test Theme"
    assert room_dict["theme"]["description"] == "A test theme"
    
    # Check collections
    assert len(room_dict["npcs"]) == 1
    assert len(room_dict["treasures"]) == 1
    assert len(room_dict["traps"]) == 1 