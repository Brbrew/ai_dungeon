"""Dice model for the dungeon project."""
import random
from typing import List, Optional

from .base import BaseModel

class DiceError(Exception):
    """Exception raised for errors in the Dice class."""
    pass

class Dice(BaseModel):
    """A dice that can be rolled to generate random numbers."""
    
    # Valid number of sides for dice
    VALID_SIDES = {4, 6, 8, 12, 20}
    
    def __init__(self, sides: int = 6) -> None:
        """Initialize a dice.
        
        Args:
            sides: The number of sides on the dice (must be 4, 6, 8, 12, or 20)
            
        Raises:
            DiceError: If sides is not a valid number
        """
        if sides not in self.VALID_SIDES:
            raise DiceError(f"Invalid number of sides: {sides}. Must be one of {sorted(self.VALID_SIDES)}")
            
        super().__init__()
        self._sides = sides
    
    @property
    def sides(self) -> int:
        """Get the number of sides on the dice.
        
        Returns:
            The number of sides
        """
        return self._sides
    
    def roll(self) -> int:
        """Roll the dice once.
        
        Returns:
            A random number between 1 and the number of sides (inclusive)
        """
        return random.randint(1, self._sides)
    
    @classmethod
    def roll_multiple(cls, num_dice: int, sides: int = 6) -> List[int]:
        """Roll multiple dice of the same type.
        
        Args:
            num_dice: The number of dice to roll
            sides: The number of sides on each dice
            
        Returns:
            A list of random numbers, one for each dice
            
        Raises:
            DiceError: If sides is not a valid number or num_dice is less than 1
        """
        if num_dice < 1:
            raise DiceError("Number of dice must be at least 1")
            
        dice = cls(sides)
        return [dice.roll() for _ in range(num_dice)]
    
    @classmethod
    def roll_with_modifier(cls, num_dice: int, sides: int = 6, modifier: int = 0) -> int:
        """Roll multiple dice and add a modifier.
        
        Args:
            num_dice: The number of dice to roll
            sides: The number of sides on each dice
            modifier: A number to add to the sum of the dice rolls
            
        Returns:
            The sum of all dice rolls plus the modifier
            
        Raises:
            DiceError: If sides is not a valid number or num_dice is less than 1
        """
        rolls = cls.roll_multiple(num_dice, sides)
        return sum(rolls) + modifier
    
    def to_dict(self) -> dict:
        """Convert the dice to a dictionary.
        
        Returns:
            Dict containing the dice's attributes
        """
        return {
            **super().to_dict(),
            "sides": self.sides
        } 