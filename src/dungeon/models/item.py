"""Item model for the dungeon project."""
from typing import Any, Dict, Optional, List
from uuid import UUID, uuid4

from .base import BaseModel
from .action import Action, ActionType

class Item(BaseModel):
    """An item that can be found in a room."""
    
    def __init__(
        self,
        name: str,
        description: str,
        detailed_description: str,
        value: float = 0.0,
        weight: float = 0.0,
        alias: Optional[List[str]] = None,
        item_type: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Initialize an item.
        
        Args:
            name: The item's name
            description: The item's description
            detailed_description: A more detailed description of the item
            value: The item's monetary value
            weight: The item's weight (must be non-negative)
            alias: Optional list of alternative names for the item
            item_type: Optional type of the item (e.g., "weapon", "armor", "consumable")
            **kwargs: Additional arguments passed to BaseModel
            
        Raises:
            ValueError: If weight is negative
        """
        if weight < 0:
            raise ValueError("Weight must be non-negative")
            
        super().__init__(**kwargs)
        self._name = name
        self._description = description
        self._detailed_description = detailed_description
        self._value = float(value)
        self._weight = float(weight)
        self._alias = [name] + (alias if alias is not None else [])
        self._item_type = item_type
    
    @property
    def name(self) -> str:
        """Get the item's name.
        
        Returns:
            The item's name
        """
        return self._name
    
    @property
    def alias(self) -> List[str]:
        """Get the item's aliases.
        
        Returns:
            List of alternative names for the item
        """
        return self._alias.copy()
    
    @property
    def description(self) -> str:
        """Get the item's description.
        
        Returns:
            The item's description
        """
        return self._description
    
    @property
    def detailed_description(self) -> str:
        """Get the item's detailed description.
        
        Returns:
            The item's detailed description
        """
        return self._detailed_description
    
    @property
    def value(self) -> float:
        """Get the item's value.
        
        Returns:
            The item's value
        """
        return self._value
    
    @property
    def weight(self) -> float:
        """Get the item's weight.
        
        Returns:
            The item's weight
        """
        return self._weight
    
    @weight.setter
    def weight(self, value: float) -> None:
        """Set the item's weight.
        
        Args:
            value: The new weight value (must be non-negative)
            
        Raises:
            ValueError: If weight is negative
        """
        if value < 0:
            raise ValueError("Weight must be non-negative")
        self._weight = float(value)
    
    @property
    def item_type(self) -> Optional[str]:
        """Get the item's type.
        
        Returns:
            The item's type or None if not set
        """
        return self._item_type
    
    @item_type.setter
    def item_type(self, value: Optional[str]) -> None:
        """Set the item's type.
        
        Args:
            value: The new item type or None to clear it
        """
        self._item_type = value
    
    def _handle_use(self) -> str:
        """Handle the USE action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You try to use the {self.name}, but you need to specify what to use it on."
    
    def _handle_examine(self) -> str:
        """Handle the EXAMINE action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You examine the {self.name}. {self.detailed_description}"
    
    def _handle_read(self) -> str:
        """Handle the READ action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You try to read the {self.name}, but there's nothing to read."
    
    def _handle_eat(self) -> str:
        """Handle the EAT action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You try to eat the {self.name}, but it's not edible."
    
    def _handle_drink(self) -> str:
        """Handle the DRINK action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You try to drink the {self.name}, but it's not a liquid."
    
    def _handle_smell(self) -> str:
        """Handle the SMELL action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You smell the {self.name}. It has a metallic scent."
    
    def _handle_break(self) -> str:
        """Handle the BREAK action on this item.
        
        Returns:
            A message describing what happened
        """
        return f"You try to break the {self.name}, but it's too sturdy."
    
    def _handle_non_inventory(self, action: Action) -> str:
        """Handle a non-inventory action on this item.
        
        Args:
            action: The action to perform
            
        Returns:
            A message describing what happened
        """
        return f"You can't {action.name.lower()} the {self.name}."
    
    def handle_inventory_action(self, action: Action) -> str:
        """Handle an inventory action on this item.
        
        Args:
            action: The action to perform
            
        Returns:
            A message describing what happened
        """
        # Check if the action is an inventory action
        if Action.get_action_type(action) == ActionType.INVENTORY:
            # Handle specific inventory actions
            if action == Action.USE:
                return self._handle_use()
            elif action == Action.EXAMINE:
                return self._handle_examine()
            elif action == Action.READ:
                return self._handle_read()
            elif action == Action.EAT:
                return self._handle_eat()
            elif action == Action.DRINK:
                return self._handle_drink()
            elif action == Action.SMELL:
                return self._handle_smell()
            elif action == Action.BREAK:
                return self._handle_break()
        
        # For non-inventory actions, return a generic message
        return self._handle_non_inventory(action)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the item to a dictionary.
        
        Returns:
            Dict containing the item's attributes
        """
        return {
            **super().to_dict(),
            "name": self.name,
            "alias": self.alias,
            "description": self.description,
            "detailed_description": self.detailed_description,
            "value": self.value,
            "weight": self.weight,
            "item_type": self._item_type,
        } 