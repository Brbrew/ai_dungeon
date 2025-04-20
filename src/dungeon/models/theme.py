"""Theme model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .base import BaseModel

class Theme(BaseModel):
    """A theme for a room in the dungeon."""
    
    def __init__(
        self,
        name: str,
        description: str,
        **kwargs: Any
    ) -> None:
        """Initialize a theme.
        
        Args:
            name: The theme's name
            description: The theme's description
            **kwargs: Additional arguments passed to BaseModel
        """
        super().__init__(**kwargs)
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """Get the theme's name.
        
        Returns:
            The theme's name
        """
        return self._name
    
    @property
    def description(self) -> str:
        """Get the theme's description.
        
        Returns:
            The theme's description
        """
        return self._description
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the theme to a dictionary.
        
        Returns:
            Dict containing the theme's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "description": self.description,
        } 