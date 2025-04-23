"""Theme model for the dungeon project."""
from typing import Any, Dict, Optional, Literal
from uuid import UUID, uuid4
from enum import Enum

from .base import BaseModel

class ThemeType(Enum):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"

class Theme(BaseModel):
    """A theme for a room in the dungeon."""
    
    THEME_COLORS = {
        "farm": "Khaki",
        "forest": "ForestGreen",
        "swamp": "DarkOliveGreen",
        "house": "Peru",
        "castle": "SlateGray",
        "graveyard": "Purple",
        "crypt": "DarkSlateBlue",
        "mountain": "LightSteelBlue",
        "plain": "YellowGreen",
        "desert": "Tan",
        "sewer": "MediumSeaGreen",
        "cave": "SaddleBrown"
    }
    
    def __init__(
        self,
        theme_name: str,
        description: str,
        theme_type: ThemeType = ThemeType.OUTDOOR,
        music: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Initialize a theme.
        
        Args:
            theme_name: The theme's name
            description: The theme's description
            theme_type: The type of theme (Exterior, Interior, or Underground)
            music: Optional music file path for this theme
            **kwargs: Additional arguments passed to BaseModel
        """
        super().__init__(**kwargs)
        self._name = theme_name
        self._description = description
        self._type = theme_type
        self._music = music
        self.color = self.THEME_COLORS.get(theme_name.lower(), "Gray")  # Default to Gray if theme not found
    
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
    
    @property
    def theme_type(self) -> ThemeType:
        """Get the theme's type.
        
        Returns:
            The theme's type (Exterior, Interior, or Underground)
        """
        return self._type
    
    @property
    def music(self) -> Optional[str]:
        """Get the theme's music file path.
        
        Returns:
            The theme's music file path, or None if no music is set
        """
        return self._music
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the theme to a dictionary.
        
        Returns:
            Dict containing the theme's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "description": self.description,
            "theme_type": self.theme_type,
            "music": self.music,
        } 

    def __str__(self) -> str:
        return f"{self.name} ({self.theme_type.value})"

    def __repr__(self) -> str:
        return f"Theme(theme_name='{self.name}', description='{self.description}', theme_type={self.theme_type}, music='{self.music}')" 