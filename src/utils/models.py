# src/utils/models.py
from typing import TypedDict, Literal, NotRequired

class DeathSaves(TypedDict):
    successes: int
    failures: int

class BaseCombatant(TypedDict):
    """Base combatant fields shared by all"""
    name: str
    initiative: int
    dex_modifier: int
    max_hp: int
    current_hp: int
    temp_hp: int
    ac: int
    speed: int
    conditions: list[str]
    exhaustion: int
    death_saves: DeathSaves
    is_stable: bool
    notes: str

class PlayerCombatant(BaseCombatant):
    """Player character in combat"""
    combatant_type: Literal['player']
    class_name: str
    level: int
    proficiency_bonus: int
    has_alert: bool

class MonsterCombatant(BaseCombatant):
    """Monster/NPC in combat"""
    combatant_type: Literal['monster']
    cr: NotRequired[str]
    monster_type: NotRequired[str]
    size: NotRequired[str]

# Union type for any combatant
Combatant = PlayerCombatant | MonsterCombatant