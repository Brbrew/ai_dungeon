"""Potion model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .item import Item
from .action import Action, ActionType

class Potion(Item):
    """A potion that can be drunk."""
    
    def __init__(
        self,
        name: str,
        description: str,
        detailed_description: str,
        smell_description: str,
        effects: str,
        value: float = 0.0,
        weight: float = 0.0,
        **kwargs: Any
    ) -> None:
        """Initialize a potion.
        
        Args:
            name: The potion's name
            description: The potion's description
            detailed_description: A more detailed description of the potion
            effects: Description of what happens when the potion is drunk
            value: The potion's monetary value
            weight: The potion's weight (must be non-negative)
            **kwargs: Additional arguments passed to Item
            
        Raises:
            ValueError: If weight is negative
        """
        super().__init__(
            name=name,
            description=description,
            detailed_description=detailed_description,
            value=value,
            weight=weight,
            **kwargs
        )
        self._effects = effects
        self._smell_description = smell_description

    @property
    def effects(self) -> str:
        """Get the potion's effects.
        
        Returns:
            Description of the potion's effects
        """
        return self._effects
    
    @property
    def smell_description(self) -> str:
        """Get the description of the potion's smell.
        
        Returns:
            Description of the potion's smell
        """
        return self._smell_description
    
    def _handle_drink(self) -> str:
        """Handle the DRINK action on this potion.
        
        Returns:
            A message describing the effects of drinking the potion
        """
        return f"You drink the {self.name}. {self.effects}"
    
    def _handle_smell(self) -> str:
        """Handle the SMELL action on this potion.
        
        Returns:
            A message describing the potion's scent
        """
        return f"You smell the {self.name}. {self.smell_description}."
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the potion to a dictionary.
        
        Returns:
            Dict containing the potion's attributes
        """
        return {
            **super().to_dict(),
            "effects": self.effects,
            "smell_description": self.smell_description
        } 