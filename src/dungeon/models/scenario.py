"""Scenario model for managing dungeon scenarios."""
from typing import Dict, List, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class Scenario(BaseModel):
    """A class representing a dungeon scenario.
    
    This class defines a scenario that can be loaded into a dungeon.
    A scenario includes a name, description, welcome message, and difficulty level.
    """
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = "Default Scenario"
    description: str = "A default scenario"
    welcome_message: str = "Welcome to the dungeon!"
    difficulty: str = "medium"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the scenario to a dictionary.
        
        Returns:
            A dictionary representation of the scenario
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "welcome_message": self.welcome_message,
            "difficulty": self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scenario':
        """Create a scenario from a dictionary.
        
        Args:
            data: The dictionary to create the scenario from
            
        Returns:
            A new scenario instance
        """
        return cls(
            id=data.get("id", str(uuid4())),
            name=data.get("name", "Default Scenario"),
            description=data.get("description", "A default scenario"),
            welcome_message=data.get("welcome_message", "Welcome to the dungeon!"),
            difficulty=data.get("difficulty", "medium")
        )
    
    def get_name(self) -> str:
        """Get the name of the scenario.
        
        Returns:
            The name of the scenario
        """
        return self.name
    
    def set_name(self, value: str) -> None:
        """Set the name of the scenario.
        
        Args:
            value: The new name
        """
        self.name = value
    
    def get_description(self) -> str:
        """Get the description of the scenario.
        
        Returns:
            The description of the scenario
        """
        return self.description
    
    def set_description(self, value: str) -> None:
        """Set the description of the scenario.
        
        Args:
            value: The new description
        """
        self.description = value
    
    def get_welcome_message(self) -> str:
        """Get the welcome message of the scenario.
        
        Returns:
            The welcome message of the scenario
        """
        return self.welcome_message
    
    def set_welcome_message(self, value: str) -> None:
        """Set the welcome message of the scenario.
        
        Args:
            value: The new welcome message
        """
        self.welcome_message = value
    
    def get_difficulty(self) -> str:
        """Get the difficulty of the scenario.
        
        Returns:
            The difficulty of the scenario
        """
        return self.difficulty
    
    def set_difficulty(self, value: str) -> None:
        """Set the difficulty of the scenario.
        
        Args:
            value: The new difficulty
        """
        self.difficulty = value
    
    def get_enabled(self) -> bool:
        """Get whether the scenario is enabled.
        
        Returns:
            True if the scenario is enabled, False otherwise
        """
        return self.enabled
    
    def set_enabled(self, value: bool) -> None:
        """Set whether the scenario is enabled.
        
        Args:
            value: True to enable the scenario, False to disable
        """
        self.enabled = value
    
    def get_filename(self) -> str:
        """Get the filename of the scenario.
        
        Returns:
            The filename of the scenario
        """
        return self.filename
    
    def set_filename(self, value: str) -> None:
        """Set the filename of the scenario.
        
        Args:
            value: The new filename
        """
        self.filename = value 