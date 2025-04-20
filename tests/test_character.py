"""Tests for the Character model."""
from decimal import Decimal
import pytest

from dungeon.models.character import Character, Alignment
from dungeon.models.item import Item

@pytest.fixture
def character():
    """Create a test character."""
    return Character(
        name="Test Character",
        description="A test character",
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

def test_character_initialization(character):
    """Test character initialization."""
    assert character.name == "Test Character"
    assert character.description == "A test character"
    assert character.hit_points == Decimal("50.0")
    assert character.dexterity == 10
    assert character.intelligence == 10
    assert character.strength == 10
    assert character.gender == "unknown"
    assert character.race == "unknown"
    assert character.alignment == Alignment.TRUE_NEUTRAL
    assert character.items == []

def test_character_immutable_attributes(character):
    """Test that certain character attributes are immutable."""
    with pytest.raises(AttributeError):
        character.name = "New Name"
    
    with pytest.raises(AttributeError):
        character.description = "New Description"

def test_character_hit_points_validation(character):
    """Test hit points validation."""
    character.hit_points = Decimal("75")
    assert character.hit_points == Decimal("75")
    
    with pytest.raises(ValueError):
        character.hit_points = Decimal("-1")
    
    with pytest.raises(ValueError):
        character.hit_points = Decimal("101")

def test_character_attribute_validation():
    """Test validation of character attributes."""
    with pytest.raises(ValueError):
        Character(
            name="Test",
            description="Test",
            hit_points=Decimal("50"),
            dexterity=0,
            intelligence=10,
            strength=10
        )
    
    with pytest.raises(ValueError):
        Character(
            name="Test",
            description="Test",
            hit_points=Decimal("50"),
            dexterity=10,
            intelligence=21,
            strength=10
        )
    
    with pytest.raises(ValueError):
        Character(
            name="Test",
            description="Test",
            hit_points=Decimal("50"),
            dexterity=10,
            intelligence=10,
            strength=-1
        )

def test_character_items(character, sword, shield):
    """Test character item management."""
    character.add_item(sword)
    assert len(character.items) == 1
    assert character.items[0] == sword
    
    character.add_item(shield)
    assert len(character.items) == 2
    assert character.items[1] == shield
    
    character.remove_item(sword)
    assert len(character.items) == 1
    assert character.items[0] == shield
    
    with pytest.raises(ValueError):
        character.remove_item(sword)

def test_character_alignment(character):
    """Test character alignment."""
    # Test default alignment
    assert character.alignment == Alignment.TRUE_NEUTRAL
    
    # Test setting valid alignments
    character.alignment = Alignment.LAWFUL_GOOD
    assert character.alignment == Alignment.LAWFUL_GOOD
    
    character.alignment = Alignment.CHAOTIC_EVIL
    assert character.alignment == Alignment.CHAOTIC_EVIL
    
    # Test setting invalid alignment
    with pytest.raises(ValueError):
        character.alignment = "Invalid Alignment"

def test_character_to_dict(character, sword, shield):
    """Test character serialization."""
    character.add_item(sword)
    character.add_item(shield)
    
    data = character.to_dict()
    assert data["name"] == "Test Character"
    assert data["description"] == "A test character"
    assert data["hit_points"] == 50.0
    assert data["dexterity"] == 10
    assert data["intelligence"] == 10
    assert data["strength"] == 10
    assert data["gender"] == "unknown"
    assert data["race"] == "unknown"
    assert data["alignment"] == "True Neutral"
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Sword"
    assert data["items"][1]["name"] == "Shield"

def test_hit_points_validation():
    """Test hit points validation."""
    # Valid hit points values
    Character(
        name="Test",
        description="Test",
        hit_points=Decimal("0"),
        dexterity=10,
        intelligence=10,
        strength=10
    )
    Character(
        name="Test",
        description="Test",
        hit_points=Decimal("100"),
        dexterity=10,
        intelligence=10,
        strength=10
    )
    
    # Invalid hit points values
    with pytest.raises(ValueError):
        Character(
            name="Test",
            description="Test",
            hit_points=Decimal("-1"),
            dexterity=10,
            intelligence=10,
            strength=10
        )
    
    with pytest.raises(ValueError):
        Character(
            name="Test",
            description="Test",
            hit_points=Decimal("101"),
            dexterity=10,
            intelligence=10,
            strength=10
        )

def test_attribute_validation():
    """Test validation for dexterity, intelligence, and strength."""
    # Valid values
    Character(
        name="Test",
        description="Test",
        hit_points=Decimal("50"),
        dexterity=1,
        intelligence=1,
        strength=1
    )
    Character(
        name="Test",
        description="Test",
        hit_points=Decimal("50"),
        dexterity=20,
        intelligence=20,
        strength=20
    )
    
    # Invalid values
    for attr in ["dexterity", "intelligence", "strength"]:
        with pytest.raises(ValueError, match=f"{attr.capitalize()} must be between 1 and 20"):
            Character(
                name="Test",
                description="Test",
                hit_points=Decimal("50"),
                dexterity=0 if attr == "dexterity" else 10,
                intelligence=0 if attr == "intelligence" else 10,
                strength=0 if attr == "strength" else 10
            )
        
        with pytest.raises(ValueError, match=f"{attr.capitalize()} must be between 1 and 20"):
            Character(
                name="Test",
                description="Test",
                hit_points=Decimal("50"),
                dexterity=21 if attr == "dexterity" else 10,
                intelligence=21 if attr == "intelligence" else 10,
                strength=21 if attr == "strength" else 10
            )

def test_attribute_setters(character):
    """Test setters for dexterity, intelligence, and strength."""
    # Test valid values
    character.dexterity = 15
    assert character.dexterity == 15
    
    character.intelligence = 15
    assert character.intelligence == 15
    
    character.strength = 15
    assert character.strength == 15
    
    # Test invalid values
    for attr, setter in [
        ("dexterity", character.dexterity),
        ("intelligence", character.intelligence),
        ("strength", character.strength)
    ]:
        with pytest.raises(ValueError, match=f"{attr.capitalize()} must be between 1 and 20"):
            setattr(character, attr, 0)
        
        with pytest.raises(ValueError, match=f"{attr.capitalize()} must be between 1 and 20"):
            setattr(character, attr, 21)

def test_to_dict_with_items(character, sword, shield):
    """Test to_dict method with items."""
    character.add_item(sword)
    character.add_item(shield)
    
    char_dict = character.to_dict()
    
    assert "items" in char_dict
    assert len(char_dict["items"]) == 2
    
    # Check first item
    assert char_dict["items"][0]["name"] == "Sword"
    assert char_dict["items"][0]["description"] == "A sharp sword"
    assert char_dict["items"][0]["value"] == 10.0
    assert char_dict["items"][0]["weight"] == 5.0
    
    # Check second item
    assert char_dict["items"][1]["name"] == "Shield"
    assert char_dict["items"][1]["description"] == "A sturdy shield"
    assert char_dict["items"][1]["value"] == 5.0
    assert char_dict["items"][1]["weight"] == 8.0 