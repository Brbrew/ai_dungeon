"""NPC (Non-Player Character) model for the dungeon project."""
from decimal import Decimal
from typing import Any, Optional

from .character import Character
from .race import Race

class NPC(Character):
    """A non-player character in the dungeon."""
    
    def __init__(
        self,
        name: str,
        description: str,
        hit_points: Decimal,
        dexterity: int,
        intelligence: int,
        strength: int,
        alias: Optional[str] = None,
        race: Race = Race.HUMAN,
        ai_enabled: bool = False,
        **kwargs: Any
    ) -> None:
        """Initialize an NPC.
        
        Args:
            name: The NPC's name (immutable)
            description: The NPC's description (immutable)
            hit_points: The NPC's hit points (0-100)
            dexterity: The NPC's dexterity (1-20)
            intelligence: The NPC's intelligence (1-20)
            strength: The NPC's strength (1-20)
            alias: An alternative name for the NPC (immutable)
            race: The NPC's race (default: HUMAN)
            ai_enabled: Whether AI is enabled for this NPC (default: False)
            **kwargs: Additional arguments passed to Character
        """
        super().__init__(
            name=name,
            description=description,
            hit_points=hit_points,
            dexterity=dexterity,
            intelligence=intelligence,
            strength=strength,
            race=race.value,
            **kwargs
        )
        self._alias = alias
        self._ai_enabled = ai_enabled
    
    @property
    def ai_enabled(self) -> bool:
        """Get whether AI is enabled for this NPC.
        
        Returns:
            True if AI is enabled, False otherwise
        """
        return self._ai_enabled
    
    @ai_enabled.setter
    def ai_enabled(self, value: bool) -> None:
        """Set whether AI is enabled for this NPC.
        
        Args:
            value: True to enable AI, False to disable
        """
        self._ai_enabled = value
        print(f"DEBUG: AI enabled set to {value} for NPC {self.name}")
    
    @property
    def alias(self) -> Optional[str]:
        """Get the NPC's alias.
        
        Returns:
            The NPC's alias or None if not set
        """
        return self._alias
    
    @property
    def race_enum(self) -> Race:
        """Get the NPC's race as a Race enum.
        
        Returns:
            The NPC's race as a Race enum
        """
        try:
            return Race(self.race)
        except ValueError:
            return Race.HUMAN
    
    def to_dict(self) -> dict:
        """Convert the NPC to a dictionary.
        
        Returns:
            Dict containing the NPC's attributes
        """
        data = super().to_dict()
        data["alias"] = self._alias
        data["race"] = self.race_enum.value
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'NPC':
        """Create an NPC from a dictionary.
        
        Args:
            data: The dictionary to create the NPC from
            
        Returns:
            A new NPC instance
        """
        race_str = data.get("race", "Human")
        try:
            race = Race(race_str)
        except ValueError:
            race = Race.HUMAN
            
        return cls(
            name=data["name"],
            description=data["description"],
            hit_points=data["hit_points"],
            dexterity=data["dexterity"],
            intelligence=data["intelligence"],
            strength=data["strength"],
            alias=data.get("alias"),
            race=race,
            ai_enabled=data.get("ai_enabled", False),
            id=data.get("id")
        ) 