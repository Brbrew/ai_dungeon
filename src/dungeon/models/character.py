"""Character model for the dungeon project."""
from decimal import Decimal
from typing import List, Any
from enum import Enum

from .base import BaseModel
from .item import Item

class Alignment(Enum):
    """Character alignment options."""
    LAWFUL_GOOD = "Lawful Good"
    NEUTRAL_GOOD = "Neutral Good"
    CHAOTIC_GOOD = "Chaotic Good"
    LAWFUL_NEUTRAL = "Lawful Neutral"
    TRUE_NEUTRAL = "True Neutral"
    CHAOTIC_NEUTRAL = "Chaotic Neutral"
    LAWFUL_EVIL = "Lawful Evil"
    NEUTRAL_EVIL = "Neutral Evil"
    CHAOTIC_EVIL = "Chaotic Evil"

class Character(BaseModel):
    """A character in the dungeon with attributes, inventory, and description."""
    
    def __init__(
        self,
        name: str,
        description: str,
        hit_points: Decimal,
        dexterity: int,
        intelligence: int,
        strength: int,
        gender: str = "unknown",
        race: str = "unknown",
        alignment: Alignment = Alignment.TRUE_NEUTRAL,
        **kwargs: Any
    ) -> None:
        """Initialize a character.
        
        Args:
            name: The character's name (immutable)
            description: The character's description (immutable)
            hit_points: The character's hit points (0-100)
            dexterity: The character's dexterity (1-20)
            intelligence: The character's intelligence (1-20)
            strength: The character's strength (1-20)
            gender: The character's gender (default: "unknown")
            race: The character's race (default: "unknown")
            alignment: The character's alignment (default: TRUE_NEUTRAL)
            **kwargs: Additional arguments passed to BaseModel
            
        Raises:
            ValueError: If hit_points is not between 0 and 100
            ValueError: If dexterity, intelligence, or strength is not between 1 and 20
        """
        if not 0 <= hit_points <= 100:
            raise ValueError("Hit points must be between 0 and 100")
            
        for attr, value in [("dexterity", dexterity), ("intelligence", intelligence), ("strength", strength)]:
            if not 1 <= value <= 20:
                raise ValueError(f"{attr.capitalize()} must be between 1 and 20")
            
        super().__init__(**kwargs)
        
        # Immutable attributes
        self._name = name
        self._description = description
        
        # Mutable attributes
        self._hit_points = Decimal(str(hit_points))
        self._dexterity = int(dexterity)
        self._intelligence = int(intelligence)
        self._strength = int(strength)
        self._gender = str(gender)
        self._race = str(race)
        self._alignment = alignment
        self._items: List[Item] = []
    
    @property
    def name(self) -> str:
        """Get the character's name.
        
        Returns:
            The character's name
        """
        return self._name
    
    @property
    def description(self) -> str:
        """Get the character's description.
        
        Returns:
            The character's description
        """
        return self._description
    
    @property
    def hit_points(self) -> Decimal:
        """Get the character's hit points.
        
        Returns:
            The character's hit points
        """
        return self._hit_points
    
    @hit_points.setter
    def hit_points(self, value: Decimal) -> None:
        """Set the character's hit points.
        
        Args:
            value: The new hit points value (0-100)
            
        Raises:
            ValueError: If hit points is not between 0 and 100
        """
        if not 0 <= value <= 100:
            raise ValueError("Hit points must be between 0 and 100")
        self._hit_points = Decimal(str(value))
    
    @property
    def dexterity(self) -> int:
        """Get the character's dexterity.
        
        Returns:
            The character's dexterity
        """
        return self._dexterity
    
    @dexterity.setter
    def dexterity(self, value: int) -> None:
        """Set the character's dexterity.
        
        Args:
            value: The new dexterity value (1-20)
            
        Raises:
            ValueError: If dexterity is not between 1 and 20
        """
        if not 1 <= value <= 20:
            raise ValueError("Dexterity must be between 1 and 20")
        self._dexterity = int(value)
    
    @property
    def intelligence(self) -> int:
        """Get the character's intelligence.
        
        Returns:
            The character's intelligence
        """
        return self._intelligence
    
    @intelligence.setter
    def intelligence(self, value: int) -> None:
        """Set the character's intelligence.
        
        Args:
            value: The new intelligence value (1-20)
            
        Raises:
            ValueError: If intelligence is not between 1 and 20
        """
        if not 1 <= value <= 20:
            raise ValueError("Intelligence must be between 1 and 20")
        self._intelligence = int(value)
    
    @property
    def strength(self) -> int:
        """Get the character's strength.
        
        Returns:
            The character's strength
        """
        return self._strength
    
    @strength.setter
    def strength(self, value: int) -> None:
        """Set the character's strength.
        
        Args:
            value: The new strength value (1-20)
            
        Raises:
            ValueError: If strength is not between 1 and 20
        """
        if not 1 <= value <= 20:
            raise ValueError("Strength must be between 1 and 20")
        self._strength = int(value)
    
    @property
    def gender(self) -> str:
        """Get the character's gender.
        
        Returns:
            The character's gender
        """
        return self._gender
    
    @gender.setter
    def gender(self, value: str) -> None:
        """Set the character's gender.
        
        Args:
            value: The new gender value
        """
        self._gender = str(value)
    
    @property
    def race(self) -> str:
        """Get the character's race.
        
        Returns:
            The character's race
        """
        return self._race
    
    @race.setter
    def race(self, value: str) -> None:
        """Set the character's race.
        
        Args:
            value: The new race value
        """
        self._race = str(value)
    
    @property
    def alignment(self) -> Alignment:
        """Get the character's alignment.
        
        Returns:
            The character's alignment
        """
        return self._alignment
    
    @alignment.setter
    def alignment(self, value: Alignment) -> None:
        """Set the character's alignment.
        
        Args:
            value: The new alignment value
            
        Raises:
            ValueError: If value is not a valid Alignment
        """
        if not isinstance(value, Alignment):
            raise ValueError("Alignment must be a valid Alignment enum value")
        self._alignment = value
    
    @property
    def items(self) -> List[Item]:
        """Get the character's items.
        
        Returns:
            A copy of the character's items
        """
        return self._items.copy()
    
    def add_item(self, item: Item) -> None:
        """Add an item to the character's inventory.
        
        Args:
            item: The item to add
        """
        self._items.append(item)
    
    def remove_item(self, item: Item) -> None:
        """Remove an item from the character's inventory.
        
        Args:
            item: The item to remove
            
        Raises:
            ValueError: If the item is not in the inventory
        """
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError(f"Item {item.name} not found in inventory")
    
    def to_dict(self) -> dict:
        """Convert the character to a dictionary.
        
        Returns:
            Dict containing the character's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "description": self.description,
            "hit_points": float(self.hit_points),
            "dexterity": self.dexterity,
            "intelligence": self.intelligence,
            "strength": self.strength,
            "gender": self.gender,
            "race": self.race,
            "alignment": self.alignment.value,
            "items": [item.to_dict() for item in self.items]
        } 