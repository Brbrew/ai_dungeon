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

    

    THEME_ICONS = {
        "farm": "/static/img/icon/farm_icon.webp",
        "forest": "/static/img/icon/forest_icon.webp",
        "swamp": "/static/img/icon/swamp_icon.webp",
        "house": "/static/img/icon/house_icon.webp",
        "castle": "/static/img/icon/castle_icon.webp",
        "graveyard": "/static/img/icon/grave_icon.webp",
        "crypt": "/static/img/icon/grave_icon.webp",
        "mountain": "/static/img/icon/mountain_icon.webp",
        "plain": "/static/img/icon/plain_icon.webp",
        "desert": "/static/img/icon/desert_icon.webp",
        "sewer": "/static/img/icon/sewer_icon.webp",
        "cave": "/static/img/icon/cave_icon.webp",
        "village": "/static/img/icon/village_icon.webp"
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
        self.icon = self.THEME_ICONS.get(theme_name.lower(), "/static/img/icon/default_icon.webp")  # Default icon if theme not found
    
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
    
    @property
    def icon(self) -> str:
        """Get the theme's icon file path.
        
        Returns:
            The theme's icon file path
        """
        return self._icon
    
    @icon.setter
    def icon(self, value: str) -> None:
        """Set the theme's icon file path.
        
        Args:
            value: The icon file path to set
        """
        self._icon = value
    
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
            "icon": self.icon,
            "color": self.color
        } 

    def __str__(self) -> str:
        return f"{self.name} ({self.theme_type.value})"

    def __repr__(self) -> str:
        return f"Theme(theme_name='{self.name}', description='{self.description}', theme_type={self.theme_type}, music='{self.music}')" 