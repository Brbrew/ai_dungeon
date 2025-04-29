"""Scroll model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .item import Item
from .action import Action, ActionType

class Scroll(Item):
    """A scroll that can be read."""
    
    def __init__(
        self,
        name: str,
        description: str,
        detailed_description: str,
        scroll_text: str,
        value: float = 0.0,
        weight: float = 0.0,
        **kwargs: Any
    ) -> None:
        """Initialize a scroll.
        
        Args:
            name: The scroll's name
            description: The scroll's description
            detailed_description: A more detailed description of the scroll
            scroll_text: The text written on the scroll
            value: The scroll's monetary value
            weight: The scroll's weight (must be non-negative)
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
        self._scroll_text = scroll_text
    
    @property
    def scroll_text(self) -> str:
        """Get the text written on the scroll.
        
        Returns:
            The scroll's text content
        """
        return self._scroll_text
    
    def _handle_read(self) -> str:
        """Handle the READ action on this scroll.
        
        Returns:
            A message containing the scroll's text
        """
        return f"You read the scroll:\n\n{self.scroll_text}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the scroll to a dictionary.
        
        Returns:
            Dict containing the scroll's attributes
        """
        return {
            **super().to_dict(),
            "scroll_text": self.scroll_text,
        } 