"""Key model for the dungeon project."""
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from .item import Item
from .action import Action, ActionType

class Key(Item):
    """A key that can be used to unlock doors."""
    
    def __init__(
        self,
        name: str,
        description: str,
        unlock_room_ref_id: str,
        detailed_description: str,
        value: float = 0.0,
        weight: float = 0.0,
        **kwargs: Any
    ) -> None:
        """Initialize a key.
        
        Args:
            name: The key's name
            description: The key's description
            unlock_room_ref_id: The reference ID of the room this key unlocks
            detailed_description: A more detailed description of the key
            value: The key's monetary value
            weight: The key's weight (must be non-negative)
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
        self._unlock_room_ref_id = unlock_room_ref_id
    
    @property
    def unlock_room_ref_id(self) -> str:
        """Get the room reference ID that this key unlocks.
        
        Returns:
            The room reference ID
        """
        return self._unlock_room_ref_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the key to a dictionary.
        
        Returns:
            Dict containing the key's attributes
        """
        return {
            **super().to_dict(),
            "unlock_room_ref_id": self.unlock_room_ref_id,
        } 