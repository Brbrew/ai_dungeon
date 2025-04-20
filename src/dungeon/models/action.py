"""Action enum for the dungeon project."""
from enum import Enum

class Action(Enum):
    """Enum representing possible actions in the dungeon game."""
    
    # No action recognized
    NONE = ["none", "unknown"]
    
    # Initialization actions
    INIT = ["init", "initialize", "start"]
    RESTART = ["restart", "reset", "begin again"]
    
    # Generic actions
    MOVE = ["move", "go", "travel"]
    LOOK = ["look"]
    EXAMINE = ["examine"]
    TALK = ["talk", "ask", "tell"]
    HELP = ["help"]
    
    # Room actions
    # Unlock door with key
    
    # Inventory actions
    INVENTORY = ["inventory", "inv"]
    USE = ["use"]
    EAT = ["eat"]
    DRINK = ["drink"]
    SMELL = ["smell"]
    BREAK = ["break"]
    TAKE = ["take"]
    GIVE = ["give"]
    OPEN = ["open"]
    CLOSE = ["close"]
    READ = ["read"]
    
    # Combat actions
    ATTACK = ["attack", "kick", "punch", "kill", "fight"]

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
            for alias in action.value:
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
        return action.value 