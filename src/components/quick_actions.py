# src/components/quick_actions.py
"""Quick action buttons for combatants.

Note: This module is kept for backward compatibility.
The main quick actions are now integrated into combatant_card.py.
"""

import streamlit as st
from src.utils.combat import (
    add_condition, remove_condition, full_heal, clear_all_conditions
)


def render_quick_actions(combatant: dict, index: int):
    """Render quick action buttons for common operations.
    
    Args:
        combatant: Combatant data dictionary
        index: Index in the combatants list
    """
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Toggle Prone
        if "Prone" in combatant['conditions']:
            if st.button("🧍 Stand Up", key=f"standup_{index}", use_container_width=True):
                remove_condition(index, "Prone")
                st.rerun()
        else:
            if st.button("🤕 Knock Prone", key=f"prone_{index}", use_container_width=True):
                add_condition(index, "Prone")
                st.rerun()
    
    with col2:
        # Toggle Unconscious
        if "Unconscious" in combatant['conditions']:
            if st.button("😊 Wake Up", key=f"wakeup_{index}", use_container_width=True):
                remove_condition(index, "Unconscious")
                st.rerun()
        else:
            if st.button("😵 Unconscious", key=f"unconscious_{index}", use_container_width=True):
                add_condition(index, "Unconscious")
                st.rerun()
    
    with col3:
        # Full Heal
        if st.button("✨ Full Heal", key=f"fullheal_{index}", use_container_width=True, type="primary"):
            full_heal(index)
            st.rerun()
    
    with col4:
        # Clear All Conditions
        if combatant['conditions']:
            if st.button("🧹 Clear Conditions", key=f"clearcond_{index}", use_container_width=True):
                clear_all_conditions(index)
                st.rerun()


def get_hp_color(current: int, maximum: int) -> str:
    """Return color based on HP percentage.
    
    Args:
        current: Current HP
        maximum: Maximum HP
        
    Returns:
        Color string: 'gray', 'red', 'orange', or 'green'
    """
    if current == 0:
        return "gray"
    pct = current / maximum
    if pct > 0.5:
        return "green"
    elif pct > 0.25:
        return "orange"
    else:
        return "red"