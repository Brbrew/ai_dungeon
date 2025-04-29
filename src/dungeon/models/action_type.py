"""ActionType enum for the dungeon project."""
from enum import Enum

class ActionType(Enum):
    """Enum representing the types of actions in the dungeon game."""
    
    # No action type
    NONE = {"action_type":"NONE","name":"NONE","show_help":False, "help_text":""}
    
    # Initialization actions
    INIT = {"action_type":"INIT","name":"INIT","show_help":False, "help_text":""}
    RESTART = {"action_type":"RESTART","name":"RESTART","show_help":False, "help_text":""}
    
    # General actions
    GENERAL = {"action_type":"GENERAL","name":"GENERAL","show_help":True, "help_text":"General Commands\n\n"}

    # Movement actions
    MOVE = {"action_type":"MOVE","name":"MOVE","show_help":True, "help_text":"Move Commands\n\n"}
    
    # Inventory actions
    INVENTORY = {"action_type":"INVENTORY","name":"INVENTORY","show_help":True, "help_text":"Inventory Commands.\nInventory commands are typically in the form of 'take [item]' or 'drink [item]'.\n\n"}
    
    # Room actions
    ROOM = {"action_type":"ROOM","name":"ROOM","show_help":False, "help_text":"Room Commands\n\n"}
    
    # Interaction actions
    INTERACTION = {"action_type":"INTERACTION","name":"INTERACTION","show_help":True, "help_text":"Interaction Commands.\nInteraction commands are typically in the form of 'give [item] to [npc]' or 'take [item] from [npc]'.\nThey can also be singular, like 'use [item]'.\n\n"}
    
    # Combat actions
    COMBAT = {"action_type":"COMBAT","name":"COMBAT","show_help":True, "help_text":"Combat Commands. Combat commands are typically in the form of 'attack [enemy]'.\n\n"}
    
    def __str__(self):
        return self.value 