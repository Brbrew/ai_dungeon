#!/usr/bin/env python3
"""
Update Dungeon AI Descriptions

This script takes a dungeon JSON file as input, uses the room_description_generate
function from ai_generator.py to update the ai_description field for each room,
and saves the result to a new file with '_ai' appended to the original filename.

Usage:
    python update_dungeon_ai.py <dungeon_json_file>

Example:
    python update_dungeon_ai.py mysterious_land.json
    # Creates mysterious_land_ai.json with updated AI descriptions
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the src directory to the Python path so we can import the dungeon modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dungeon.models.ai_generator import AIGenerator
from src.dungeon.models.room import Room
from src.dungeon.models.theme import Theme
from src.dungeon.models.room_type import RoomType


def load_dungeon_json(file_path):
    """Load a dungeon JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading dungeon JSON file: {e}")
        sys.exit(1)


def save_dungeon_json(dungeon_data, file_path):
    """Save a dungeon JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(dungeon_data, f, indent=2)
        print(f"Saved updated dungeon to {file_path}")
    except Exception as e:
        print(f"Error saving dungeon JSON file: {e}")
        sys.exit(1)


def create_room_object(room_data, themes):
    """Create a Room object from room data."""
    # Find the theme object
    theme_name = room_data.get('theme', '')
    theme_data = next((t for t in themes if t['name'] == theme_name), None)
    theme = Theme(theme_data['name'], theme_data['description'], theme_data['theme_type'], theme_data['music']) if theme_data else None
    
    # Create a RoomType object with both name and description
    room_type_name = room_data.get('room_type', '')
    room_type = RoomType(
        name=room_type_name,
        description=f"A {room_type_name} room"
    ) if room_type_name else None
    
    # Create a Room object
    room = Room(
        name=room_data.get('name', ''),
        description=room_data.get('description', ''),
        theme=theme,
        room_type=room_type,
        room_ref_id=room_data.get('room_ref_id', ''),
        is_dark=room_data.get('is_dark', False),
        is_locked=room_data.get('is_locked', False)
    )
    
    return room


def update_dungeon_ai(dungeon_file):
    """Update the AI descriptions in a dungeon JSON file."""
    # Load the dungeon JSON file
    dungeon_data = load_dungeon_json(dungeon_file)
    
    # Initialize the AI generator
    ai_generator = AIGenerator()
    
    # Get the themes
    themes = dungeon_data.get('themes', [])
    
    # Update each room with AI-generated descriptions
    for room in dungeon_data['map']['rooms']:
        room_ref_id = room.get('room_ref_id', '')
        if not room_ref_id:
            print(f"Warning: Room {room.get('name', 'Unknown')} has no room_ref_id, skipping")
            continue
        
        # Create a Room object for the AI generator
        room_obj = create_room_object(room, themes)
        
        # Generate an AI description
        print(f"Generating AI description for room: {room_obj.name} ({room_ref_id})")
        ai_description = ai_generator.room_description_generate(room_ref_id, room_obj)
        
        # Update the room data
        room['ai_description'] = ai_description
        room['ai_update'] = True
    
    # Create the output file path
    file_path = Path(dungeon_file)
    output_file = file_path.parent / f"{file_path.stem}_ai{file_path.suffix}"
    
    # Save the updated dungeon data
    save_dungeon_json(dungeon_data, output_file)
    
    return output_file


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Update dungeon AI descriptions')
    parser.add_argument('dungeon_file', help='Path to the dungeon JSON file')
    args = parser.parse_args()
    
    # Check if the file exists
    if not os.path.exists(args.dungeon_file):
        print(f"Error: File {args.dungeon_file} does not exist")
        sys.exit(1)
    
    # Update the dungeon AI descriptions
    output_file = update_dungeon_ai(args.dungeon_file)
    print(f"Successfully updated dungeon AI descriptions to {output_file}")


if __name__ == '__main__':
    main() 