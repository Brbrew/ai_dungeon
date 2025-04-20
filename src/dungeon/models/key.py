"""Key model for the dungeon project."""
from typing import Any, Dict
from uuid import UUID

from .item import Item

class Key(Item):
    """A key that can unlock a specific room."""
    
    def __init__(
        self,
        name: str,
        description: str,
        unlocks_room_id: UUID,
        **kwargs: Any
    ) -> None:
        """Initialize a key.
        
        Args:
            name: The key's name
            description: The key's description
            unlocks_room_id: The ID of the room this key unlocks
            **kwargs: Additional arguments passed to Item
        """
        super().__init__(name, description, **kwargs)
        self._unlocks_room_id = unlocks_room_id
    
    @property
    def unlocks_room_id(self) -> UUID:
        """Get the ID of the room this key unlocks.
        
        Returns:
            The room ID this key unlocks
        """
        return self._unlocks_room_id
    
    def can_unlock(self, room_id: UUID) -> bool:
        """Check if this key can unlock a specific room.
        
        Args:
            room_id: The ID of the room to check
            
        Returns:
            True if this key can unlock the room, False otherwise
        """
        return self._unlocks_room_id == room_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the key to a dictionary.
        
        Returns:
            Dict containing the key's attributes
        """
        return {
            **super().to_dict(),
            "unlocks_room_id": str(self.unlocks_room_id),
        } 