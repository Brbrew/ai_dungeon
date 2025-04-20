"""Item model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .base import BaseModel

class Item(BaseModel):
    """An item that can be found in a room."""
    
    def __init__(
        self,
        name: str,
        description: str,
        value: float = 0.0,
        weight: float = 0.0,
        **kwargs: Any
    ) -> None:
        """Initialize an item.
        
        Args:
            name: The item's name
            description: The item's description
            value: The item's monetary value
            weight: The item's weight (must be non-negative)
            **kwargs: Additional arguments passed to BaseModel
            
        Raises:
            ValueError: If weight is negative
        """
        if weight < 0:
            raise ValueError("Weight must be non-negative")
            
        super().__init__(**kwargs)
        self._name = name
        self._description = description
        self._value = float(value)
        self._weight = float(weight)
    
    @property
    def name(self) -> str:
        """Get the item's name.
        
        Returns:
            The item's name
        """
        return self._name
    
    @property
    def description(self) -> str:
        """Get the item's description.
        
        Returns:
            The item's description
        """
        return self._description
    
    @property
    def value(self) -> float:
        """Get the item's value.
        
        Returns:
            The item's value
        """
        return self._value
    
    @property
    def weight(self) -> float:
        """Get the item's weight.
        
        Returns:
            The item's weight
        """
        return self._weight
    
    @weight.setter
    def weight(self, value: float) -> None:
        """Set the item's weight.
        
        Args:
            value: The new weight value (must be non-negative)
            
        Raises:
            ValueError: If weight is negative
        """
        if value < 0:
            raise ValueError("Weight must be non-negative")
        self._weight = float(value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the item to a dictionary.
        
        Returns:
            Dict containing the item's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "weight": self.weight,
        } 