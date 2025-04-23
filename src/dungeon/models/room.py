"""Room model for the dungeon project."""
from typing import Any, Dict, List, Optional
from uuid import UUID

from .base import BaseModel
from .character import Character
from .item import Item
from .key import Key
from .room_type import RoomType
from .theme import Theme
from .trap import Trap

class RoomLockError(Exception):
    """Exception raised when there are issues with room locking/unlocking."""
    pass

class Room(BaseModel):
    """A room in the dungeon."""
    
    def __init__(
        self,
        name: str,
        description: str,
        theme: Theme,
        room_ref_id: str,
        room_type: Optional[RoomType] = None,
        is_dark: bool = False,
        is_locked: bool = False,
        ai_update: bool = False,
        ai_description: str = "",
        room_direction_info: str = "",
        room_img: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Initialize a room.
        
        Args:
            name: The room's name
            description: The room's description
            theme: The room's theme
            room_ref_id: Human-readable reference ID for initial room connections
            room_type: The type of room (e.g., treasure room, boss room, etc.)
            is_dark: Whether the room is dark
            is_locked: Whether the room is locked
            ai_update: Whether the room's AI update flag is set
            ai_description: The room's AI description
            room_direction_info: Additional information about the room's direction
            room_img: Optional image file path for this room
            **kwargs: Additional arguments passed to BaseModel
        """
        super().__init__(**kwargs)
        self._name = name
        self._description = description
        self._theme = theme
        self._room_ref_id = room_ref_id
        self._room_type = room_type
        self._is_dark = bool(is_dark)
        self._is_locked = bool(is_locked)
        self._ai_update = ai_update
        self._ai_description = ai_description
        self.room_direction_info = room_direction_info
        self._room_img = room_img
        
        # Initialize collections
        self._npcs: List[Character] = []
        self._treasures: List[Item] = []
        self._traps: List[Trap] = []
    
    @property
    def name(self) -> str:
        """Get the room's name.
        
        Returns:
            The room's name
        """
        return self._name
    
    @property
    def description(self) -> str:
        """Get the room's description.
        
        Returns:
            The room's description
        """
        return self._description
    
    @property
    def theme(self) -> Theme:
        """Get the room's theme.
        
        Returns:
            The room's theme
        """
        return self._theme
    
    @property
    def room_type(self) -> Optional[RoomType]:
        """Get the room's type.
        
        Returns:
            The room's type, or None if not set
        """
        return self._room_type
    
    @room_type.setter
    def room_type(self, value: Optional[RoomType]) -> None:
        """Set the room's type.
        
        Args:
            value: The room type to set, or None to clear it
        """
        self._room_type = value
    
    @property
    def room_ref_id(self) -> str:
        """Get the room's reference ID.
        
        Returns:
            The room's human-readable reference ID
        """
        return self._room_ref_id
    
    @property
    def npcs(self) -> List[Character]:
        """Get the room's NPCs.
        
        Returns:
            A copy of the room's NPCs
        """
        return self._npcs.copy()
    
    @property
    def treasures(self) -> List[Item]:
        """Get the room's treasures.
        
        Returns:
            A copy of the room's treasures
        """
        return self._treasures.copy()
    
    @property
    def traps(self) -> List[Trap]:
        """Get the room's traps.
        
        Returns:
            A copy of the room's traps
        """
        return self._traps.copy()
    
    @property
    def is_dark(self) -> bool:
        """Get whether the room is dark.
        
        Returns:
            True if the room is dark, False otherwise
        """
        return self._is_dark
    
    @is_dark.setter
    def is_dark(self, value: bool) -> None:
        """Set whether the room is dark.
        
        Args:
            value: True if the room should be dark, False otherwise
        """
        self._is_dark = bool(value)
    
    @property
    def is_locked(self) -> bool:
        """Get whether the room is locked.
        
        Returns:
            True if the room is locked, False otherwise
        """
        return self._is_locked
    
    def lock(self) -> None:
        """Lock the room."""
        self._is_locked = True
    
    def unlock(self, key: Optional[Key] = None) -> None:
        """Unlock the room.
        
        Args:
            key: The key to use for unlocking. If None, force unlock the room.
            
        Raises:
            RoomLockError: If the key cannot unlock this room
        """
        if key is not None and not key.can_unlock(self.id):
            raise RoomLockError(f"Key {key.name} cannot unlock this room")
        self._is_locked = False
    
    def add_npc(self, npc: Character) -> None:
        """Add an NPC to the room.
        
        Args:
            npc: The NPC to add
        """
        self._npcs.append(npc)
    
    def remove_npc(self, npc: Character) -> None:
        """Remove an NPC from the room.
        
        Args:
            npc: The NPC to remove
            
        Raises:
            ValueError: If the NPC is not in the room
        """
        try:
            self._npcs.remove(npc)
        except ValueError:
            raise ValueError(f"NPC {npc.name} not found in room")
    
    def add_treasure(self, item: Item) -> None:
        """Add a treasure to the room.
        
        Args:
            item: The item to add
        """
        self._treasures.append(item)
    
    def remove_treasure(self, item: Item) -> None:
        """Remove a treasure from the room.
        
        Args:
            item: The item to remove
            
        Raises:
            ValueError: If the item is not in the room
        """
        try:
            self._treasures.remove(item)
        except ValueError:
            raise ValueError(f"Item {item.name} not found in room")
    
    def add_trap(self, trap: Trap) -> None:
        """Add a trap to the room.
        
        Args:
            trap: The trap to add
        """
        self._traps.append(trap)
    
    def remove_trap(self, trap: Trap) -> None:
        """Remove a trap from the room.
        
        Args:
            trap: The trap to remove
            
        Raises:
            ValueError: If the trap is not in the room
        """
        try:
            self._traps.remove(trap)
        except ValueError:
            raise ValueError(f"Trap {trap.name} not found in room")
    
    def get_ai_update(self) -> bool:
        """Get the current value of ai_update."""
        return self._ai_update
    
    def set_ai_update(self, value: bool) -> None:
        """Set the value of ai_update."""
        self._ai_update = value
        print(f"DEBUG: ai_update set to {value} for room {self.name}")
    
    def get_ai_description(self) -> str:
        """Get the current value of ai_description."""
        return self._ai_description
    
    def set_ai_description(self, value: str) -> None:
        """Set the value of ai_description."""
        self._ai_description = value
        print(f"DEBUG: ai_description set to '{value}' for room {self.name}")
    
    def get_room_direction_info(self) -> str:
        """Get the current value of room_direction_info."""
        return self.room_direction_info
    
    def set_room_direction_info(self, value: str) -> None:
        """Set the room's direction information.
        
        Args:
            value: The room's direction information
        """
        self.room_direction_info = value
    
    @property
    def room_img(self) -> Optional[str]:
        """Get the room's image file path.
        
        Returns:
            The room's image file path, or None if not set
        """
        return self._room_img
    
    @room_img.setter
    def room_img(self, value: Optional[str]) -> None:
        """Set the room's image file path.
        
        Args:
            value: The room's image file path, or None to clear
        """
        self._room_img = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the room to a dictionary.
        
        Returns:
            Dict containing the room's attributes
        """
        result = super().to_dict()
        result.update({
            "name": self._name,
            "description": self._description,
            "theme_id": str(self._theme.id),
            "room_type_id": str(self._room_type.id) if self._room_type else None,
            "room_ref_id": self._room_ref_id,
            "is_dark": self._is_dark,
            "is_locked": self._is_locked,
            "npcs": [str(npc.id) for npc in self._npcs],
            "treasures": [str(item.id) for item in self._treasures],
            "traps": [str(trap.id) for trap in self._traps],
            "ai_update": self._ai_update,
            "ai_description": self._ai_description,
            "room_direction_info": self.room_direction_info,
            "room_img": self._room_img
        })
        return result 