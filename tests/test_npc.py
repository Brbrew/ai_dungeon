"""Tests for the NPC model."""
from decimal import Decimal
import pytest

from dungeon.models.npc import NPC
from dungeon.models.item import Item

@pytest.fixture
def npc():
    """Create a test NPC."""
    return NPC(
        name="Test NPC",
        description="A test NPC",
        hit_points=Decimal("50.0"),
        dexterity=10,
        intelligence=10,
        strength=10
    )

@pytest.fixture
def sword():
    """Create a test sword."""
    return Item(
        name="Sword",
        description="A sharp sword",
        value=10.0,
        weight=5.0
    )

@pytest.fixture
def shield():
    """Create a test shield."""
    return Item(
        name="Shield",
        description="A sturdy shield",
        value=5.0,
        weight=8.0
    )

def test_npc_initialization(npc):
    """Test NPC initialization."""
    assert npc.name == "Test NPC"
    assert npc.description == "A test NPC"
    assert npc.hit_points == Decimal("50.0")
    assert npc.dexterity == 10
    assert npc.intelligence == 10
    assert npc.strength == 10
    assert npc.items == []

def test_item_operations(npc, sword, shield):
    """Test item operations."""
    # Add items
    npc.add_item(sword)
    npc.add_item(shield)
    
    assert len(npc.items) == 2
    assert npc.items[0] == sword
    assert npc.items[1] == shield
    
    # Remove items
    npc.remove_item(sword)
    assert len(npc.items) == 1
    assert npc.items[0] == shield
    
    # Try to remove non-existent item
    with pytest.raises(ValueError):
        npc.remove_item(sword)

def test_to_dict(npc, sword, shield):
    """Test to_dict method."""
    npc.add_item(sword)
    npc.add_item(shield)
    
    npc_dict = npc.to_dict()
    
    assert npc_dict["name"] == "Test NPC"
    assert npc_dict["description"] == "A test NPC"
    assert npc_dict["hit_points"] == 50.0
    assert npc_dict["dexterity"] == 10
    assert npc_dict["intelligence"] == 10
    assert npc_dict["strength"] == 10
    assert len(npc_dict["items"]) == 2
    
    # Check first item
    assert npc_dict["items"][0]["name"] == "Sword"
    assert npc_dict["items"][0]["description"] == "A sharp sword"
    assert npc_dict["items"][0]["value"] == 10.0
    assert npc_dict["items"][0]["weight"] == 5.0
    
    # Check second item
    assert npc_dict["items"][1]["name"] == "Shield"
    assert npc_dict["items"][1]["description"] == "A sturdy shield"
    assert npc_dict["items"][1]["value"] == 5.0
    assert npc_dict["items"][1]["weight"] == 8.0 