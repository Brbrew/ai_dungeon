"""Base model for the dungeon project."""
from typing import Any, Dict, Optional
import uuid

class BaseModel:
    """Base model class for all dungeon entities."""
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize a base model.
        
        Args:
            **kwargs: Additional arguments
        """
        self._id = uuid.uuid4()
        self._created_at = None  # Would be set to datetime.now() in a real implementation
        
    @property
    def id(self) -> uuid.UUID:
        """Get the model's ID.
        
        Returns:
            The model's UUID
        """
        return self._id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary.
        
        Returns:
            Dict containing the model's attributes
        """
        return {
            "id": str(self._id),
            "created_at": self._created_at
        } 