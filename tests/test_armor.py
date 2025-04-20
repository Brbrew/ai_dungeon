"""Tests for the Armor model."""
import pytest

from dungeon.models.armor import Armor, ArmorType, ArmorError

@pytest.fixture
def light_armor():
    """Create a test light armor."""
    return Armor(
        name="Leather Armor",
        description="Light armor made of leather",
        armor_type=ArmorType.LIGHT,
        armor_rating=2,
        strength_requirement=0,
        dexterity_requirement=0,
        value=10.0,
        weight=5.0
    )

@pytest.fixture
def medium_armor():
    """Create a test medium armor."""
    return Armor(
        name="Chain Mail",
        description="Medium armor made of interlocking metal rings",
        armor_type=ArmorType.MEDIUM,
        armor_rating=5,
        strength_requirement=5,
        dexterity_requirement=3,
        value=30.0,
        weight=15.0
    )

@pytest.fixture
def heavy_armor():
    """Create a test heavy armor."""
    return Armor(
        name="Plate Mail",
        description="Heavy armor made of metal plates",
        armor_type=ArmorType.HEAVY,
        armor_rating=8,
        strength_requirement=10,
        dexterity_requirement=5,
        value=50.0,
        weight=30.0
    )

def test_armor_initialization(light_armor, medium_armor, heavy_armor):
    """Test armor initialization."""
    # Test light armor
    assert light_armor.name == "Leather Armor"
    assert light_armor.description == "Light armor made of leather"
    assert light_armor.armor_type == ArmorType.LIGHT
    assert light_armor.armor_rating == 2
    assert light_armor.strength_requirement == 0
    assert light_armor.dexterity_requirement == 0
    assert light_armor.value == 10.0
    assert light_armor.weight == 5.0
    
    # Test medium armor
    assert medium_armor.name == "Chain Mail"
    assert medium_armor.description == "Medium armor made of interlocking metal rings"
    assert medium_armor.armor_type == ArmorType.MEDIUM
    assert medium_armor.armor_rating == 5
    assert medium_armor.strength_requirement == 5
    assert medium_armor.dexterity_requirement == 3
    assert medium_armor.value == 30.0
    assert medium_armor.weight == 15.0
    
    # Test heavy armor
    assert heavy_armor.name == "Plate Mail"
    assert heavy_armor.description == "Heavy armor made of metal plates"
    assert heavy_armor.armor_type == ArmorType.HEAVY
    assert heavy_armor.armor_rating == 8
    assert heavy_armor.strength_requirement == 10
    assert heavy_armor.dexterity_requirement == 5
    assert heavy_armor.value == 50.0
    assert heavy_armor.weight == 30.0

def test_invalid_armor_rating():
    """Test that armor rating must be positive."""
    with pytest.raises(ArmorError, match="Armor rating must be a positive integer"):
        Armor(
            name="Invalid Armor",
            description="Armor with invalid rating",
            armor_type=ArmorType.LIGHT,
            armor_rating=0
        )
    
    with pytest.raises(ArmorError, match="Armor rating must be a positive integer"):
        Armor(
            name="Invalid Armor",
            description="Armor with invalid rating",
            armor_type=ArmorType.LIGHT,
            armor_rating=-1
        )

def test_can_wear(light_armor, medium_armor, heavy_armor):
    """Test armor usage requirements."""
    # Test light armor (no requirements)
    assert light_armor.can_wear(0, 0) is True  # Meets requirements
    assert light_armor.can_wear(5, 5) is True  # Exceeds requirements
    
    # Test medium armor
    assert medium_armor.can_wear(5, 3) is True  # Meets requirements
    assert medium_armor.can_wear(4, 3) is False  # Too weak
    assert medium_armor.can_wear(5, 2) is False  # Too clumsy
    
    # Test heavy armor
    assert heavy_armor.can_wear(10, 5) is True  # Meets requirements
    assert heavy_armor.can_wear(9, 5) is False  # Too weak
    assert heavy_armor.can_wear(10, 4) is False  # Too clumsy

def test_to_dict(light_armor, medium_armor, heavy_armor):
    """Test armor serialization."""
    # Test light armor
    light_dict = light_armor.to_dict()
    assert light_dict["name"] == "Leather Armor"
    assert light_dict["description"] == "Light armor made of leather"
    assert light_dict["armor_type"] == "light"
    assert light_dict["armor_rating"] == 2
    assert light_dict["strength_requirement"] == 0
    assert light_dict["dexterity_requirement"] == 0
    assert light_dict["value"] == 10.0
    assert light_dict["weight"] == 5.0
    
    # Test medium armor
    medium_dict = medium_armor.to_dict()
    assert medium_dict["name"] == "Chain Mail"
    assert medium_dict["description"] == "Medium armor made of interlocking metal rings"
    assert medium_dict["armor_type"] == "medium"
    assert medium_dict["armor_rating"] == 5
    assert medium_dict["strength_requirement"] == 5
    assert medium_dict["dexterity_requirement"] == 3
    assert medium_dict["value"] == 30.0
    assert medium_dict["weight"] == 15.0
    
    # Test heavy armor
    heavy_dict = heavy_armor.to_dict()
    assert heavy_dict["name"] == "Plate Mail"
    assert heavy_dict["description"] == "Heavy armor made of metal plates"
    assert heavy_dict["armor_type"] == "heavy"
    assert heavy_dict["armor_rating"] == 8
    assert heavy_dict["strength_requirement"] == 10
    assert heavy_dict["dexterity_requirement"] == 5
    assert heavy_dict["value"] == 50.0
    assert heavy_dict["weight"] == 30.0 