"""Dungeon model for managing a dungeon instance."""
import json
import uuid
import itertools
from typing import Dict, List, Any, Optional, Union
from decimal import Decimal
import os
from pathlib import Path
from nltk.tokenize import word_tokenize
from uuid import UUID
import random
import re

from .character import Character
from .map import Map, Direction
from .room import Room
from .theme import Theme
from .weapon import Weapon, WeaponType
from .armor import Armor, ArmorType
from .npc import NPC
from .item import Item
from .key import Key
from .potion import Potion
from .scroll import Scroll
from .action import Action
from .room_type import RoomType
from .ai_generator import AIGenerator
from .scenario import Scenario
from .action_type import ActionType


class Dungeon:
    """A class representing a dungeon instance.
    
    This class manages all aspects of a dungeon, including:
    - Characters (players and NPCs)
    - Enemies
    - A single map with rooms
    - Items and equipment
    - Themes
    
    It can load a dungeon from a JSON file or generate one using external services.
    """
    
    def __init__(self, name: str = "New Dungeon", description: str = "A mysterious dungeon", load_sample: bool = True, session_id: Optional[str] = None):
        """Initialize a new dungeon.
        
        Args:
            name: The name of the dungeon
            description: A description of the dungeon
            load_sample: Whether to load the sample dungeon by default
            session_id: The session ID associated with this dungeon
        """
        self.id = str(uuid.uuid4())
        self.dungeon_file = "mysterious_land_ai.json"  # mysterious_land.json
        self.session_id = session_id
        self.ai_enabled = False  # Initialize ai_enabled to True
        self.ai_generator = AIGenerator()  # Initialize the AI generator
        self.score = 0  # Initialize player score to 0
        self.scenario = None  # Initialize scenario to None

        # Player data
        self.player_character: Optional[Character] = None  # Will be initialized when username is provided
        self.npcs: Dict[str, NPC] = {}  # Dictionary to store NPCs
        self.enemies: Dict[str, NPC] = {}  # Dictionary to store enemies
        self.items: Dict[str, Item] = {}  # Dictionary to store items
        
        # Collections to store dungeon entities
        # NPC
        # ENEMY
        # ITEM

        self.map: Optional[Map] = None  # Single map for the dungeon
        self.themes: Dict[str, Theme] = {}
        
        # Current game state
        self.current_room_id: Optional[str] = None
        self.current_room: Optional[Room] = None  # Direct reference to the current room object
        
        # Load sample dungeon
        if load_sample:
            self.load_dungeon()
        
    def load_dungeon(self) -> None:
        """Load a dungeon from a JSON file."""
        try:
            # Get the path to the dungeon file
            dungeon_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "dungeon", "api", "dungeons", self.dungeon_file
            )
            
            # Check if the dungeon file exists
            if not os.path.exists(dungeon_path):
                print(f"DEBUG: Dungeon file not found: {dungeon_path}")
                return
            
            print(f"DEBUG: Loading dungeon file: {dungeon_path}")
            
            # Load the dungeon file
            with open(dungeon_path, 'r') as f:
                dungeon_data = json.load(f)
            
            # Create an initial scenario
            self.scenario = Scenario()
            print(f"DEBUG: Created initial scenario: {self.scenario.name} ({self.scenario.difficulty})")
            
            # Update the scenario if scenario data is present
            if "scenario" in dungeon_data:
                scenario_data = dungeon_data["scenario"]
                self.scenario.set_name(scenario_data.get("name", self.scenario.get_name()))
                self.scenario.set_description(scenario_data.get("description", self.scenario.get_description()))
                self.scenario.set_welcome_message(scenario_data.get("welcome_message", self.scenario.get_welcome_message()))
                self.scenario.set_difficulty(scenario_data.get("difficulty", self.scenario.get_difficulty()))
                print(f"DEBUG: Updated scenario: {self.scenario.get_name()} ({self.scenario.get_difficulty()})")
            
            # Create a new map
            self.map = Map()
            
            # Load themes first
            for theme_data in dungeon_data.get("themes", []):
                theme_name = theme_data.get("name", "default").lower()
                theme_description = theme_data.get("description", f"A {theme_name} themed area")
                theme = Theme(
                    theme_name=theme_name,
                    description=theme_description,
                    theme_type=theme_data.get("type", "Interior").lower(),
                    default_img=theme_data.get("default_img", ""),
                    music=theme_data.get("music", "")
                )
                self.themes[theme_name] = theme
                print(f"DEBUG: Created theme: {theme_name} ({theme.theme_type})")
            
            # Create room objects
            room_objects = {}
            for room_data in dungeon_data.get("map", {}).get("rooms", []):
                room_ref_id = room_data.get("room_ref_id")
                if not room_ref_id:
                    print(f"DEBUG: Skipping room without room_ref_id: {room_data.get('name')}")
                    continue
                
                print(f"DEBUG: Creating room: {room_data.get('name')} ({room_ref_id})")
                
                # Get theme from room data or use default
                theme_name = room_data.get("theme", "default").lower()
                theme = self.themes.get(theme_name)
                if not theme:
                    print(f"DEBUG: Theme {theme_name} not found, using default theme")
                    theme = Theme(theme_name="default", description="A default themed area")
                    self.themes["default"] = theme
                
                #Use AI description if available
                if "ai_description" in room_data:
                    room_description = room_data["description"] = room_data["ai_description"]
                else:
                    room_description = room_data["description"]

                # Get room item location
                if "room_item_location" in room_data:
                    room_item_location = room_data["room_item_location"]
                else:
                    room_item_location = ""

                # Create the room object first
                room = Room(
                    name=room_data["name"],
                    description=room_description,
                    theme=theme,
                    room_ref_id=room_ref_id,
                    room_type=RoomType(name=room_data["room_type"].lower(), description=f"A {room_data['room_type'].lower()} room") if "room_type" in room_data else None,
                    is_dark=room_data.get("is_dark", False),
                    is_locked=room_data.get("is_locked", False),
                    room_img=room_data.get("room_img", ""),
                    room_item_location=room_item_location
                )

                # Now add items to the room
                if "room_items" in room_data:
                    room_items = room_data["room_items"]
                    for item_data in room_items:
                        item_type = item_data.get("item_type", "")
                        item_name = item_data.get("name", "")
                        item_description = item_data.get("description", "")
                        item_detailed_description = item_data.get("detailed_description", "")
                        item_alias = item_data.get("alias", [])
                        item_room_description = item_data.get("item_room_description", "")
                        
                        # Create the appropriate item subclass based on type
                        if item_type == "key":
                            unlock_room_ref_id = item_data.get("unlock_room_ref_id", "")
                            item = Key(
                                name=item_name,
                                item_type=item_type,
                                description=item_description,
                                unlock_room_ref_id=unlock_room_ref_id,
                                detailed_description=item_detailed_description,
                                alias=item_alias
                            )
                        elif item_type == "potion": 
                            potion_text = item_data.get("potion_text", "")
                            smell_description = item_data.get("smell_description", "It has a strange smell.")
                            item = Potion(
                                name=item_name,
                                item_type=item_type,
                                description=item_description,
                                detailed_description=item_detailed_description,
                                effects=potion_text,
                                smell_description=smell_description,
                                alias=item_alias
                            )
                        elif item_type == "scroll":
                            scroll_text = item_data.get("scroll_text", "")
                            item = Scroll(
                                name=item_name,
                                item_type=item_type,
                                description=item_description,
                                detailed_description=item_detailed_description,
                                scroll_text=scroll_text,
                                alias=item_alias
                            )
                        else:
                            # Default to generic Item if type is not recognized
                            item = Item(
                                name=item_name,
                                item_type="something",
                                description=item_description,
                                detailed_description=item_detailed_description,
                                alias=item_alias
                            )
                        
                        # Add the item to the room
                        room.add_item(item, item_room_description)
                else:
                    room_items = []

                print(f"DEBUG: Room created with room_id: {room.id} and theme: {theme.name}")
                room_objects[room_ref_id.lower()] = room
                self.map.add_room(room)
            
            print(f"DEBUG: Created {len(room_objects)} room objects")
            
            # Generate AI Room Descriptions
            if self.ai_enabled:
                for room in self.map.get_all_rooms():
                    room.set_ai_description(self.ai_generator.room_description_generate(room.id, room))
                    room.set_ai_update(True)
            
            # Debug output of all rooms in the map
            all_rooms = self.map.get_all_rooms()
            print(f"DEBUG: All rooms in map: {[(room.name, room.id) for room in all_rooms]}")
            
            # Set the current room to the first room in the list
            if room_objects:
                first_room = list(room_objects.values())[0]
                self.current_room_id = str(first_room.id)
                print(f"DEBUG: Set the current room to: {first_room.name} (ID: {first_room.id})")
                
                self.set_current_room(self.current_room_id)

                # Mark the first room as visited
                try:
                    self.map.mark_room_visited(first_room.id)
                    print(f"DEBUG: Marked the first room as visited: {first_room.name}")
                except KeyError as e:
                    print(f"DEBUG: Error marking first room as visited: {e}")
            
            # Connect rooms using the connections from the dungeon file
            print("\nDEBUG: Starting room connections...")
            for room_ref_id, connections in dungeon_data.get("map", {}).get("connections", {}).items():
                room_ref_id = room_ref_id.lower()  # Ensure lowercase
                print(f"\nDEBUG: Processing connections for room_ref_id: {room_ref_id}")
                if room_ref_id in room_objects:
                    room = room_objects[room_ref_id]
                    print(f"DEBUG: Found room object: {room.name} (ID: {room.id})")
                    for direction_str, target_ref_id in connections.items():
                        target_ref_id = target_ref_id.lower()  # Ensure lowercase
                        print(f"DEBUG: Processing connection: {direction_str} -> {target_ref_id}")
                        if target_ref_id in room_objects:
                            direction = Direction[direction_str.upper()]
                            try:
                                # First try to disconnect any existing connection in this direction
                                if direction in self.map._connections[room.id]:
                                    old_target_id = self.map._connections[room.id][direction]
                                    # Remove the old connection from both rooms
                                    del self.map._connections[room.id][direction]
                                    opposite_direction = Direction.get_opposite(direction)
                                    if opposite_direction in self.map._connections[old_target_id]:
                                        del self.map._connections[old_target_id][opposite_direction]
                                    print(f"DEBUG: Removed old connection from {room.name} {direction_str} to {self.map._rooms[old_target_id].name}")
                                
                                # Now create the new connection
                                self.map.connect_rooms(room.id, room_objects[target_ref_id].id, direction)
                                print(f"DEBUG: Successfully connected {room.name} {direction_str} to {room_objects[target_ref_id].name}")
                            except (KeyError, ValueError) as e:
                                print(f"DEBUG: Error connecting rooms: {e}")
                                continue
                        else:
                            print(f"DEBUG: Target room {target_ref_id} not found in room_objects")
                else:
                    print(f"DEBUG: Room {room_ref_id} not found in room_objects")
            
            # Debug output: show all connected rooms for each room
            print("\nDEBUG: Final room connections:")
            for room in self.map.get_all_rooms():
                try:
                    connected = self.map.get_connected_rooms(room.id)
                    connections_str = ', '.join([f"{direction.value[0]} -> {connected_room.name}" for direction, connected_room in connected.items()])
                    print(f"DEBUG: {room.name} ({room.id}): {connections_str if connections_str else 'No connections'}")
                except Exception as e:
                    print(f"DEBUG: Error getting connections for {room.name}: {e}")
            
            # Populate room_direction_info for each room
            print("DEBUG: Populating room_direction_info for each room")
            for room in self.map.get_all_rooms():
                connected_rooms = self.map.get_connected_rooms(room.id)
                
                # Create descriptive room direction info based on connected rooms and their themes
                if connected_rooms:
                    direction_descriptions = []
                    for direction, connected_room in connected_rooms.items():
                        room_type_name = connected_room.room_type.name.lower() if connected_room.room_type else "room"
                        room_theme = connected_room.theme.name.lower() if connected_room.theme else "room"

                        direction_descriptions.append(f"There is a <span class='console-highlight'>{room_theme}</span> to the <span class='console-highlight'>{direction.value[0]}</span>")
                    room_direction_info = ". ".join(direction_descriptions) + "."
                else:
                    room_direction_info = "There are no exits from this room."
                
                # Set the room_direction_info
                room.set_room_direction_info(room_direction_info)
                print(f"DEBUG: Set room_direction_info for {room.name}: {room_direction_info}")
            
            print(f"DEBUG: Dungeon loaded successfully: {self.scenario.name}")
        except Exception as e:
            print(f"DEBUG: Error loading dungeon: {e}")
    
    
    def add_npc(self, npc: NPC) -> str:
        """Add an NPC to the dungeon.
        
        Args:
            npc: The NPC to add
            
        Returns:
            The ID of the added NPC
        """
        npc_id = str(npc.id)
        self.npcs[npc_id] = npc
        return npc_id
    
    def add_enemy(self, enemy: NPC) -> str:
        """Add an enemy to the dungeon.
        
        Args:
            enemy: The enemy to add
            
        Returns:
            The ID of the added enemy
        """
        enemy_id = str(enemy.id)
        self.enemies[enemy_id] = enemy
        return enemy_id
    
    def set_map(self, map_obj: Map) -> None:
        """Set the dungeon map.
        
        Args:
            map_obj: The map to set
        """
        self.map = map_obj
    
    def add_theme(self, theme: Theme) -> str:
        """Add a theme to the dungeon.
        
        Args:
            theme: The theme to add
            
        Returns:
            The ID of the added theme
        """
        theme_id = str(theme.id)
        self.themes[theme_id] = theme
        return theme_id
    
    def add_item(self, item: Item) -> str:
        """Add an item to the dungeon.
        
        Args:
            item: The item to add
            
        Returns:
            The ID of the added item
        """
        item_id = str(item.id)
        self.items[item_id] = item
        return item_id
    
    
    def get_npc(self, npc_id: str) -> NPC:
        """Get an NPC by ID.
        
        Args:
            npc_id: The ID of the NPC to get
            
        Returns:
            The NPC with the given ID
            
        Raises:
            KeyError: If no NPC with the given ID exists
        """
        if npc_id not in self.npcs:
            raise KeyError(f"No NPC with ID {npc_id} exists")
        return self.npcs[npc_id]
    
    def get_enemy(self, enemy_id: str) -> NPC:
        """Get an enemy by ID.
        
        Args:
            enemy_id: The ID of the enemy to get
            
        Returns:
            The enemy with the given ID
            
        Raises:
            KeyError: If no enemy with the given ID exists
        """
        if enemy_id not in self.enemies:
            raise KeyError(f"No enemy with ID {enemy_id} exists")
        return self.enemies[enemy_id]
    
    def get_map(self) -> Map:
        """Get the dungeon map.
        
        Returns:
            The dungeon map
            
        Raises:
            ValueError: If no map has been set
        """
        if self.map is None:
            raise ValueError("No map has been set for this dungeon")
        return self.map
    
    def get_theme(self, theme_id: str) -> Theme:
        """Get a theme by ID.
        
        Args:
            theme_id: The ID of the theme to get
            
        Returns:
            The theme with the given ID
            
        Raises:
            KeyError: If no theme with the given ID exists
        """
        if theme_id not in self.themes:
            raise KeyError(f"No theme with ID {theme_id} exists")
        return self.themes[theme_id]
    
    def get_item(self, item_id: str) -> Item:
        """Get an item by ID.
        
        Args:
            item_id: The ID of the item to get
            
        Returns:
            The item with the given ID
            
        Raises:
            KeyError: If no item with the given ID exists
        """
        if item_id not in self.items:
            raise KeyError(f"No item with ID {item_id} exists")
        return self.items[item_id]
    
    def set_current_room(self, room_id: str) -> None:
        """Set the current room.
        
        Args:
            room_id: The ID of the room to set as current
            
        Raises:
            ValueError: If no map has been set or if the room does not exist
        """
        if self.map is None:
            raise ValueError("No map has been set for this dungeon")
        
        try:
            print(f"DEBUG: Attempting to get room with ID: {room_id}")
            # Check if the room exists in the map
            room_exists = False
            for room in self.map.get_all_rooms():
                if str(room.id) == room_id:
                    room_exists = True
                    break
            
            if not room_exists:
                print(f"DEBUG: Room with ID {room_id} not found in map")
                raise ValueError(f"Room with ID {room_id} does not exist in the map")
            
            current_room = self.map.get_room_by_id(room_id)
            self.current_room_id = room_id
            self.current_room = current_room
            
            # Set the room image from the current room
            if current_room.room_img:
                room_img = current_room.room_img
            else:
                # Initialize with default image
                current_room.room_img = "/static/img/interface/default_room.webp"
                
        except (ValueError, KeyError) as e:
            print(f"DEBUG: Error getting room by ID: {e}")
            self.current_room_id = None
            self.current_room = None
            raise ValueError(f"Room with ID {room_id} does not exist in the map")
    
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the dungeon to a dictionary.
        
        Returns:
            A dictionary representation of the dungeon
        """
        dungeon_dict = {
            "id": self.id,
            "dungeon_file": self.dungeon_file,
            "session_id": self.session_id,
            "npcs": {id: npc.to_dict() for id, npc in self.npcs.items()},
            "enemies": {id: enemy.to_dict() for id, enemy in self.enemies.items()},
            "map": self.map.to_dict() if self.map else None,
            "themes": {id: theme.to_dict() for id, theme in self.themes.items()},
            "items": {id: item.to_dict() for id, item in self.items.items()},
            "current_room_id": self.current_room_id,
            "active_character_id": self.active_character_id,
            "ai_enabled": self.ai_enabled,
            "score": self.score
        }
        
        # Add scenario information if available
        if self.scenario:
            dungeon_dict["scenario"] = self.scenario.to_dict()
            # Add name and description from scenario
            dungeon_dict["name"] = self.scenario.name
            dungeon_dict["description"] = self.scenario.description
        else:
            # Add default name and description if no scenario
            dungeon_dict["name"] = "New Dungeon"
            dungeon_dict["description"] = "A mysterious dungeon"
        
        return dungeon_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dungeon':
        """Create a dungeon from a dictionary.
        
        Args:
            data: The dictionary to create the dungeon from
            
        Returns:
            A new dungeon instance
        """
        dungeon = cls(
            name=data.get("name", "New Dungeon"),
            description=data.get("description", "A mysterious dungeon"),
            load_sample=False,
            session_id=data.get("session_id")
        )
        
        # Set the ID and file
        dungeon.id = data.get("id", str(uuid.uuid4()))
        dungeon.dungeon_file = data.get("dungeon_file", "sample_dungeon.json")
        
        # Load default player items
        # todo
        
        # Load NPCs
        for npc_id, npc_data in data.get("npcs", {}).items():
            npc = NPC.from_dict(npc_data)
            dungeon.npcs[npc_id] = npc
        
        # Load enemies
        for enemy_id, enemy_data in data.get("enemies", {}).items():
            enemy = NPC.from_dict(enemy_data)
            dungeon.enemies[enemy_id] = enemy
        
        # Load map
        if data.get("map"):
            dungeon.map = Map.from_dict(data["map"])
        
        # Load themes
        for theme_id, theme_data in data.get("themes", {}).items():
            theme = Theme.from_dict(theme_data)
            dungeon.themes[theme_id] = theme
        
        # Load items
        for item_id, item_data in data.get("items", {}).items():
            item = Item.from_dict(item_data)
            dungeon.items[item_id] = item
        
        # Set current room and active character
        dungeon.current_room_id = data.get("current_room_id")
        dungeon.active_character_id = data.get("active_character_id")
        
        # Set ai_enabled
        dungeon.ai_enabled = data.get("ai_enabled", True)
        
        # Set score
        dungeon.score = data.get("score", 0)
        
        # Load scenario if available
        if "scenario" in data:
            dungeon.scenario = Scenario.from_dict(data["scenario"])
        
        return dungeon


    def list_npcs(self) -> List[NPC]:
        """List all NPCs in the dungeon.
        
        Returns:
            A list of all NPCs
        """
        return list(self.npcs.values())
    
    def list_enemies(self) -> List[NPC]:
        """List all enemies in the dungeon.
        
        Returns:
            A list of all enemies
        """
        return list(self.enemies.values())
    
    def get_help(self) -> str:
        """Get help for the dungeon.
        
        Returns:
            A string containing the help text
        """
        help_text = "<hr><p class='output-area_bold'>~ Available Commands ~</p><ul>"
        
        # Loop through all action types where show_help is True
        for action_type in ActionType:
            if action_type.value["show_help"]:
                # Add the action type help text as a header
                help_text += f"<p class='output-area_bold'>{action_type.value['name']}</p>{action_type.value['help_text']}"
                
                # Find all actions of this type
                actions_of_type = [action for action in Action if action.value["action_type"] == action_type]
                
                # Loop through all actions of this type
                for action in actions_of_type:
                    if action == Action.NONE:
                        continue
                    
                    # Get the primary command (first alias)
                    primary_command = action.value["alias"][0]
                    
                    # Get all aliases
                    aliases = ", ".join(action.value["alias"][1:]) if len(action.value["alias"]) > 1 else ""
                    
                    # Format the command line with help text
                    command_line = f"- {primary_command}"
                    
                    
                    # Add the help text for this action
                    if action.value["help_text"]:
                        command_line += f" - {action.value['help_text']}"
                    
                    if aliases:
                        command_line += f" (aliases: {aliases})"

                    help_text += command_line + "\n"
                
                help_text += "\n"
        
        help_text += "<p class='output-area_bold'>Examples:</p>"
        help_text += "- move north\n"
        help_text += "- look around\n"
        help_text += "- examine chest\n"
        help_text += "- talk to merchant\n"
        help_text += "- take sword\n"
        help_text += "- attack goblin\n"

        help_text += "</ul>"
        return help_text
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse a command string into a dictionary.
        
        Args:
            command: The command string to parse
            
        Returns:
            A dictionary containing the parsed command
        """
        #-------------------------------
        '''The parser has an order to how it interprets commands. 
        1 - Actions based on action ENUMs
        2 - NPCs
        3 - Enemies
        4 - Items based on items in the room, or player inventory
        5 - Any specific amount of an item, a numeric value
        '''

        # Get NPCs in the current room
        npc_list = []
        room_item_list = []
        player_item_list = []

        # TODO: This is a hack we need to refactor this
        if self.current_room:
            # Get NPCs in the current room
            npc_list = [npc.name.lower() for npc in self.current_room.npcs]
            # Also add aliases if they exist
            for npc in self.current_room.npcs:
                if hasattr(npc, 'alias') and npc.alias:
                    npc_list.append(npc.alias.lower())
            
            # Get items in the current room
            room_item_list = [item["item"].name.lower() for item in self.current_room.room_items]


        


        
        # --- Default Output ---
        default_response = ["I'm not sure what you are trying to do here...",
                            "Nope.",
                            "Ain't gonna happen.",
                            "No can do."
                            ]
        output_message = "" #empty string


         # Naughty word list; an imcomplete list to be sure, mainly added for humour
        naughty_word_list = ["fuck", "shit", "asshole", "bitch"]
        naughty_response = ["Does your mother know you talk like that?",
                                       "Rude!",
                                       "Seriously? No."
                                        ]

        # Remove non-alphabetic characters and tokenize the command
        command_alpha = re.sub(r'[^a-zA-Z0-9\s]', '', command)
        command_alpha_words = word_tokenize(command_alpha)

        amount = 1  # used for numbers, default is 1 
        primary_action = Action.NONE

        # list of action words and alias
        available_action_words = [{action: action.value["alias"]} for action in Action]
        
        # list of directions
        available_direction_words = [{direction: direction.value} for direction in Direction]
        print(f"DEBUG: Available direction words: {available_direction_words}")
        # -----------------------
        
        # Remove non-alphabetic characters and tokenize the command
        command_words = word_tokenize(command_alpha.lower())
        print(f"DEBUG: Command words: {command_words}")
        
     
        
        # Command Actions
        '''
        Gets a list of alias for each command word, and compares the words in the command to see if they map to an action word alias
        If they do, then return the list of action ENUMS
        '''
        command_actions = [action_word.keys() for action_word in available_action_words 
            if len([word for word in command_words 
                 if word in list(action_word.values())[0]]) > 0]  # only one list
        
       
        

        # find primary action, if not primary action, return NONE
        if len(command_actions) == 0:
            # return Action.NONE
            output_message = random.choice(default_response)
        
        elif len(set(naughty_word_list) & set(command_words)) > 0:
            output_message = random.choice(naughty_response)

        else:
            primary_action = list(command_actions[0])[0]
            
            # alias of action
            available_action_words_alias = list(itertools.chain.from_iterable([action.value["alias"] for action in Action]))
            available_directions_alias = list(itertools.chain.from_iterable([direction.value for direction in Direction]))
            remaining_command_words = [word for word in command_words if word not in available_action_words_alias]

        
            # Get room_direction_info from the current room
            # Used for MOVE and LOOK commands
            room_direction_info = ""
            if self.current_room:
                room_direction_info = self.current_room.get_room_direction_info()
            else:
                room_direction_info = "There are no exits from this room."



            #TODO: Refactor
            '''
            # NPC
            npc_target = None
            if remaining_command_words:
                for word in remaining_command_words:
                    if word.lower() in npc_list:
                        npc_target = word
                        remaining_command_words.remove(word)
                        break
               
            # Get items in player inventory
            if self.active_character_id and self.active_character_id in self.characters:
                active_character = self.characters[self.active_character_id]
                player_item_list = [item.name.lower() for item in active_character.items]

            # Enemy
            enemy_target = None
            if remaining_command_words:
                for word in remaining_command_words:
                    if word.lower() in npc_list:  # Enemies are also in the NPC list
                        enemy_target = word
                        remaining_command_words.remove(word)
                        break
            
            # Items
            item_target = None
            if remaining_command_words:
                for word in remaining_command_words:
                    if word.lower() in room_item_list or word.lower() in player_item_list:
                        item_target = word
                        remaining_command_words.remove(word)
                        break
            
            # Item amount 
            if remaining_command_words:
                try:
                    amount = int(remaining_command_words[0])
                    remaining_command_words.pop(0)
                except (ValueError, IndexError):
                    pass
            '''

            # output
     
            # Special Actions
            # --------------------------------
            if primary_action is Action.INIT:
                scenario_welcome_message = self.scenario.get_welcome_message()
                output_message = f"{scenario_welcome_message}\n\n {room_description}\n{room_direction_info}."
                
            # HELP
            # --------------------------------
            elif primary_action is Action.HELP:
                help_text = self.get_help()
                output_message = help_text

            # CLEAR
            # --------------------------------
            elif primary_action is Action.CLEAR:
                output_message = "CLEAR_OUTPUT"
        
            # INVENTORY
            # --------------------------------
            elif primary_action is Action.INVENTORY:
                # Check if player character exists
                if not self.player_character:
                    output_message = "You need to set a player character first."
                else:
                    # Get the player's inventory
                    inventory = self.player_character.inventory
                    
                    if not inventory:
                        output_message = "Your inventory is empty."
                    else:
                        # Create a list of item names and types
                        item_details = [f"<span class='console-highlight'>{item.name}</span> (a {item.item_type})" for item in inventory]
                        
                        # Format the output message
                        if len(item_details) == 1:
                            output_message = f"Your inventory contains: {item_details[0]}."
                        else:
                            # Join all item details with commas and 'and' for the last item
                            formatted_items = ", ".join(item_details[:-1])
                            formatted_items += f" and {item_details[-1]}"
                            
                            output_message = f"Your inventory contains: {formatted_items}."

                

            # LOOK
            # --------------------------------
            elif primary_action is Action.LOOK:
                if self.current_room:
                    # Check if the AI has updated the description  
                    output_message = self.current_room.get_room_details()
                    output_message += f"\n{room_direction_info}"
                else:
                    output_message = "You can't see anything in the darkness."
                
            # MOVE DIRECTION
            # --------------------------------
            elif primary_action is Action.MOVE:

                # get room direction information
                available_directions = []
                if self.current_room_id and self.map:
                    try:
                        connected_rooms = self.map.get_connected_rooms(self.current_room_id)
                        available_directions = [direction.value[0] for direction in connected_rooms.keys()]
                        print(f"DEBUG: Available directions: {available_directions}")
                    except (ValueError, KeyError) as e:
                        print(f"DEBUG: Error getting connected rooms: {e}")
                        available_directions = []

                room_description = self.current_room.description
                room_name = self.current_room.name
                
                print(f"DEBUG: Processing MOVE command with words: {command_words}")
                command_directions = [direction_word.keys() for direction_word in available_direction_words 
                    if len([word for word in command_words 
                         if word in list(direction_word.values())[0]]) > 0]  # only one list
                
                print(f"DEBUG: Detected directions: {command_directions}")
                
                # No direction specified
                if len(command_directions) == 0:
                    if self.current_room and self.map:
                        try:
                            print(f"DEBUG: Current room ID: {self.current_room_id}")
                            print(f"DEBUG: Available directions: {available_directions}")
                        except (ValueError, KeyError) as e:
                            print(f"DEBUG: Error getting connected rooms: {e}")
                          
                    
                    if available_directions:
                        if remaining_command_words:
                            invalid_direction = " ".join(remaining_command_words)
                            output_message = f"You can't move <span class='console-highlight'>{invalid_direction}</span>. What direction do you want to move in? {room_direction_info}."
                        else:
                            output_message = f"What direction do you want to move in? {room_direction_info}."
                    else:
                        output_message = "You are stuck! There are no exits from this room."
                else:
                    primary_direction = list(command_directions[0])[0]
                    print(f"DEBUG: Primary direction: {primary_direction}")
                    
                    # Check if there's a connection in that direction
                    if self.current_room and self.map:
                        try:
                            # Get the connected room in the specified direction
                            connected_room = self.map.get_connected_room(self.current_room_id, primary_direction)
                            if connected_room:
                                # Update the current room
                                self.current_room_id = str(connected_room.id)
                                self.set_current_room(self.current_room_id)
                                # Mark the new room as visited
                                self.map.mark_room_visited(connected_room.id)
                                output_message = f"You move <span class='console-highlight'>{primary_direction}</span>.\n\n{connected_room.description}\n{connected_room.get_room_direction_info()}"
                                
                                # Get the room image for the new room
                                room_img = connected_room.room_img if connected_room.room_img else "/static/img/interface/default_room.webp"
                            else:
                                output_message = "You can't go that direction."
                        except (ValueError, KeyError):
                            output_message = "You can't go that direction."           
                    else:
                        output_message = "You can't move right now."
            
            # VERB SPECIFIC ACTIONS
            else:
                if not remaining_command_words:
                    output_message = f'What do you want to <span class="console-highlight">{primary_action.name.lower()}</span>?'
                else:
                    room_target_item = None
                    player_target_item = None
                    target_item = None
                    target_subject = None

                    # Get target and subject
                    # Check room items first, then player inventory
                     # Get all items in the current room
                    room_items = self.current_room.room_items
                    player_items = self.player_character.inventory
                    
                    # Check each word against each item's name, alias, and item_type
                    for word in remaining_command_words:
                        for item_dict in room_items:
                            # Get the actual Item object from the dictionary
                            item = item_dict["item"]
                            
                            # Check if the word matches the item's name
                            if word.lower() == item.name.lower():
                                room_target_item = item
                                break
                            
                            # Check if the word matches any of the item's aliases
                            if hasattr(item, 'alias') and any(word.lower() == alias.lower() for alias in item.alias):
                                room_target_item = item                    
                                break
                            
                            # Check if the word matches the item's type (if it has one)
                            if hasattr(item, 'item_type') and item.item_type and word.lower() == item.item_type.lower():
                                room_target_item = item
                                break

                    # Check each word against each item's name, alias, and item_type
                    for word in remaining_command_words:
                        for item in player_items:
                            # Check if the word matches the item's name
                            if word.lower() == item.name.lower():
                                player_target_item = item
                                break
                            
                            # Check if the word matches any of the item's aliases
                            if hasattr(item, 'alias') and any(word.lower() == alias.lower() for alias in item.alias):
                                player_target_item = item                    
                                break
                            
                            # Check if the word matches the item's type (if it has one)
                            if hasattr(item, 'item_type') and item.item_type and word.lower() == item.item_type.lower():
                                player_target_item = item
                                break
                        
                    if not room_target_item and not player_target_item:
                        output_message = f"I don't see anything called '{' '.join(remaining_command_words)}' to {primary_action.name.lower()}."
                 
            
                    else:

                        # Prioritise room target item
                        if room_target_item:
                            target_item = room_target_item
                        elif player_target_item:
                            target_item = player_target_item

                        # --------------------------------
                        # EXAMINE
                        # --------------------------------
                        if primary_action is Action.EXAMINE:
                        
                                # Check if any of the remaining command words match an item in the room
                                if target_item:
                                    # We found a matching item, examine it
                                    # use a, an, or the depending on the item
                                    a_or_an = "a"
                                    if target_item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                                        a_or_an = "an"
                            
                                    output_message = f"You examine the <span class='console-highlight'>{target_item.item_type.lower()}</span>. You see {a_or_an} <span class='console-highlight'>{target_item.name}</span>. {target_item.detailed_description}"
                                else:
                                    # No matching item found
                                    output_message = f"I don't see anything called '{' '.join(remaining_command_words)}' to examine."

                        # TAKE
                        # --------------------------------
                        # Only room target item
                        elif primary_action is Action.TAKE:
                            # Check if player character exists
                            if not self.player_character:
                                output_message = "You need to set a player character first."
                            else:
                                # Remove the item from the room
                                self.current_room.remove_item(room_target_item)
                                
                                # Add the item to the player's inventory
                                self.player_character.add_to_inventory(room_target_item)
                                
                                # Use a or an depending on the item name
                                a_or_an = "a"
                                if room_target_item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                                    a_or_an = "an"
                                
                                output_message = f"You take {a_or_an} <span class='console-highlight'>{room_target_item.name}</span> and add it to your inventory."

                        # DROP
                        # --------------------------------
                        # Only player target item
                        elif primary_action is Action.DROP:
                            # Check if player character exists
                            if not self.player_character:
                                output_message = "You need to set a player character first."
                            else:
                                # Check if the item is in the player's inventory
                                if player_target_item:
                                    # Remove the item from the player's inventory
                                    self.player_character.remove_from_inventory(player_target_item)
                                    
                                    # Add the item to the current room
                                    self.current_room.add_item(player_target_item)
                                    
                                    # Use a or an depending on the item name
                                    a_or_an = "a"
                                    if player_target_item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                                        a_or_an = "an"
                                    
                                    output_message = f"You drop {a_or_an} <span class='console-highlight'>{player_target_item.name}</span> in the room."
                                else:
                                    # Item not found in inventory
                                    output_message = f"You don't have anything called '{' '.join(remaining_command_words)}' to drop."

                        # INVENTORY actions
                        # --------------------------------
                        #EAT  DRINK SMELL  BREAK  THROW READ
                    

                        # GIVE
                        # --------------------------------
                        elif primary_action is Action.GIVE:
                            output_message = f"<Not implemented> Give item."

                        

                        # ATTACK [NPC/ENEMY]
                        # --------------------------------
                        elif primary_action is Action.ATTACK:
                            output_message = f"<Not implemented> What do you want to attack?"
                    
                        # TALK
                        # --------------------------------
                        elif primary_action is Action.TALK:
                            output_message = f"<Not implemented> Who do you want to talk to?"

                        # Inventory interaction
                        # --------------------------------
                        else:
                            pass
                            # [ITEM ACTION] [ITEM] [AMOUNT] - Assumes player since no enemy/NPC
                            # [ITEM ACTION] [ITEM] [NPC] [AMOUNT] - Interact with NPC

            # Get the current room image if not already set
            # TODO: This is a hack to get the room image, we need to refactor this

        
     

        return {"action": primary_action, "message": output_message, "room_img": self.current_room.room_img}

    def get_use_ai(self) -> bool:
        """Get the current value of use_ai."""
        return self.use_ai
    
    def set_use_ai(self, value: bool) -> None:
        """Set the value of use_ai."""
        self.use_ai = value
        print(f"DEBUG: use_ai set to {value}") 

    def get_ai_enabled(self) -> bool:
        """Get whether AI is enabled for the dungeon.
        
        Returns:
            True if AI is enabled, False otherwise
        """
        return self.ai_enabled
    
    def set_ai_enabled(self, value: bool) -> None:
        """Set whether AI is enabled for the dungeon.
        
        Args:
            value: True to enable AI, False to disable
        """
        self.ai_enabled = value
        print(f"DEBUG: AI enabled set to {value} for dungeon {self.scenario.name}") 

    def get_score(self) -> int:
        """Get the current player score.
        
        Returns:
            The current player score
        """
        return self.score
    
    def set_score(self, value: int) -> None:
        """Set the player score.
        
        Args:
            value: The new score value
        """
        self.score = value
        print(f"DEBUG: Player score set to {value}")
    
    def add_to_score(self, value: int) -> None:
        """Add a value to the player score.
        
        Args:
            value: The value to add to the score (can be positive or negative)
        """
        self.score += value
        print(f"DEBUG: Added {value} to player score. New score: {self.score}") 

    def set_player_character(self, username: str) -> None:
        """Set the player character with the given username.
        
        Args:
            username: The username to use for the player character
        """
        # Create a new character for the player
        self.player_character = Character(
            name=username,
            description=f"A brave adventurer named {username}",
            hit_points=100,
            dexterity=10,
            intelligence=10,
            perception=10,
            strength=10,
            wisdom=10
        )
        