from src.utils.command_stack import CombatCommand
from src.utils.models import Combatant, PlayerCombatant, MonsterCombatant
import streamlit as st

class AddCombatantCommand(CombatCommand):
    def __init__(self, combatant: Combatant):
        super().__init__()
        self.combatant = combatant
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        st.session_state.combatants.append(self.combatant)
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"Added {self.combatant['name']} to combat"
    
    def technical_description(self) -> str:
        ctype = self.combatant.get('combatant_type', 'unknown')
        return f"AddCombatant(name={self.combatant['name']}, type={ctype}, init={self.combatant['initiative']})"

class RemoveCombatantCommand(CombatCommand):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants', 'current_turn_index'])
        self.combatant_name = st.session_state.combatants[self.index]['name']
        st.session_state.combatants.pop(self.index)
        
        # Adjust current turn index if needed
        if st.session_state.current_turn_index >= len(st.session_state.combatants) and len(st.session_state.combatants) > 0:
            st.session_state.current_turn_index = 0
        
        self.after_state = self.capture_state(['combatants', 'current_turn_index'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"Removed {self.combatant_name} from combat"
    
    def technical_description(self) -> str:
        return f"RemoveCombatant(index={self.index}, name={self.combatant_name})"

class ApplyDamageCommand(CombatCommand):
    def __init__(self, index: int, damage: int):
        super().__init__()
        self.index = index
        self.damage = damage
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        
        # Apply to temp HP first
        if combatant['temp_hp'] > 0:
            if self.damage <= combatant['temp_hp']:
                combatant['temp_hp'] -= self.damage
            else:
                damage_remaining = self.damage - combatant['temp_hp']
                combatant['temp_hp'] = 0
                combatant['current_hp'] = max(0, combatant['current_hp'] - damage_remaining)
        else:
            combatant['current_hp'] = max(0, combatant['current_hp'] - self.damage)
        
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        combatant = st.session_state.combatants[self.index] if self.index < len(st.session_state.combatants) else {'current_hp': '?', 'max_hp': '?'}
        return f"{self.combatant_name} took {self.damage} damage (HP: {combatant['current_hp']}/{combatant['max_hp']})"
    
    def technical_description(self) -> str:
        return f"ApplyDamage(index={self.index}, damage={self.damage})"

class ApplyHealingCommand(CombatCommand):
    def __init__(self, index: int, healing: int):
        super().__init__()
        self.index = index
        self.healing = healing
        self.combatant_name = ""
        self.actual_healing = 0
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        
        old_hp = combatant['current_hp']
        combatant['current_hp'] = min(combatant['max_hp'], combatant['current_hp'] + self.healing)
        self.actual_healing = combatant['current_hp'] - old_hp
        
        # Reset death saves if healed from 0
        if old_hp == 0 and combatant['current_hp'] > 0:
            combatant['death_saves'] = {'successes': 0, 'failures': 0}
            combatant['is_stable'] = False
        
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        combatant = st.session_state.combatants[self.index] if self.index < len(st.session_state.combatants) else {'current_hp': '?', 'max_hp': '?'}
        msg = f"{self.combatant_name} healed {self.actual_healing} HP (HP: {combatant['current_hp']}/{combatant['max_hp']})"
        if self.before_state['combatants'][self.index]['current_hp'] == 0:
            msg += " - recovered from unconsciousness! ✨"
        return msg
    
    def technical_description(self) -> str:
        return f"ApplyHealing(index={self.index}, healing={self.healing})"

class SetTempHPCommand(CombatCommand):
    def __init__(self, index: int, temp_hp: int):
        super().__init__()
        self.index = index
        self.temp_hp = temp_hp
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        combatant['temp_hp'] = max(0, self.temp_hp)
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"{self.combatant_name} gained {self.temp_hp} temporary HP"
    
    def technical_description(self) -> str:
        return f"SetTempHP(index={self.index}, temp_hp={self.temp_hp})"

class AddConditionCommand(CombatCommand):
    def __init__(self, index: int, condition: str):
        super().__init__()
        self.index = index
        self.condition = condition
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        if self.condition not in combatant['conditions']:
            combatant['conditions'].append(self.condition)
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"{self.combatant_name} gained condition: {self.condition}"
    
    def technical_description(self) -> str:
        return f"AddCondition(index={self.index}, condition={self.condition})"

class RemoveConditionCommand(CombatCommand):
    def __init__(self, index: int, condition: str):
        super().__init__()
        self.index = index
        self.condition = condition
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        if self.condition in combatant['conditions']:
            combatant['conditions'].remove(self.condition)
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"{self.combatant_name} lost condition: {self.condition}"
    
    def technical_description(self) -> str:
        return f"RemoveCondition(index={self.index}, condition={self.condition})"

class ClearAllConditionsCommand(CombatCommand):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.combatant_name = ""
        self.cleared_conditions = []
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        self.cleared_conditions = combatant['conditions'].copy()
        combatant['conditions'] = []
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        if self.cleared_conditions:
            return f"{self.combatant_name} cleared all conditions: {', '.join(self.cleared_conditions)}"
        return f"{self.combatant_name} had no conditions to clear"
    
    def technical_description(self) -> str:
        return f"ClearAllConditions(index={self.index})"

class SetExhaustionCommand(CombatCommand):
    def __init__(self, index: int, level: int):
        super().__init__()
        self.index = index
        self.level = level
        self.combatant_name = ""
        self.old_level = 0
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        self.old_level = combatant['exhaustion']
        combatant['exhaustion'] = max(0, min(6, self.level))
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        if self.level > self.old_level:
            msg = f"{self.combatant_name} exhaustion increased to level {self.level}"
            if self.level == 6:
                msg += " 💀 (DEATH)"
        elif self.level < self.old_level:
            msg = f"{self.combatant_name} exhaustion decreased to level {self.level}"
            if self.level == 0:
                msg = f"{self.combatant_name} recovered from exhaustion"
        else:
            msg = f"{self.combatant_name} exhaustion unchanged at level {self.level}"
        return msg
    
    def technical_description(self) -> str:
        return f"SetExhaustion(index={self.index}, level={self.level})"

class UpdateDeathSavesCommand(CombatCommand):
    def __init__(self, index: int, success_delta: int = 0, failure_delta: int = 0, reset: bool = False):
        super().__init__()
        self.index = index
        self.success_delta = success_delta
        self.failure_delta = failure_delta
        self.reset = reset
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        
        if self.reset:
            combatant['death_saves'] = {'successes': 0, 'failures': 0}
            combatant['is_stable'] = False
        else:
            combatant['death_saves']['successes'] = max(0, min(3, combatant['death_saves']['successes'] + self.success_delta))
            combatant['death_saves']['failures'] = max(0, min(3, combatant['death_saves']['failures'] + self.failure_delta))
            
            # Check for stabilization
            if combatant['death_saves']['successes'] >= 3:
                combatant['is_stable'] = True
        
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        if self.reset:
            return f"{self.combatant_name} death saves reset"
        
        msg_parts = []
        if self.success_delta > 0:
            msg_parts.append(f"+{self.success_delta} success")
        if self.failure_delta > 0:
            msg_parts.append(f"+{self.failure_delta} failure")
        
        combatant = st.session_state.combatants[self.index] if self.index < len(st.session_state.combatants) else None
        if combatant and combatant.get('is_stable'):
            msg_parts.append("(STABLE)")
        
        return f"{self.combatant_name} death save: {', '.join(msg_parts)}"
    
    def technical_description(self) -> str:
        return f"UpdateDeathSaves(index={self.index}, success={self.success_delta}, failure={self.failure_delta}, reset={self.reset})"

class FullHealCommand(CombatCommand):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.combatant_name = ""
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['combatants'])
        combatant = st.session_state.combatants[self.index]
        self.combatant_name = combatant['name']
        
        combatant['current_hp'] = combatant['max_hp']
        combatant['death_saves'] = {'successes': 0, 'failures': 0}
        combatant['is_stable'] = False
        combatant['conditions'] = [c for c in combatant['conditions'] if c != "Unconscious"]
        
        self.after_state = self.capture_state(['combatants'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        return f"✨ {self.combatant_name} fully healed"
    
    def technical_description(self) -> str:
        return f"FullHeal(index={self.index})"

class NextTurnCommand(CombatCommand):
    def __init__(self):
        super().__init__()
        self.new_round = False
        self.new_combatant_name = ""
        self.skipped_count = 0
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['current_turn_index', 'round_number'])
        
        self.skipped_count = 0
        
        # Advance turn
        st.session_state.current_turn_index += 1
        
        # Check for new round
        if st.session_state.current_turn_index >= len(st.session_state.combatants):
            st.session_state.current_turn_index = 0
            st.session_state.round_number += 1
            self.new_round = True
        
        # Skip ONLY MONSTERS at 0 HP (not players - they need death saves)
        max_checks = len(st.session_state.combatants)  # Prevent infinite loop
        checks = 0
        
        while checks < max_checks and len(st.session_state.combatants) > 0:
            current_combatant = st.session_state.combatants[st.session_state.current_turn_index]
            
            # If current combatant is a MONSTER at 0 HP, skip to next
            is_player = current_combatant.get('combatant_type') == 'player'
            
            if current_combatant['current_hp'] == 0 and not is_player:
                self.skipped_count += 1
                st.session_state.current_turn_index += 1
                
                # Check for new round again
                if st.session_state.current_turn_index >= len(st.session_state.combatants):
                    st.session_state.current_turn_index = 0
                    st.session_state.round_number += 1
                    self.new_round = True
                
                checks += 1
            else:
                # Found a valid combatant (alive or player at 0 HP)
                break
        
        if len(st.session_state.combatants) > 0:
            self.new_combatant_name = st.session_state.combatants[st.session_state.current_turn_index]['name']
        
        self.after_state = self.capture_state(['current_turn_index', 'round_number'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        if self.new_round:
            msg = f"=== Round {st.session_state.round_number} ==="
        else:
            msg = f"Turn advanced to {self.new_combatant_name}"
        
        if self.skipped_count > 0:
            msg += f" (skipped {self.skipped_count} unconscious monster(s))"
        
        return msg
    
    def technical_description(self) -> str:
        return f"NextTurn(to_index={self.after_state.get('current_turn_index')}, round={self.after_state.get('round_number')}, skipped={self.skipped_count})"

class PreviousTurnCommand(CombatCommand):
    def __init__(self):
        super().__init__()
        self.prev_round = False
        self.prev_combatant_name = ""
        self.skipped_count = 0
    
    def execute(self) -> None:
        self.before_state = self.capture_state(['current_turn_index', 'round_number'])
        
        self.skipped_count = 0
        
        # Go back one turn
        st.session_state.current_turn_index -= 1
        
        # Check for previous round
        if st.session_state.current_turn_index < 0:
            st.session_state.current_turn_index = len(st.session_state.combatants) - 1
            st.session_state.round_number = max(1, st.session_state.round_number - 1)
            self.prev_round = True
        
        # Skip ONLY MONSTERS at 0 HP backwards (not players - they need death saves)
        max_checks = len(st.session_state.combatants)  # Prevent infinite loop
        checks = 0
        
        while checks < max_checks and len(st.session_state.combatants) > 0:
            current_combatant = st.session_state.combatants[st.session_state.current_turn_index]
            
            # If current combatant is a MONSTER at 0 HP, skip backwards
            is_player = current_combatant.get('combatant_type') == 'player'
            
            if current_combatant['current_hp'] == 0 and not is_player:
                self.skipped_count += 1
                st.session_state.current_turn_index -= 1
                
                # Check for previous round again
                if st.session_state.current_turn_index < 0:
                    st.session_state.current_turn_index = len(st.session_state.combatants) - 1
                    st.session_state.round_number = max(1, st.session_state.round_number - 1)
                    self.prev_round = True
                
                checks += 1
            else:
                # Found a valid combatant (alive or player at 0 HP)
                break
        
        if len(st.session_state.combatants) > 0:
            self.prev_combatant_name = st.session_state.combatants[st.session_state.current_turn_index]['name']
        
        self.after_state = self.capture_state(['current_turn_index', 'round_number'])
    
    def undo(self) -> None:
        self.restore_state(self.before_state)
    
    def description(self) -> str:
        if self.prev_round:
            msg = f"=== Back to Round {st.session_state.round_number} ==="
        else:
            msg = f"Turn reverted to {self.prev_combatant_name}"
        
        if self.skipped_count > 0:
            msg += f" (skipped {self.skipped_count} unconscious monster(s))"
        
        return msg
    
    def technical_description(self) -> str:
        return f"PreviousTurn(to_index={self.after_state.get('current_turn_index')}, round={self.after_state.get('round_number')}, skipped={self.skipped_count})"