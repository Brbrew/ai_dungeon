"""Predefined room types for the dungeon project."""
from .room_type import RoomType

# Standard room types
STANDARD_ROOM = RoomType(
    name="Standard Room",
    description="A basic room with no special features."
)

TREASURE_ROOM = RoomType(
    name="Treasure Room",
    description="A room containing valuable treasures and items."
)

BOSS_ROOM = RoomType(
    name="Boss Room",
    description="A room containing a powerful boss enemy."
)

PUZZLE_ROOM = RoomType(
    name="Puzzle Room",
    description="A room containing a puzzle that must be solved to proceed."
)

TRAP_ROOM = RoomType(
    name="Trap Room",
    description="A room filled with dangerous traps."
)

SECRET_ROOM = RoomType(
    name="Secret Room",
    description="A hidden room that may contain special rewards."
)

# List of all available room types
ALL_ROOM_TYPES = [
    STANDARD_ROOM,
    TREASURE_ROOM,
    BOSS_ROOM,
    PUZZLE_ROOM,
    TRAP_ROOM,
    SECRET_ROOM
] 