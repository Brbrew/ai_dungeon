"""RoomType model for the dungeon project."""
from typing import Any, Dict, Optional

from .base import BaseModel

class RoomType(BaseModel):
    """A type of room in the dungeon (e.g., treasure room, boss room, etc.)."""
    
    def __init__(
        self,
        name: str,
        description: str,
        **kwargs: Any
    ) -> None:
        """Initialize a room type.
        
        Args:
            name: The room type's name
            description: The room type's description
            **kwargs: Additional arguments passed to BaseModel
        """
        super().__init__(**kwargs)
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """Get the room type's name.
        
        Returns:
            The room type's name
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the room type's name.
        
        Args:
            value: The new name for the room type
        """
        self._name = value
    
    @property
    def description(self) -> str:
        """Get the room type's description.
        
        Returns:
            The room type's description
        """
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        """Set the room type's description.
        
        Args:
            value: The new description for the room type
        """
        self._description = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the room type to a dictionary.
        
        Returns:
            Dict containing the room type's attributes
        """
        result = super().to_dict()
        result.update({
            "name": self._name,
            "description": self._description
        })
        return result 