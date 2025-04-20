"""Direction enum for the dungeon project."""
from enum import Enum, auto

class Direction(Enum):
    """Directions for room connections."""
    
    UP = ["up"]
    DOWN = ["down"]
    NORTH = ["north"]
    SOUTH = ["south"]
    EAST = ["east"]
    WEST = ["west"]

    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def get_opposite(cls, direction: 'Direction') -> 'Direction':
        """Get the opposite direction.
        
        Args:
            direction: The direction to get the opposite of
            
        Returns:
            The opposite direction
        """
        opposites = {
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
            cls.NORTH: cls.SOUTH,
            cls.SOUTH: cls.NORTH,
            cls.EAST: cls.WEST,
            cls.WEST: cls.EAST,
        }
        return opposites[direction] 