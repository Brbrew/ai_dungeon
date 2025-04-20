"""Tests for the Weapon model."""
import pytest
from unittest.mock import patch

from dungeon.models.weapon import Weapon, WeaponType, WeaponError
from dungeon.models.dice import Dice

@pytest.fixture
def d6():
    """Create a test d6."""
    return Dice(sides=6)

@pytest.fixture
def d8():
    """Create a test d8."""
    return Dice(sides=8)

@pytest.fixture
def melee_sword(d6):
    """Create a test melee sword."""
    return Weapon(
        name="Long Sword",
        description="A standard long sword",
        weapon_type=WeaponType.MELEE,
        damage_dice=d6,
        num_damage_dice=1,
        damage_modifier=0,
        strength_requirement=10,
        dexterity_requirement=5,
        value=15.0,
        weight=3.0
    )

@pytest.fixture
def great_sword(d6):
    """Create a test great sword with multiple damage dice."""
    return Weapon(
        name="Great Sword",
        description="A massive two-handed sword",
        weapon_type=WeaponType.MELEE,
        damage_dice=d6,
        num_damage_dice=2,
        damage_modifier=0,
        strength_requirement=15,
        dexterity_requirement=8,
        value=30.0,
        weight=6.0
    )

@pytest.fixture
def magic_sword(d6):
    """Create a test magic sword with a damage modifier."""
    return Weapon(
        name="Magic Sword",
        description="A sword imbued with magical power",
        weapon_type=WeaponType.MELEE,
        damage_dice=d6,
        num_damage_dice=1,
        damage_modifier=2,
        strength_requirement=10,
        dexterity_requirement=5,
        value=50.0,
        weight=3.0
    )

@pytest.fixture
def ranged_bow(d8):
    """Create a test ranged bow."""
    return Weapon(
        name="Short Bow",
        description="A standard short bow",
        weapon_type=WeaponType.RANGED,
        damage_dice=d8,
        num_damage_dice=1,
        damage_modifier=0,
        strength_requirement=8,
        dexterity_requirement=12,
        range_distance=60,
        value=25.0,
        weight=2.0
    )

def test_weapon_initialization(melee_sword, great_sword, magic_sword, ranged_bow):
    """Test weapon initialization."""
    # Test melee weapon
    assert melee_sword.name == "Long Sword"
    assert melee_sword.description == "A standard long sword"
    assert melee_sword.weapon_type == WeaponType.MELEE
    assert melee_sword.damage_dice.sides == 6
    assert melee_sword.num_damage_dice == 1
    assert melee_sword.damage_modifier == 0
    assert melee_sword.strength_requirement == 10
    assert melee_sword.dexterity_requirement == 5
    assert melee_sword.range_distance is None
    assert melee_sword.value == 15.0
    assert melee_sword.weight == 3.0
    
    # Test great sword
    assert great_sword.name == "Great Sword"
    assert great_sword.num_damage_dice == 2
    assert great_sword.damage_modifier == 0
    assert great_sword.strength_requirement == 15
    
    # Test magic sword
    assert magic_sword.name == "Magic Sword"
    assert magic_sword.num_damage_dice == 1
    assert magic_sword.damage_modifier == 2
    
    # Test ranged weapon
    assert ranged_bow.name == "Short Bow"
    assert ranged_bow.description == "A standard short bow"
    assert ranged_bow.weapon_type == WeaponType.RANGED
    assert ranged_bow.damage_dice.sides == 8
    assert ranged_bow.num_damage_dice == 1
    assert ranged_bow.damage_modifier == 0
    assert ranged_bow.strength_requirement == 8
    assert ranged_bow.dexterity_requirement == 12
    assert ranged_bow.range_distance == 60
    assert ranged_bow.value == 25.0
    assert ranged_bow.weight == 2.0

def test_ranged_weapon_requires_range():
    """Test that ranged weapons require a range distance."""
    with pytest.raises(WeaponError, match="Range distance must be provided for ranged weapons"):
        Weapon(
            name="Bow",
            description="A bow without range",
            weapon_type=WeaponType.RANGED,
            damage_dice=Dice(sides=6)
        )

def test_roll_damage(melee_sword, ranged_bow):
    """Test rolling for damage."""
    # Test melee weapon
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 4
        assert melee_sword.roll_damage() == 4
        mock_randint.assert_called_with(1, 6)
    
    # Test ranged weapon
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 6
        assert ranged_bow.roll_damage() == 6
        mock_randint.assert_called_with(1, 8)

def test_roll_damage_with_modifier(magic_sword):
    """Test rolling for damage with a modifier."""
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 4
        assert magic_sword.roll_damage_with_modifier() == 6  # 4 + 2
        mock_randint.assert_called_with(1, 6)
        
        # Test with additional modifier
        assert magic_sword.roll_damage_with_modifier(3) == 9  # 4 + 2 + 3

def test_roll_multiple_damage(great_sword):
    """Test rolling multiple dice for damage."""
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [3, 5]
        rolls = great_sword.roll_multiple_damage()
        assert rolls == [3, 5]
        assert mock_randint.call_count == 2
        mock_randint.assert_any_call(1, 6)
        mock_randint.assert_any_call(1, 6)

def test_roll_total_damage(great_sword, magic_sword):
    """Test rolling total damage with all dice and modifiers."""
    # Test great sword (2d6)
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [4, 6]
        total, rolls = great_sword.roll_total_damage()
        assert rolls == [4, 6]
        assert total == 10  # 4 + 6 + 0
        assert mock_randint.call_count == 2
        
        # Test with additional modifier
        total, rolls = great_sword.roll_total_damage(2)
        assert total == 12  # 4 + 6 + 0 + 2
    
    # Test magic sword (1d6+2)
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 5
        total, rolls = magic_sword.roll_total_damage()
        assert rolls == [5]
        assert total == 7  # 5 + 2
        assert mock_randint.call_count == 1
        
        # Test with additional modifier
        total, rolls = magic_sword.roll_total_damage(3)
        assert total == 10  # 5 + 2 + 3

def test_can_use(melee_sword, ranged_bow):
    """Test weapon usage requirements."""
    # Test melee weapon
    assert melee_sword.can_use(10, 5) is True  # Meets requirements
    assert melee_sword.can_use(9, 5) is False  # Too weak
    assert melee_sword.can_use(10, 4) is False  # Too clumsy
    
    # Test ranged weapon
    assert ranged_bow.can_use(8, 12) is True  # Meets requirements
    assert ranged_bow.can_use(7, 12) is False  # Too weak
    assert ranged_bow.can_use(8, 11) is False  # Too clumsy

def test_to_dict(melee_sword, great_sword, magic_sword, ranged_bow):
    """Test weapon serialization."""
    # Test melee weapon
    sword_dict = melee_sword.to_dict()
    assert sword_dict["name"] == "Long Sword"
    assert sword_dict["description"] == "A standard long sword"
    assert sword_dict["weapon_type"] == "melee"
    assert sword_dict["damage_dice"]["sides"] == 6
    assert sword_dict["num_damage_dice"] == 1
    assert sword_dict["damage_modifier"] == 0
    assert sword_dict["strength_requirement"] == 10
    assert sword_dict["dexterity_requirement"] == 5
    assert "range_distance" not in sword_dict
    assert sword_dict["value"] == 15.0
    assert sword_dict["weight"] == 3.0
    
    # Test great sword
    great_sword_dict = great_sword.to_dict()
    assert great_sword_dict["num_damage_dice"] == 2
    assert great_sword_dict["damage_modifier"] == 0
    
    # Test magic sword
    magic_sword_dict = magic_sword.to_dict()
    assert magic_sword_dict["num_damage_dice"] == 1
    assert magic_sword_dict["damage_modifier"] == 2
    
    # Test ranged weapon
    bow_dict = ranged_bow.to_dict()
    assert bow_dict["name"] == "Short Bow"
    assert bow_dict["description"] == "A standard short bow"
    assert bow_dict["weapon_type"] == "ranged"
    assert bow_dict["damage_dice"]["sides"] == 8
    assert bow_dict["num_damage_dice"] == 1
    assert bow_dict["damage_modifier"] == 0
    assert bow_dict["strength_requirement"] == 8
    assert bow_dict["dexterity_requirement"] == 12
    assert bow_dict["range_distance"] == 60
    assert bow_dict["value"] == 25.0
    assert bow_dict["weight"] == 2.0 