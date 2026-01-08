# src/components/combat_controls.py
"""Combat control buttons: undo/redo, turn navigation, end combat."""

import streamlit as st
from src.utils.command_manager import undo_last_command, redo_last_command, can_undo, can_redo
from src.utils.combat import next_turn, previous_turn, end_combat


def render_combat_controls() -> None:
    """Render combat control buttons (undo/redo, prev/next, end combat).
    
    Should only be called when combat is active.
    """
    if not st.session_state.get('combat_active', False):
        return
    
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        if st.button("⏪", use_container_width=True, key="ctrl_undo",
                     disabled=not can_undo(), help="Undo (Ctrl+Z)"):
            if undo_last_command():
                st.rerun()
    
    with col2:
        if st.button("⏩", use_container_width=True, key="ctrl_redo",
                     disabled=not can_redo(), help="Redo (Ctrl+Shift+Z)"):
            if redo_last_command():
                st.rerun()
    
    with col3:
        if st.button("⬅️ Prev", use_container_width=True, key="ctrl_prev", help="Previous Turn"):
            previous_turn()
            st.rerun()
    
    with col4:
        if st.button("Next ➡️", use_container_width=True, key="ctrl_next", help="Next Turn"):
            next_turn()
            st.rerun()
    
    with col5:
        if st.button("🛑 End", use_container_width=True, key="ctrl_end", 
                     type="secondary", help="End Combat"):
            if st.session_state.get('confirm_end_combat', False):
                end_combat()
                st.session_state.confirm_end_combat = False
                st.rerun()
            else:
                st.session_state.confirm_end_combat = True
                st.rerun()
    
    with col6:
        if st.session_state.get('confirm_end_combat', False):
            if st.button("✔ Confirm", use_container_width=True, type="primary", 
                        key="ctrl_confirm", help="Confirm End Combat"):
                end_combat()
                st.session_state.confirm_end_combat = False
                st.rerun()
        else:
            st.empty()


def render_turn_indicator() -> None:
    """Render the current turn indicator."""
    if not st.session_state.get('combat_active', False):
        return
    
    if not st.session_state.combatants:
        return
    
    current_combatant = st.session_state.combatants[st.session_state.current_turn_index]
    round_num = st.session_state.round_number
    
    # Check if this is a player at 0 HP (needs death save)
    is_player = current_combatant.get('combatant_type') == 'player'
    at_zero_hp = current_combatant['current_hp'] == 0
    
    if is_player and at_zero_hp:
        st.markdown(
            f'<div class="active-turn-death">💀 R{round_num} - {current_combatant["name"]} - DEATH SAVE</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="active-turn">🎯 R{round_num} - {current_combatant["name"]} (Init: {current_combatant["initiative"]})</div>',
            unsafe_allow_html=True
        )


def render_end_combat_warning() -> None:
    """Render end combat confirmation warning if needed."""
    if st.session_state.get('confirm_end_combat', False):
        st.warning("⚠️ Click Confirm to end combat")


def render_start_combat_button() -> None:
    """Render the start combat button when combat is not active."""
    if st.session_state.get('combat_active', False):
        return
    
    if len(st.session_state.combatants) > 0:
        if st.button("▶️ Start Combat", type="primary", use_container_width=True, key="ctrl_start"):
            # Sort by initiative (highest first), then by DEX modifier for ties
            st.session_state.combatants.sort(
                key=lambda x: (-x['initiative'], -x['dex_modifier'])
            )
            st.session_state.combat_active = True
            st.rerun()
    else:
        st.markdown(
            '<div class="combat-status combat-inactive">➕ Add combatants to begin</div>',
            unsafe_allow_html=True
        )