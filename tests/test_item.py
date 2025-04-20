"""Tests for the Item model."""
import pytest

from dungeon.models.item import Item

@pytest.fixture
def sword():
    """Create a test sword item."""
    return Item(
        name="Sword",
        description="A sharp sword",
        value=10.0,
        weight=5.0
    )

@pytest.fixture
def shield():
    """Create a test shield item."""
    return Item(
        name="Shield",
        description="A sturdy shield",
        value=5.0,
        weight=8.0
    )

def test_item_initialization(sword):
    """Test item initialization."""
    assert sword.name == "Sword"
    assert sword.description == "A sharp sword"
    assert sword.value == 10.0
    assert sword.weight == 5.0

def test_weight_validation():
    """Test weight validation."""
    # Valid weight values
    Item(
        name="Test",
        description="Test",
        value=10.0,
        weight=0.0
    )
    Item(
        name="Test",
        description="Test",
        value=10.0,
        weight=10.0
    )
    
    # Invalid weight values
    with pytest.raises(ValueError, match="Weight must be non-negative"):
        Item(
            name="Test",
            description="Test",
            value=10.0,
            weight=-1.0
        )

def test_weight_setter(sword):
    """Test weight setter."""
    sword.weight = 7.0
    assert sword.weight == 7.0
    
    with pytest.raises(ValueError, match="Weight must be non-negative"):
        sword.weight = -1.0

def test_to_dict(sword):
    """Test to_dict method."""
    item_dict = sword.to_dict()
    
    assert item_dict["name"] == "Sword"
    assert item_dict["description"] == "A sharp sword"
    assert item_dict["value"] == 10.0
    assert item_dict["weight"] == 5.0 