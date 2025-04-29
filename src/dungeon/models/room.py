"""Room model for the dungeon project."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID, uuid4

from .base import BaseModel
from .character import Character
from .item import Item
from .key import Key
from .room_type import RoomType
from .theme import Theme
from .trap import Trap
from .npc import NPC
from .action import Action, ActionType

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
        room_item_location: Optional[str] = None,
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
            room_item_location: Optional location description for items in the room
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
        self._room_item_location = room_item_location
        
        # Initialize collections
        self._npcs: List[Character] = []
        self._room_items: List[Dict[str, Any]] = []  # List of dicts with Item and room-specific description
        self._traps: List[Trap] = []
        self._room_npcs: List[NPC] = []
        self._connections: Dict[str, UUID] = {}
    
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
    def room_items(self) -> List[Dict[str, Any]]:
        """Get the items in the room.
        
        Returns:
            List of dictionaries containing items and their room-specific descriptions
        """
        return self._room_items.copy()
    
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
    
    def add_item(self, item: Item, room_description: str = "") -> None:
        """Add an item to the room.
        
        Args:
            item: The item to add
            room_description: Optional room-specific description of the item
        """
        self._room_items.append({
            "item": item,
            "item_room_description": room_description
        })
    
    def remove_item(self, item: Item) -> None:
        """Remove an item from the room.
        
        Args:
            item: The item to remove
        """
        self._room_items = [item_dict for item_dict in self._room_items if item_dict["item"] != item]
    
    def get_item_room_description(self, item: Item) -> str:
        """Get the room-specific description for an item.
        
        Args:
            item: The item to get the description for
            
        Returns:
            The room-specific description of the item, or empty string if not found
        """
        for item_dict in self._room_items:
            if item_dict["item"] == item:
                return item_dict["item_room_description"]
        return ""
    
    def set_item_room_description(self, item: Item, description: str) -> None:
        """Set the room-specific description for an item.
        
        Args:
            item: The item to set the description for
            description: The new room-specific description
        """
        for item_dict in self._room_items:
            if item_dict["item"] == item:
                item_dict["item_room_description"] = description
                return
        # If item not found, add it with the description
        self.add_item(item, description)
    
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
    
    @property
    def room_npcs(self) -> List[NPC]:
        """Get the NPCs in the room.
        
        Returns:
            List of NPCs in the room
        """
        return self._room_npcs.copy()
    
    def add_npc_npcs(self, npc: NPC) -> None:
        """Add an NPC to the room's NPC list.
        
        Args:
            npc: The NPC to add
        """
        self._room_npcs.append(npc)
    
    def remove_npc_npcs(self, npc: NPC) -> None:
        """Remove an NPC from the room's NPC list.
        
        Args:
            npc: The NPC to remove
        """
        self._room_npcs = [n for n in self._room_npcs if n != npc]
    
    @property
    def connections(self) -> Dict[str, UUID]:
        """Get the room's connections.
        
        Returns:
            Dictionary mapping directions to connected room IDs
        """
        return self._connections.copy()
    
    def add_connection(self, direction: str, room_id: UUID) -> None:
        """Add a connection to another room.
        
        Args:
            direction: The direction of the connection
            room_id: The ID of the connected room
        """
        self._connections[direction.lower()] = room_id
    
    def remove_connection(self, direction: str) -> None:
        """Remove a connection to another room.
        
        Args:
            direction: The direction of the connection to remove
        """
        self._connections.pop(direction.lower(), None)
    
    def get_connected_room_id(self, direction: str) -> Optional[UUID]:
        """Get the ID of the room connected in a specific direction.
        
        Args:
            direction: The direction to check
            
        Returns:
            The ID of the connected room, or None if no connection exists
        """
        return self._connections.get(direction.lower())
    
    def handle_room_action(self, action: Action) -> str:
        """Handle a room action.
        
        Args:
            action: The action to perform
            
        Returns:
            A message describing what happened
        """
        # Check if the action is a room action
        if Action.get_action_type(action) == ActionType.ROOM:
            # Handle specific room actions
            if action == Action.LOOK:
                return f"{self.description}\n\n{self._get_items_description()}\n\n{self._get_npcs_description()}\n\n{self._get_exits_description()}"
            elif action == Action.SEARCH:
                return f"You search the {self.name} thoroughly.\n\n{self._get_items_description()}\n\n{self._get_npcs_description()}"
            elif action == Action.EXAMINE:
                return f"You examine the {self.name} carefully.\n\n{self.room_direction_info}\n\n{self._get_items_description()}\n\n{self._get_npcs_description()}\n\n{self._get_exits_description()}"
        
        # For non-room actions, return a generic message
        return f"You can't {action.name.lower()} the {self.name}."
    
    def get_items_description(self) -> str:
        """Get a description of the items in the room.
        
        Returns:
            A string describing the items in the room
        """
        if not self._room_items:
            return "There's nothing here."
        
        items_desc = []
        for item_dict in self._room_items:
            item = item_dict["item"]
            room_desc = item_dict["item_room_description"]
            if room_desc:
                items_desc.append(f"{item.name} - {room_desc}")
            else:
                items_desc.append(item.name)
        
        return "You see: " + ", ".join(items_desc)
    
    def get_items_names(self) -> str:
        """Get a description of the items in the room.
        
        Returns:
            A string describing the items in the room
        """
        if not self._room_items:
            return ""
        
        items_desc = []
        for item_dict in self._room_items:
            item = item_dict["item"]
            
            if len(item.item_type) > 0:
                item_name = item.item_type
            else:
                item_name = item.name
            # use a, an, or the depending on the item
            if item_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                items_desc.append("an <span class='console-highlight'>" + item_name + "</span>")
            else:
                items_desc.append("a <span class='console-highlight'>" + item_name + "</span>")
        
        if len(items_desc) > 1:
            last_item = "and " + items_desc.pop()
            items_desc.append(last_item)
        return ", ".join(items_desc)
    
    def get_npcs_description(self) -> str:
        """Get a description of the NPCs in the room.
        
        Returns:
            A string describing the NPCs in the room
        """
        if not self._room_npcs:
            return ""
        
        npcs_desc = []
        for npc in self._room_npcs:
            npcs_desc.append(npc.name)
        
        return "Also here: " + ", ".join(npcs_desc)
    
    def get_exits_description(self) -> str:
        """Get a description of the exits from the room.
        
        Returns:
            A string describing the exits from the room
        """
        if not self._connections:
            return "There are no obvious exits."
        
        exits = []
        for direction in self._connections:
            exits.append(direction)
        
        return "Exits: " + ", ".join(exits)
    

    def get_room_details(self) -> str:
        """Get the room's details.
        
        Returns:
            A string describing the room's details
        """
        room_description = ""
        room_item_description = ""
        room_npcs = ""
        room_item_location = ""
        #room_exits = ""

        if self.get_ai_update():
            room_description = self.get_ai_description()
        else:
            room_description = self.description

        if len(self.get_items_names()) > 0:
            room_items = self.get_items_names()
            if len(self._room_item_location) > 0:
                room_item_location = self.room_item_location
                room_item_description = f"You see {room_item_location} in the room {room_items}."
            else:
                room_item_description = f"Somewhere in the room you see {room_items}."
        
        #TODO: Add NPCs and exits
        '''
        if self.room_npcs:
            room_npcs = self._get_npcs_description()

        if self.connections:
            room_exits = self._get_exits_description()
        '''
        

        return f"{room_description}\n\n{room_item_description}"
    
    
    @property
    def room_item_location(self) -> Optional[str]:
        """Get the location description for items in the room.
        
        Returns:
            The location description for items, or None if not set
        """
        return self._room_item_location
    
    @room_item_location.setter
    def room_item_location(self, value: Optional[str]) -> None:
        """Set the location description for items in the room.
        
        Args:
            value: The location description to set, or None to clear it
        """
        self._room_item_location = value
    
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
            "room_items": [
                {
                    "item_id": str(item_dict["item"].id),
                    "item_room_description": item_dict["item_room_description"]
                }
                for item_dict in self._room_items
            ],
            "traps": [str(trap.id) for trap in self._traps],
            "ai_update": self._ai_update,
            "ai_description": self._ai_description,
            "room_direction_info": self.room_direction_info,
            "room_img": self._room_img,
            "room_npcs": [npc.to_dict() for npc in self._room_npcs],
            "connections": self.connections,
            "room_item_location": self._room_item_location,
        })
        return result 