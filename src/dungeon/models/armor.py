"""Armor model for the dungeon project."""
from enum import Enum
from typing import Dict, Any

from .item import Item

class ArmorType(Enum):
    """Types of armor."""
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"

class ArmorError(Exception):
    """Exception raised for errors in the Armor class."""
    pass

class Armor(Item):
    """A piece of armor that can be worn for protection."""
    
    def __init__(
        self,
        name: str,
        description: str,
        armor_type: ArmorType,
        armor_rating: int,
        strength_requirement: int = 0,
        dexterity_requirement: int = 0,
        value: float = 0.0,
        weight: float = 0.0
    ) -> None:
        """Initialize a piece of armor.
        
        Args:
            name: The name of the armor
            description: A description of the armor
            armor_type: The type of armor (light, medium, heavy)
            armor_rating: The protection value of the armor
            strength_requirement: The minimum strength required to wear the armor
            dexterity_requirement: The minimum dexterity required to wear the armor
            value: The monetary value of the armor
            weight: The weight of the armor
            
        Raises:
            ArmorError: If armor_rating is not a positive integer
        """
        super().__init__(
            name=name,
            description=description,
            value=value,
            weight=weight
        )
        
        if armor_rating <= 0:
            raise ArmorError("Armor rating must be a positive integer")
            
        self._armor_type = armor_type
        self._armor_rating = armor_rating
        self._strength_requirement = strength_requirement
        self._dexterity_requirement = dexterity_requirement
    
    @property
    def armor_type(self) -> ArmorType:
        """Get the type of armor.
        
        Returns:
            The armor type
        """
        return self._armor_type
    
    @property
    def armor_rating(self) -> int:
        """Get the armor rating.
        
        Returns:
            The protection value of the armor
        """
        return self._armor_rating
    
    @property
    def strength_requirement(self) -> int:
        """Get the strength requirement.
        
        Returns:
            The minimum strength required
        """
        return self._strength_requirement
    
    @property
    def dexterity_requirement(self) -> int:
        """Get the dexterity requirement.
        
        Returns:
            The minimum dexterity required
        """
        return self._dexterity_requirement
    
    def can_wear(self, strength: int, dexterity: int) -> bool:
        """Check if a character can wear this armor.
        
        Args:
            strength: The character's strength
            dexterity: The character's dexterity
            
        Returns:
            True if the character meets the requirements
        """
        return (
            strength >= self._strength_requirement and
            dexterity >= self._dexterity_requirement
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the armor to a dictionary.
        
        Returns:
            Dict containing the armor's attributes
        """
        return {
            **super().to_dict(),
            "armor_type": self.armor_type.value,
            "armor_rating": self.armor_rating,
            "strength_requirement": self.strength_requirement,
            "dexterity_requirement": self.dexterity_requirement
        } 