"""Tests for the Dice model."""
import pytest
from unittest.mock import patch

from dungeon.models.dice import Dice, DiceError

@pytest.fixture
def d4():
    """Create a test d4."""
    return Dice(sides=4)

@pytest.fixture
def d6():
    """Create a test d6."""
    return Dice(sides=6)

@pytest.fixture
def d20():
    """Create a test d20."""
    return Dice(sides=20)

def test_dice_initialization():
    """Test dice initialization."""
    # Test valid dice
    for sides in Dice.VALID_SIDES:
        dice = Dice(sides=sides)
        assert dice.sides == sides
    
    # Test invalid dice
    with pytest.raises(DiceError, match="Invalid number of sides"):
        Dice(sides=7)

def test_dice_roll_range(d4, d6, d20):
    """Test that dice rolls are within valid ranges."""
    # Test d4
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 3
        assert d4.roll() == 3
        mock_randint.assert_called_with(1, 4)
    
    # Test d6
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 4
        assert d6.roll() == 4
        mock_randint.assert_called_with(1, 6)
    
    # Test d20
    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 15
        assert d20.roll() == 15
        mock_randint.assert_called_with(1, 20)

def test_roll_multiple():
    """Test rolling multiple dice."""
    # Test valid number of dice
    rolls = Dice.roll_multiple(num_dice=3, sides=6)
    assert len(rolls) == 3
    assert all(1 <= roll <= 6 for roll in rolls)
    
    # Test invalid number of dice
    with pytest.raises(DiceError, match="Number of dice must be at least 1"):
        Dice.roll_multiple(num_dice=0, sides=6)
    
    # Test invalid sides
    with pytest.raises(DiceError, match="Invalid number of sides"):
        Dice.roll_multiple(num_dice=2, sides=7)

def test_roll_with_modifier():
    """Test rolling dice with a modifier."""
    # Test with positive modifier
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [4, 5, 6]
        result = Dice.roll_with_modifier(num_dice=3, sides=6, modifier=2)
        assert result == 17  # 4 + 5 + 6 + 2
        assert mock_randint.call_count == 3
    
    # Test with negative modifier
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [1, 2, 3]
        result = Dice.roll_with_modifier(num_dice=3, sides=6, modifier=-1)
        assert result == 5  # 1 + 2 + 3 - 1
        assert mock_randint.call_count == 3
    
    # Test with zero modifier
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [3, 3, 3]
        result = Dice.roll_with_modifier(num_dice=3, sides=6, modifier=0)
        assert result == 9  # 3 + 3 + 3 + 0
        assert mock_randint.call_count == 3

def test_to_dict(d6):
    """Test dice serialization."""
    dice_dict = d6.to_dict()
    assert dice_dict["sides"] == 6 