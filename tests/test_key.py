"""Tests for the Key model."""
import pytest
from uuid import UUID

from dungeon.models.key import Key
from dungeon.models.room import Room, RoomLockError
from dungeon.models.theme import Theme

@pytest.fixture
def theme():
    """Create a test theme."""
    return Theme(
        name="Test Theme",
        description="A test theme",
        room_types=["test"],
        item_types=["key"]
    )

@pytest.fixture
def room(theme):
    """Create a test room."""
    return Room(
        name="Test Room",
        description="A test room",
        theme=theme,
        room_type="test"
    )

@pytest.fixture
def key(room):
    """Create a test key."""
    return Key(
        name="Test Key",
        description="A test key",
        value=10.0,
        weight=1.0,
        unlocks_room_id=room.id
    )

def test_key_initialization(key, room):
    """Test key initialization."""
    assert key.name == "Test Key"
    assert key.description == "A test key"
    assert key.value == 10.0
    assert key.weight == 1.0
    assert key.unlocks_room_id == room.id

def test_key_unlock_room(key, room):
    """Test unlocking a room with a key."""
    # Lock the room
    room.lock()
    assert room.is_locked is True
    
    # Unlock with correct key
    room.unlock(key)
    assert room.is_locked is False
    
    # Try to unlock with incorrect key
    wrong_key = Key(
        name="Wrong Key",
        description="A wrong key",
        value=5.0,
        weight=0.5,
        unlocks_room_id=UUID('00000000-0000-0000-0000-000000000000')
    )
    room.lock()
    with pytest.raises(RoomLockError):
        room.unlock(wrong_key)
    
    # Force unlock without key
    room.lock()
    room.unlock(None)
    assert room.is_locked is False

def test_key_can_unlock(key, room):
    """Test whether a key can unlock a specific room."""
    assert key.can_unlock(room.id) is True
    assert key.can_unlock(UUID('00000000-0000-0000-0000-000000000000')) is False

def test_key_to_dict(key, room):
    """Test key serialization."""
    key_dict = key.to_dict()
    
    assert key_dict["name"] == "Test Key"
    assert key_dict["description"] == "A test key"
    assert key_dict["value"] == 10.0
    assert key_dict["weight"] == 1.0
    assert key_dict["unlocks_room_id"] == str(room.id) 