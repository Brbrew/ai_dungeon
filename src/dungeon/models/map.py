"""Map model for the dungeon project."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID
import math

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
        """
        room = self.get_room_by_id(room_id)
        room.remove_trap(trap)
    
    def to_svg(self, room_radius: int = 30, current_room_id: Optional[UUID] = None) -> str:
        """Generate an SVG representation of the map.
        
        Args:
            room_radius: The radius of the room circles in pixels
            current_room_id: The ID of the current room where the player is located
            
        Returns:
            An SVG string representing the map
        """
        print("\nDEBUG: Starting SVG generation...")
        print(f"DEBUG: Total rooms in map: {len(self._rooms)}")
        print(f"DEBUG: Room IDs: {[str(room_id) for room_id in self._rooms.keys()]}")
        print(f"DEBUG: Connections: {[(str(room_id), direction.value, str(connected_id)) for room_id, connections in self._connections.items() for direction, connected_id in connections.items()]}")
        
        # Get all rooms
        rooms = self.get_all_rooms()
        if not rooms:
            print("DEBUG: No rooms found in map")
            return '<svg width="100" height="100"><text x="50%" y="50%" text-anchor="middle">No rooms in map</text></svg>'
        
        print(f"DEBUG: Found {len(rooms)} rooms to place")
        
        # Calculate room positions using a simple grid layout
        # This is a basic implementation - a more sophisticated layout algorithm could be used
        room_positions = {}
        
        # Increase spacing between rooms to prevent overlapping
        #spacing = room_radius * 4  # Increased from 3 to 4
        spacing = room_radius * 3
        
        # Function to check if a position overlaps with existing rooms
        def position_overlaps(x, y, existing_positions, min_distance=room_radius*2.5):
            for pos_x, pos_y in existing_positions.values():
                distance = ((x - pos_x) ** 2 + (y - pos_y) ** 2) ** 0.5
                if distance < min_distance:
                    return True
            return False
        
        # Start with the first room at the center
        if rooms:
            center_room = rooms[0]
            room_positions[center_room.id] = (0, 0)  # Start at origin
            
            # Place other rooms relative to their connections
            placed_rooms = {center_room.id}
            rooms_to_place = [r for r in rooms if r.id != center_room.id]
            
            # Simple placement algorithm - place rooms in a grid based on their connections
            while rooms_to_place:
                for room in rooms[:]:  # Create a copy to avoid modifying during iteration
                    if room.id in placed_rooms:
                        continue
                    
                    # Find a connected room that's already placed
                    connected_placed_room = None
                    direction_to_placed = None
                    
                    for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
                        try:
                            connected_room = self.get_connected_room(room.id, direction)
                            if connected_room and connected_room.id in placed_rooms:
                                connected_placed_room = connected_room
                                direction_to_placed = direction
                                break
                        except (KeyError, ValueError):
                            continue
                    
                    if connected_placed_room:
                        # Place this room relative to the connected room
                        x, y = room_positions[connected_placed_room.id]
                        
                        # Calculate offset based on direction
                        if direction_to_placed == Direction.NORTH:
                            y += spacing
                        elif direction_to_placed == Direction.SOUTH:
                            y -= spacing
                        elif direction_to_placed == Direction.EAST:
                            x -= spacing
                        elif direction_to_placed == Direction.WEST:
                            x += spacing
                        
                        # If the position overlaps with existing rooms, try to find a nearby non-overlapping position
                        if position_overlaps(x, y, room_positions):
                            # Try positions in a spiral pattern around the original position
                            for i in range(1, 5):  # Try up to 4 alternative positions
                                for angle in range(0, 360, 90):  # Try 4 directions
                                    rad = angle * 3.14159 / 180
                                    new_x = x + i * spacing * 0.5 * math.cos(rad)
                                    new_y = y + i * spacing * 0.5 * math.sin(rad)
                                    
                                    if not position_overlaps(new_x, new_y, room_positions):
                                        x, y = new_x, new_y
                                        break
                                else:
                                    continue
                                break
                        
                        room_positions[room.id] = (x, y)
                        placed_rooms.add(room.id)
                        rooms_to_place.remove(room)
                        break
            
            # If any rooms couldn't be placed, place them in a grid pattern
            if rooms_to_place:
                print(f"DEBUG: {len(rooms_to_place)} rooms couldn't be placed by connections, using grid layout")
                grid_size = int(math.ceil(math.sqrt(len(rooms_to_place))))
                
                for i, room in enumerate(rooms_to_place):
                    row = i // grid_size
                    col = i % grid_size
                    x = col * spacing
                    y = row * spacing
                    
                    room_positions[room.id] = (x, y)
                    placed_rooms.add(room.id)
        
        # Calculate the bounds of the SVG based on room positions
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for x, y in room_positions.values():
            min_x = min(min_x, x - room_radius)
            min_y = min(min_y, y - room_radius)
            max_x = max(max_x, x + room_radius)
            max_y = max(max_y, y + room_radius)
        
        # Add padding
        padding = room_radius * 2
        min_x -= padding
        min_y -= padding
        max_x += padding
        max_y += padding
        
        # Calculate width and height
        width = max_x - min_x
        height = max_y - min_y
        
        # Adjust all positions to be relative to the top-left corner
        adjusted_positions = {}
        for room_id, (x, y) in room_positions.items():
            adjusted_positions[room_id] = (x - min_x, y - min_y)
        
        # Generate SVG
        svg = f'<?xml version="1.0" encoding="UTF-8"?><svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
        svg+= '''
            <defs>
                <style>
                .text_class {
                    font-family: ArialMT, Arial;
                    font-size: 10px;
                    isolation: isolate;
                }
                .room_circle:hover {
                    fill: #000000;
                    opacity: 0.25;
                    stroke: "#99FF00"; 
                    stroke-width: "3"; 
                    stroke-opacity: "0.25";
                }
                </style>
            </defs>'''
        # Add connections (lines)
        for room_id, connections in self._connections.items():
            if room_id in adjusted_positions:
                x1, y1 = adjusted_positions[room_id]
                
                for direction, connected_id in connections.items():
                    # Skip UP and DOWN directions as requested
                    if direction in [Direction.UP, Direction.DOWN]:
                        continue
                    
                    if connected_id in adjusted_positions:
                        x2, y2 = adjusted_positions[connected_id]
                        
                        # Draw a line from room to connected room
                        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2" />'
        
        # Add rooms (circles)
        for room_id, (x, y) in adjusted_positions.items():
            room = self._rooms[room_id]
            
            # Get the theme color from the room's theme
            theme_color = room.theme.color if hasattr(room.theme, 'color') else "white"
            
            # Determine fill color based on whether the room has been visited
            # Use a lighter version of the theme color for visited rooms
            fill_color = theme_color if room_id in self._visited_rooms else "white"
            
            # Draw the room circle
            svg += f'<circle class="room_circle" cx="{x}" cy="{y}" r="{room_radius}" fill="{fill_color}" stroke="black" stroke-width="3" stroke-opacity="0.25"/>'
            

            # Add player triangle if this is the current room
            # This will place the icon below the text
            if current_room_id and room_id == current_room_id:
                # Calculate triangle points (smaller than the room circle)
                triangle_size = room_radius * 0.3
                triangle_offset = y + (room_radius * 1) # offset the triangle down by 1 room radius, using 1 for now
                triangle_points = f"{x},{triangle_offset-triangle_size} {x-triangle_size},{triangle_offset+triangle_size} {x+triangle_size},{triangle_offset+triangle_size}"
                svg += f'<polygon points="{triangle_points}" fill="#99FF00" stroke="black" stroke-width="1" stroke-opacity="0.25"/>'
        
            # Add room name
            room_name = room.name
            
            #add line break to room names
            y_step = 0
            y_offset = 0
            room_word_count = room_name.count(" ")

            #offset the text to the center of the room
            if room_word_count > 0:
                y_offset = 14 * (room_word_count -1)

            room_text_output = ""
            for word in room_name.split(" "):
            
                room_text_output += f'<tspan x="{x}" dy="{y_step}px">{word.strip()}</tspan>'
                y_step = 14

            svg += f'<text x="{x}" y="{y-y_offset}" text-anchor="middle" class="text_class">{room_text_output}</text>'
            
            
        svg += '</svg>'
        return svg 
    
