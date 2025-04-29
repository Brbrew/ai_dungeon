"""Action enum for the dungeon project."""
from enum import Enum

from .action_type import ActionType

class Action(Enum):
    """Enum representing possible actions in the dungeon game."""
    
    # No action recognized
    NONE = {"alias": ["none", "unknown"], "action_type": ActionType.NONE, "help_text":""}
    
    # Initialization actions
    INIT = {"alias": ["init", "initialize", "start"], "action_type": ActionType.INIT, "help_text":""}
    RESTART = {"alias": ["restart", "reset", "begin again"], "action_type": ActionType.RESTART, "help_text":""}
    
    # Generic actions
    MOVE = {"alias": ["move", "go", "travel"], "action_type": ActionType.MOVE, "help_text":"Move in a direction."}
    #JUMP = {"alias": ["jump"], "action_type": ActionType.MOVE, "help_text":""}

    # Generic actions
    LOOK = {"alias": ["look"], "action_type": ActionType.GENERAL, "help_text":"Look around you, in a general way."}
    INVENTORY = {"alias": ["inventory", "inv"], "action_type": ActionType.GENERAL, "help_text":"Check your inventory."}
    HELP = {"alias": ["help"], "action_type": ActionType.GENERAL, "help_text":"Get help with the game."}
    CLEAR = {"alias": ["clear"], "action_type": ActionType.GENERAL, "help_text":"Clear the screen."}
    EXAMINE = {"alias": ["examine"], "action_type": ActionType.GENERAL, "help_text":"Examine an object in detail."}
    # Room actions
    # Unlock door with key
   
    # Inventory actions    
    EAT = {"alias": ["eat"], "action_type": ActionType.INVENTORY, "help_text":"Eat an [item]."}
    DRINK = {"alias": ["drink"], "action_type": ActionType.INVENTORY, "help_text": "Drink an [item]."}
    SMELL = {"alias": ["smell"], "action_type": ActionType.INVENTORY, "help_text": "Smell an [item]."}
    BREAK = {"alias": ["break"], "action_type": ActionType.INVENTORY, "help_text": "Break an [item]."}
    THROW = {"alias": ["throw"], "action_type": ActionType.INVENTORY, "help_text": "Throw an [item]."}
    READ = {"alias": ["read"], "action_type": ActionType.INVENTORY, "help_text": "Read an [item]."}
    DROP = {"alias": ["drop"], "action_type": ActionType.INVENTORY, "help_text":"Drop an [item]."}

    # interaction actions, requires target and object
    USE = {"alias": ["use"], "action_type": ActionType.INVENTORY, "help_text":"Use an [item] on an [object]."}
    TALK = {"alias": ["talk", "ask", "tell"], "action_type": ActionType.INTERACTION, "help_text":"Talk to an [npc]."}
    TAKE = {"alias": ["take"], "action_type": ActionType.INTERACTION, "help_text":"Take an [item]."}
    GIVE = {"alias": ["give"], "action_type": ActionType.INTERACTION, "help_text":"Give an [item] to an [npc]."}
    OPEN = {"alias": ["open"], "action_type": ActionType.INTERACTION, "help_text":"Open an [object], like a door or a chest."}
    CLOSE = {"alias": ["close"], "action_type": ActionType.INTERACTION, "help_text":"Close an [object], like a door or a chest."}
    #UNLOCK = {"alias": ["unlock"], "action_type": ActionType.ROOM, "help_text": "Unlock a door with a key."}
    
    
    # Combat actions
    ATTACK = {"alias": ["attack", "kick", "punch", "kill", "fight"], "action_type": ActionType.COMBAT, "help_text":""}

    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def from_command(cls, command: str) -> 'Action':
        """Get the action from a command string.
        
        Args:
            command: The command string to parse
            
        Returns:
            The matching Action enum value or NONE if no match
        """
        command = command.lower().strip()
        
        # Check if the command starts with any of the action aliases
        for action in cls:
            for alias in action.value["alias"]:
                if command.startswith(alias):
                    return action
        
        return Action.NONE
    
    @classmethod
    def get_aliases(cls, action: 'Action') -> list:
        """Get all aliases for a given action.
        
        Args:
            action: The action to get aliases for
            
        Returns:
            A list of aliases for the action
        """
        return action.value["alias"]
    
    @classmethod
    def get_action_type(cls, action: 'Action') -> ActionType:
        """Get the action type for a given action.
        
        Args:
            action: The action to get the type for
            
        Returns:
            The ActionType enum value for the action
        """
        return action.value["action_type"] 