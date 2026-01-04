# src/utils/combat.py (COMPLETE)
import streamlit as st
from src.utils.models import PlayerCombatant, MonsterCombatant, Combatant
from src.utils.commands import (
    AddCombatantCommand,
    RemoveCombatantCommand,
    ApplyDamageCommand,
    ApplyHealingCommand,
    SetTempHPCommand,
    AddConditionCommand,
    RemoveConditionCommand,
    ClearAllConditionsCommand,
    SetExhaustionCommand,
    UpdateDeathSavesCommand,
    FullHealCommand,
    NextTurnCommand,
    PreviousTurnCommand,
)
from src.utils.command_manager import execute_command, clear_command_stack

def initialize_combat_state():
    """Initialize all session state variables for combat tracking"""
    if 'combatants' not in st.session_state:
        st.session_state.combatants: list[Combatant] = []
    
    if 'current_turn_index' not in st.session_state:
        st.session_state.current_turn_index = 0
    
    if 'round_number' not in st.session_state:
        st.session_state.round_number = 1
    
    if 'combat_active' not in st.session_state:
        st.session_state.combat_active = False
    
    if 'combat_log' not in st.session_state:
        st.session_state.combat_log = []

def add_player_combatant(
    name: str,
    initiative: int,
    dex_modifier: int,
    max_hp: int,
    ac: int,
    speed: int,
    class_name: str,
    level: int,
    proficiency_bonus: int,
    has_alert: bool,
    notes: str = ""
) -> None:
    """Add a player character to combat"""
    player: PlayerCombatant = {
        'combatant_type': 'player',
        'name': name,
        'initiative': initiative,
        'dex_modifier': dex_modifier,
        'max_hp': max_hp,
        'current_hp': max_hp,
        'temp_hp': 0,
        'ac': ac,
        'speed': speed,
        'conditions': [],
        'exhaustion': 0,
        'death_saves': {'successes': 0, 'failures': 0},
        'is_stable': False,
        'notes': notes,
        'class_name': class_name,
        'level': level,
        'proficiency_bonus': proficiency_bonus,
        'has_alert': has_alert
    }
    
    cmd = AddCombatantCommand(player)
    execute_command(cmd)

def add_monster_combatant(
    name: str,
    initiative: int,
    dex_modifier: int,
    max_hp: int,
    ac: int,
    speed: int = 30,
    notes: str = "",
    cr: str = "?",
    monster_type: str = "Unknown",
    size: str = "Medium"
) -> None:
    """Add a monster/NPC to combat"""
    monster: MonsterCombatant = {
        'combatant_type': 'monster',
        'name': name,
        'initiative': initiative,
        'dex_modifier': dex_modifier,
        'max_hp': max_hp,
        'current_hp': max_hp,
        'temp_hp': 0,
        'ac': ac,
        'speed': speed,
        'conditions': [],
        'exhaustion': 0,
        'death_saves': {'successes': 0, 'failures': 0},
        'is_stable': False,
        'notes': notes,
        'cr': cr,
        'monster_type': monster_type,
        'size': size
    }
    
    cmd = AddCombatantCommand(monster)
    execute_command(cmd)

def remove_combatant(index: int) -> None:
    """Remove a combatant from the tracker"""
    cmd = RemoveCombatantCommand(index)
    execute_command(cmd)

def apply_damage(index: int, damage: int) -> None:
    """Apply damage to a combatant"""
    if damage <= 0:
        return
    
    cmd = ApplyDamageCommand(index, damage)
    execute_command(cmd)

def apply_healing(index: int, healing: int) -> None:
    """Apply healing to a combatant"""
    if healing <= 0:
        return
    
    cmd = ApplyHealingCommand(index, healing)
    execute_command(cmd)

def set_temp_hp(index: int, temp_hp: int) -> None:
    """Set temporary HP for a combatant"""
    cmd = SetTempHPCommand(index, temp_hp)
    execute_command(cmd)

def add_condition(index: int, condition: str) -> None:
    """Add a condition to a combatant"""
    cmd = AddConditionCommand(index, condition)
    execute_command(cmd)

def remove_condition(index: int, condition: str) -> None:
    """Remove a condition from a combatant"""
    cmd = RemoveConditionCommand(index, condition)
    execute_command(cmd)

def clear_all_conditions(index: int) -> None:
    """Clear all conditions from a combatant"""
    cmd = ClearAllConditionsCommand(index)
    execute_command(cmd)

def set_exhaustion(index: int, level: int) -> None:
    """Set exhaustion level for a combatant"""
    cmd = SetExhaustionCommand(index, level)
    execute_command(cmd)

def update_death_saves(index: int, success_delta: int = 0, failure_delta: int = 0, reset: bool = False) -> None:
    """Update death saving throws"""
    cmd = UpdateDeathSavesCommand(index, success_delta, failure_delta, reset)
    execute_command(cmd)

def full_heal(index: int) -> None:
    """Fully heal a combatant"""
    cmd = FullHealCommand(index)
    execute_command(cmd)

def next_turn() -> None:
    """Advance to the next turn"""
    cmd = NextTurnCommand()
    execute_command(cmd)

def previous_turn() -> None:
    """Go back to the previous turn"""
    cmd = PreviousTurnCommand()
    execute_command(cmd)

def end_combat() -> None:
    """End combat and clear command history"""
    st.session_state.combat_active = False
    st.session_state.combatants = []
    st.session_state.current_turn_index = 0
    st.session_state.round_number = 1
    clear_command_stack()

# Keep legacy log_event for any direct calls
def log_event(message: str):
    """Add an event to the combat log (legacy - prefer commands)"""
    if 'combat_log' not in st.session_state:
        st.session_state.combat_log = []
    st.session_state.combat_log.append(message)

# Legacy function for backward compatibility
def add_combatant(name: str, initiative: int, dex_modifier: int, max_hp: int, ac: int, speed: int = 30):
    """Legacy function - add a generic monster combatant for backward compatibility"""
    add_monster_combatant(
        name=name,
        initiative=initiative,
        dex_modifier=dex_modifier,
        max_hp=max_hp,
        ac=ac,
        speed=speed,
        notes="",
        cr="?",
        monster_type="Unknown",
        size="Medium"
    )