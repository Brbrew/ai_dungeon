"""Map model for the dungeon project."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID

from .direction import Direction
from .room import Room

class Map:
    """A map of connected rooms in the dungeon."""
    
    def __init__(self) -> None:
        """Initialize an empty map."""
        # Dictionary mapping room IDs to Room objects
        self._rooms: Dict[UUID, Room] = {}
        
        # Dictionary mapping room IDs to dictionaries of directions to connected room IDs
        self._connections: Dict[UUID, Dict[Direction, UUID]] = {}
        
        # Set of room IDs that have been visited
        self._visited_rooms: Set[UUID] = set()
    
    def add_room(self, room: Room) -> None:
        """Add a room to the map.
        
        Args:
            room: The room to add
        """
        self._rooms[room.id] = room
        self._connections[room.id] = {}
    
    def remove_room(self, room_id: UUID) -> None:
        """Remove a room from the map.
        
        Args:
            room_id: The ID of the room to remove
            
        Raises:
            KeyError: If the room is not in the map
        """
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        # Remove connections to this room from other rooms
        for connected_room_id, connections in self._connections.items():
            for direction, connected_id in list(connections.items()):
                if connected_id == room_id:
                    del connections[direction]
        
        # Remove the room and its connections
        del self._rooms[room_id]
        del self._connections[room_id]
        
        # Remove from visited rooms if present
        if room_id in self._visited_rooms:
            self._visited_rooms.remove(room_id)
    
    def connect_rooms(self, room_id1: UUID, room_id2: UUID, direction: Direction) -> None:
        """Connect two rooms in a specific direction.
        
        Args:
            room_id1: The ID of the first room
            room_id2: The ID of the second room
            direction: The direction from room1 to room2
            
        Raises:
            KeyError: If either room is not in the map
            ValueError: If the rooms are already connected in that direction
        """
        print(f"DEBUG: Connecting rooms: {room_id1} {direction.value} to {room_id2}")
        
        if room_id1 not in self._rooms or room_id2 not in self._rooms:
            print(f"DEBUG: One or both rooms not found. Room1: {room_id1 in self._rooms}, Room2: {room_id2 in self._rooms}")
            print(f"DEBUG: Available room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
            raise KeyError("One or both rooms not found in map")
        
        if direction in self._connections[room_id1]:
            print(f"DEBUG: Room {room_id1} already has a connection in direction {direction.value}")
            raise ValueError(f"Room {room_id1} already has a connection in direction {direction.value}")
        
        # Add connection from room1 to room2
        self._connections[room_id1][direction] = room_id2
        
        # Add connection from room2 to room1 in the opposite direction
        opposite_direction = Direction.get_opposite(direction)
        self._connections[room_id2][opposite_direction] = room_id1
        
        print(f"DEBUG: Connection established: {room_id1} {direction.value} to {room_id2}")
        print(f"DEBUG: Reverse connection established: {room_id2} {opposite_direction.value} to {room_id1}")
    
    def disconnect_rooms(self, room_id1: UUID, room_id2: UUID) -> None:
        """Disconnect two rooms.
        
        Args:
            room_id1: The ID of the first room
            room_id2: The ID of the second room
            
        Raises:
            KeyError: If either room is not in the map
            ValueError: If the rooms are not connected
        """
        if room_id1 not in self._rooms or room_id2 not in self._rooms:
            raise KeyError("One or both rooms not found in map")
        
        # Find the direction from room1 to room2
        direction = None
        for dir, connected_id in self._connections[room_id1].items():
            if connected_id == room_id2:
                direction = dir
                break
        
        if direction is None:
            raise ValueError(f"Rooms {room_id1} and {room_id2} are not connected")
        
        # Remove connection from room1 to room2
        del self._connections[room_id1][direction]
        
        # Remove connection from room2 to room1 in the opposite direction
        opposite_direction = Direction.get_opposite(direction)
        del self._connections[room_id2][opposite_direction]
    
    def get_connected_room(self, room_id: Union[UUID, str], direction: Direction) -> Optional[Room]:
        """Get the room connected to the given room in the specified direction.
        
        Args:
            room_id: The ID of the room
            direction: The direction to check
            
        Returns:
            The connected room, or None if there is no connection
            
        Raises:
            KeyError: If the room is not in the map
        """
        # Convert string UUID to UUID object if needed
        if isinstance(room_id, str):
            try:
                room_id = UUID(room_id)
            except ValueError:
                print(f"DEBUG: Invalid UUID string: {room_id}")
                raise KeyError(f"Invalid UUID string: {room_id}")
        
        print(f"DEBUG: Getting room connected to {room_id} in direction {direction.value}")
        print(f"DEBUG: Room ID type: {type(room_id)}")
        
        # Check if the room exists by comparing string representations
        room_exists = False
        for existing_id in self._rooms.keys():
            if str(existing_id) == str(room_id):
                room_exists = True
                room_id = existing_id  # Use the existing UUID object
                break
        
        if not room_exists:
            print(f"DEBUG: Room with ID {room_id} not found in map. Available room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        connected_id = self._connections[room_id].get(direction)
        print(f"DEBUG: Connected room ID: {connected_id}")
        
        if connected_id is None:
            print(f"DEBUG: No connection found in direction {direction.value}")
            return None
        
        return self._rooms[connected_id]
    
    def get_connected_rooms(self, room_id: Union[UUID, str]) -> Dict[Direction, Room]:
        """Get all rooms connected to the given room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            A dictionary mapping directions to connected rooms
            
        Raises:
            KeyError: If the room is not in the map
        """
        # Convert string UUID to UUID object if needed
        if isinstance(room_id, str):
            try:
                room_id = UUID(room_id)
            except ValueError:
                print(f"DEBUG: Invalid UUID string: {room_id}")
                raise KeyError(f"Invalid UUID string: {room_id}")
        
        print(f"DEBUG: Getting connected rooms for room ID: {room_id} (type: {type(room_id)})")
        print(f"DEBUG: Available room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
        print(f"DEBUG: Room ID in map: {room_id in self._rooms}")
        
        # Check if the room exists by comparing string representations
        room_exists = False
        for existing_id in self._rooms.keys():
            if str(existing_id) == str(room_id):
                room_exists = True
                room_id = existing_id  # Use the existing UUID object
                break
        
        if not room_exists:
            print(f"DEBUG: Room with ID {room_id} not found in map. Available room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        print(f"DEBUG: Available connections: {[(direction.value, str(connected_id)) for direction, connected_id in self._connections[room_id].items()]}")
        
        result = {}
        for direction, connected_id in self._connections[room_id].items():
            result[direction] = self._rooms[connected_id]
        
        return result
    
    def mark_room_visited(self, room_id: UUID) -> None:
        """Mark a room as visited.
        
        Args:
            room_id: The ID of the room to mark as visited
            
        Raises:
            KeyError: If the room is not in the map
        """
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        self._visited_rooms.add(room_id)
    
    def is_room_visited(self, room_id: UUID) -> bool:
        """Check if a room has been visited.
        
        Args:
            room_id: The ID of the room to check
            
        Returns:
            True if the room has been visited, False otherwise
            
        Raises:
            KeyError: If the room is not in the map
        """
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        return room_id in self._visited_rooms
    
    def get_rooms_within_distance(self, room_id: UUID, distance: int) -> List[Tuple[Room, int]]:
        """Get all rooms within a certain distance from the given room.
        
        Args:
            room_id: The ID of the starting room
            distance: The maximum distance to search
            
        Returns:
            A list of tuples containing (room, distance) pairs
            
        Raises:
            KeyError: If the room is not in the map
        """
        if room_id not in self._rooms:
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        result = []
        visited = {room_id}
        queue = [(room_id, 0)]
        
        while queue:
            current_id, current_distance = queue.pop(0)
            
            # Add the current room to the result if it's not the starting room
            if current_id != room_id:
                result.append((self._rooms[current_id], current_distance))
            
            # If we've reached the maximum distance, stop
            if current_distance >= distance:
                continue
            
            # Add all connected rooms to the queue
            for connected_id in self._connections[current_id].values():
                if connected_id not in visited:
                    visited.add(connected_id)
                    queue.append((connected_id, current_distance + 1))
        
        return result
    
    def get_room_by_id(self, room_id: Union[UUID, str]) -> Room:
        """Get a room by its ID.
        
        Args:
            room_id: The ID of the room to get (UUID or string)
            
        Returns:
            The room with the given ID
            
        Raises:
            KeyError: If the room is not in the map
        """
        # Convert string UUID to UUID object if needed
        if isinstance(room_id, str):
            try:
                room_id = UUID(room_id)
            except ValueError:
                print(f"DEBUG: Invalid UUID string: {room_id}")
                raise KeyError(f"Invalid UUID string: {room_id}")
        
        if room_id not in self._rooms:
            print(f"DEBUG: Room with ID {room_id} not found. Available room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
            raise KeyError(f"Room with ID {room_id} not found in map")
        
        return self._rooms[room_id]
    
    def get_room_by_ref_id(self, room_ref_id: str) -> Optional[Room]:
        """Get a room by its reference ID.
        
        Args:
            room_ref_id: The reference ID of the room to get
            
        Returns:
            The room with the given reference ID, or None if not found
        """
        for room in self._rooms.values():
            if room.room_ref_id == room_ref_id:
                return room
        
        return None
    
    def get_all_rooms(self) -> List[Room]:
        """Get all rooms in the map.
        
        Returns:
            A list of all rooms in the map
        """
        return list(self._rooms.values())
    
    def get_visited_rooms(self) -> List[Room]:
        """Get all visited rooms in the map.
        
        Returns:
            A list of all visited rooms in the map
        """
        return [self._rooms[room_id] for room_id in self._visited_rooms]
    
    def get_unvisited_rooms(self) -> List[Room]:
        """Get all unvisited rooms in the map.
        
        Returns:
            A list of all unvisited rooms in the map
        """
        return [room for room_id, room in self._rooms.items() if room_id not in self._visited_rooms]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the map to a dictionary.
        
        Returns:
            Dict containing the map's attributes
        """
        rooms_dict = {str(room_id): room.to_dict() for room_id, room in self._rooms.items()}
        
        connections_dict = {}
        for room_id, connections in self._connections.items():
            connections_dict[str(room_id)] = {
                direction.value: str(connected_id)
                for direction, connected_id in connections.items()
            }
        
        visited_rooms = [str(room_id) for room_id in self._visited_rooms]
        
        return {
            "rooms": rooms_dict,
            "connections": connections_dict,
            "visited_rooms": visited_rooms
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], room_objects: Dict[str, Room]) -> 'Map':
        """Create a map from a dictionary.
        
        Args:
            data: The dictionary containing the map data
            room_objects: Dictionary mapping room IDs to Room objects
            
        Returns:
            A new Map instance
        """
        map_instance = cls()
        
        # Add rooms to the map
        for room_id, room in room_objects.items():
            map_instance._rooms[UUID(room_id)] = room
            map_instance._connections[UUID(room_id)] = {}
        
        # Add connections
        for room_id, connections in data.get("connections", {}).items():
            room_uuid = UUID(room_id)
            for direction_str, connected_id in connections.items():
                direction = Direction(direction_str)
                map_instance._connections[room_uuid][direction] = UUID(connected_id)
        
        # Add visited rooms
        for room_id in data.get("visited_rooms", []):
            map_instance._visited_rooms.add(UUID(room_id))
        
        return map_instance
    
    # Delegate Room methods to the appropriate room
    def get_room_name(self, room_id: UUID) -> str:
        """Get the name of a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            The name of the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).name
    
    def get_room_description(self, room_id: UUID) -> str:
        """Get the description of a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            The description of the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).description
    
    def get_room_theme(self, room_id: UUID) -> Any:
        """Get the theme of a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            The theme of the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).theme
    
    def get_room_type(self, room_id: UUID) -> Optional[Any]:
        """Get the type of a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            The type of the room, or None if not set
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).room_type
    
    def get_room_ref_id(self, room_id: UUID) -> str:
        """Get the reference ID of a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            The reference ID of the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).room_ref_id
    
    def get_room_npcs(self, room_id: UUID) -> List[Any]:
        """Get the NPCs in a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            A list of NPCs in the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).npcs
    
    def get_room_treasures(self, room_id: UUID) -> List[Any]:
        """Get the treasures in a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            A list of treasures in the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).treasures
    
    def get_room_traps(self, room_id: UUID) -> List[Any]:
        """Get the traps in a room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            A list of traps in the room
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).traps
    
    def is_room_dark(self, room_id: UUID) -> bool:
        """Check if a room is dark.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            True if the room is dark, False otherwise
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).is_dark
    
    def set_room_dark(self, room_id: UUID, value: bool) -> None:
        """Set whether a room is dark.
        
        Args:
            room_id: The ID of the room
            value: True if the room should be dark, False otherwise
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).is_dark = value
    
    def is_room_locked(self, room_id: UUID) -> bool:
        """Check if a room is locked.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            True if the room is locked, False otherwise
            
        Raises:
            KeyError: If the room is not in the map
        """
        return self.get_room_by_id(room_id).is_locked
    
    def lock_room(self, room_id: UUID) -> None:
        """Lock a room.
        
        Args:
            room_id: The ID of the room to lock
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).lock()
    
    def unlock_room(self, room_id: UUID, key: Optional[Any] = None) -> None:
        """Unlock a room.
        
        Args:
            room_id: The ID of the room to unlock
            key: The key to use for unlocking, or None to force unlock
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).unlock(key)
    
    def add_npc_to_room(self, room_id: UUID, npc: Any) -> None:
        """Add an NPC to a room.
        
        Args:
            room_id: The ID of the room
            npc: The NPC to add
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).add_npc(npc)
    
    def remove_npc_from_room(self, room_id: UUID, npc: Any) -> None:
        """Remove an NPC from a room.
        
        Args:
            room_id: The ID of the room
            npc: The NPC to remove
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).remove_npc(npc)
    
    def add_treasure_to_room(self, room_id: UUID, item: Any) -> None:
        """Add a treasure to a room.
        
        Args:
            room_id: The ID of the room
            item: The item to add
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).add_treasure(item)
    
    def remove_treasure_from_room(self, room_id: UUID, item: Any) -> None:
        """Remove a treasure from a room.
        
        Args:
            room_id: The ID of the room
            item: The item to remove
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).remove_treasure(item)
    
    def add_trap_to_room(self, room_id: UUID, trap: Any) -> None:
        """Add a trap to a room.
        
        Args:
            room_id: The ID of the room
            trap: The trap to add
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).add_trap(trap)
    
    def remove_trap_from_room(self, room_id: UUID, trap: Any) -> None:
        """Remove a trap from a room.
        
        Args:
            room_id: The ID of the room
            trap: The trap to remove
            
        Raises:
            KeyError: If the room is not in the map
        """
        self.get_room_by_id(room_id).remove_trap(trap) 