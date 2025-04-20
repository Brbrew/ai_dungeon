"""Trap model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .base import BaseModel

class Trap(BaseModel):
    """A trap that can be found in a room."""
    
    def __init__(
        self,
        name: str,
        description: str,
        damage: float = 10.0,
        is_triggered: bool = False,
        **kwargs: Any
    ) -> None:
        """Initialize a trap.
        
        Args:
            name: The trap's name
            description: The trap's description
            damage: The amount of damage the trap deals
            is_triggered: Whether the trap has been triggered
            **kwargs: Additional arguments passed to BaseModel
        """
        super().__init__(**kwargs)
        self._name = name
        self._description = description
        self._damage = float(damage)
        self._is_triggered = bool(is_triggered)
    
    @property
    def name(self) -> str:
        """Get the trap's name.
        
        Returns:
            The trap's name
        """
        return self._name
    
    @property
    def description(self) -> str:
        """Get the trap's description.
        
        Returns:
            The trap's description
        """
        return self._description
    
    @property
    def damage(self) -> float:
        """Get the trap's damage.
        
        Returns:
            The trap's damage
        """
        return self._damage
    
    @property
    def is_triggered(self) -> bool:
        """Get whether the trap has been triggered.
        
        Returns:
            True if the trap has been triggered, False otherwise
        """
        return self._is_triggered
    
    @is_triggered.setter
    def is_triggered(self, value: bool) -> None:
        """Set whether the trap has been triggered.
        
        Args:
            value: True if the trap should be triggered, False otherwise
        """
        self._is_triggered = bool(value)
    
    def trigger(self) -> float:
        """Trigger the trap.
        
        Returns:
            The amount of damage dealt
        """
        if not self._is_triggered:
            self._is_triggered = True
            return self._damage
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the trap to a dictionary.
        
        Returns:
            Dict containing the trap's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "description": self.description,
            "damage": self.damage,
            "is_triggered": self.is_triggered,
        } 