"""Weapon model for the dungeon project."""
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple

from .item import Item
from .dice import Dice, DiceError

class WeaponType(Enum):
    """Types of weapons."""
    MELEE = "melee"
    RANGED = "ranged"

class WeaponError(Exception):
    """Exception raised for errors in the Weapon class."""
    pass

class Weapon(Item):
    """A weapon that can be used in combat."""
    
    def __init__(
        self,
        name: str,
        description: str,
        weapon_type: WeaponType,
        damage_dice: Dice,
        num_damage_dice: int = 1,
        damage_modifier: int = 0,
        strength_requirement: int = 0,
        dexterity_requirement: int = 0,
        range_distance: Optional[int] = None,
        value: float = 0.0,
        weight: float = 0.0
    ) -> None:
        """Initialize a weapon.
        
        Args:
            name: The name of the weapon
            description: A description of the weapon
            weapon_type: The type of weapon (melee or ranged)
            damage_dice: The dice used to determine damage
            num_damage_dice: The number of dice to roll for damage
            damage_modifier: A modifier to add to the damage roll
            strength_requirement: The minimum strength required to use the weapon
            dexterity_requirement: The minimum dexterity required to use the weapon
            range_distance: The range of the weapon (required for ranged weapons)
            value: The monetary value of the weapon
            weight: The weight of the weapon
            
        Raises:
            WeaponError: If range_distance is not provided for ranged weapons
        """
        super().__init__(
            name=name,
            description=description,
            value=value,
            weight=weight
        )
        
        self._weapon_type = weapon_type
        self._damage_dice = damage_dice
        self._num_damage_dice = max(1, num_damage_dice)  # Ensure at least 1 die
        self._damage_modifier = damage_modifier
        self._strength_requirement = strength_requirement
        self._dexterity_requirement = dexterity_requirement
        
        if weapon_type == WeaponType.RANGED and range_distance is None:
            raise WeaponError("Range distance must be provided for ranged weapons")
        self._range_distance = range_distance
    
    @property
    def weapon_type(self) -> WeaponType:
        """Get the type of weapon.
        
        Returns:
            The weapon type
        """
        return self._weapon_type
    
    @property
    def damage_dice(self) -> Dice:
        """Get the damage dice.
        
        Returns:
            The dice used for damage
        """
        return self._damage_dice
    
    @property
    def num_damage_dice(self) -> int:
        """Get the number of damage dice.
        
        Returns:
            The number of dice rolled for damage
        """
        return self._num_damage_dice
    
    @property
    def damage_modifier(self) -> int:
        """Get the damage modifier.
        
        Returns:
            The modifier added to damage rolls
        """
        return self._damage_modifier
    
    @property
    def strength_requirement(self) -> int:
        """Get the strength requirement.
        
        Returns:
            The minimum strength required
        """
        return self._strength_requirement
    
    @property
    def dexterity_requirement(self) -> int:
        """Get the dexterity requirement.
        
        Returns:
            The minimum dexterity required
        """
        return self._dexterity_requirement
    
    @property
    def range_distance(self) -> Optional[int]:
        """Get the range distance.
        
        Returns:
            The range of the weapon, or None for melee weapons
        """
        return self._range_distance
    
    def roll_damage(self) -> int:
        """Roll for damage using a single die.
        
        Returns:
            The damage dealt
        """
        return self._damage_dice.roll()
    
    def roll_damage_with_modifier(self, modifier: int = 0) -> int:
        """Roll for damage and add a modifier.
        
        Args:
            modifier: An additional modifier to add to the damage
            
        Returns:
            The damage dealt plus modifiers
        """
        return self.roll_damage() + self._damage_modifier + modifier
    
    def roll_multiple_damage(self) -> List[int]:
        """Roll multiple dice for damage.
        
        Returns:
            A list of damage values, one for each die
        """
        return [self._damage_dice.roll() for _ in range(self._num_damage_dice)]
    
    def roll_total_damage(self, additional_modifier: int = 0) -> Tuple[int, List[int]]:
        """Roll all damage dice and calculate total damage.
        
        Args:
            additional_modifier: An additional modifier to add to the total
            
        Returns:
            A tuple containing (total damage, individual roll results)
        """
        rolls = self.roll_multiple_damage()
        total = sum(rolls) + self._damage_modifier + additional_modifier
        return total, rolls
    
    def can_use(self, strength: int, dexterity: int) -> bool:
        """Check if a character can use this weapon.
        
        Args:
            strength: The character's strength
            dexterity: The character's dexterity
            
        Returns:
            True if the character meets the requirements
        """
        return (
            strength >= self._strength_requirement and
            dexterity >= self._dexterity_requirement
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the weapon to a dictionary.
        
        Returns:
            Dict containing the weapon's attributes
        """
        weapon_dict = {
            **super().to_dict(),
            "weapon_type": self.weapon_type.value,
            "damage_dice": self.damage_dice.to_dict(),
            "num_damage_dice": self.num_damage_dice,
            "damage_modifier": self.damage_modifier,
            "strength_requirement": self.strength_requirement,
            "dexterity_requirement": self.dexterity_requirement
        }
        
        if self.range_distance is not None:
            weapon_dict["range_distance"] = self.range_distance
            
        return weapon_dict 