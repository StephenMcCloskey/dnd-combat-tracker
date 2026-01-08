# src/layouts/sticky_header.py
"""Sticky header layout with title, quick stats, and combat controls."""

import streamlit as st
from src.components.combat_controls import (
    render_turn_indicator,
    render_end_combat_warning,
)
from src.config import PAGE_TITLE, PAGE_ICON
from src.utils.command_manager import undo_last_command, redo_last_command, can_undo, can_redo


def render_sticky_header() -> None:
    """Render the sticky header with title, stats, and controls."""
    
    header = st.container()
    
    with header:
        combat_active = st.session_state.get('combat_active', False)
        
        if combat_active:
            _render_active_combat_header()
        else:
            _render_inactive_combat_header()
        
        st.divider()
    
    render_end_combat_warning()


def _render_active_combat_header() -> None:
    """Render header when combat is active."""
    
    combatants = st.session_state.get('combatants', [])
    alive = sum(1 for c in combatants if c['current_hp'] > 0)
    down = len(combatants) - alive
    
    # Row 1: Title (centered)
    st.markdown(f"<h2 style='text-align: center; margin: 0;'>{PAGE_ICON} {PAGE_TITLE}</h2>", unsafe_allow_html=True)
    
    # Row 2: Stats (small inline, centered)
    st.markdown(
        f"<p style='text-align: center; margin: 0.25rem 0;'><strong>Total:</strong> {len(combatants)} · <strong>Alive:</strong> {alive} · <strong>Down:</strong> {down}</p>",
        unsafe_allow_html=True
    )
    
    # Row 3: Controls | Turn Indicator
    c_undo, c_redo, c_prev, c_next, c_end, c_turn = st.columns([0.4, 0.4, 0.6, 0.6, 0.6, 3])
    
    with c_undo:
        st.button("⏪", use_container_width=True, key="hdr_undo",
                  disabled=not can_undo(), help="Undo",
                  on_click=_do_undo)
    
    with c_redo:
        st.button("⏩", use_container_width=True, key="hdr_redo",
                  disabled=not can_redo(), help="Redo",
                  on_click=_do_redo)
    
    with c_prev:
        st.button("◀ Prev", use_container_width=True, key="hdr_prev",
                  on_click=_do_prev)
    
    with c_next:
        st.button("Next ▶", use_container_width=True, key="hdr_next",
                  on_click=_do_next)
    
    with c_end:
        st.button("🛑 End", use_container_width=True, key="hdr_end",
                  type="secondary", on_click=_do_end)
    
    with c_turn:
        render_turn_indicator()


def _render_inactive_combat_header() -> None:
    """Render header when combat is not active."""
    
    combatants = st.session_state.get('combatants', [])
    
    # Row 1: Title (centered)
    st.markdown(f"<h2 style='text-align: center; margin: 0;'>{PAGE_ICON} {PAGE_TITLE}</h2>", unsafe_allow_html=True)
    
    if combatants:
        alive = sum(1 for c in combatants if c['current_hp'] > 0)
        down = len(combatants) - alive
        
        # Row 2: Stats (small inline, centered)
        st.markdown(
            f"<p style='text-align: center; margin: 0.25rem 0;'><strong>Total:</strong> {len(combatants)} · <strong>Alive:</strong> {alive} · <strong>Down:</strong> {down}</p>",
            unsafe_allow_html=True
        )
        
        # Row 3: Undo/Redo | Start
        c_undo, c_redo, c_spacer, c_start = st.columns([0.4, 0.4, 4, 1])
        
        with c_undo:
            st.button("⏪", use_container_width=True, key="hdr_undo_i",
                      disabled=not can_undo(), help="Undo",
                      on_click=_do_undo)
        
        with c_redo:
            st.button("⏩", use_container_width=True, key="hdr_redo_i",
                      disabled=not can_redo(), help="Redo",
                      on_click=_do_redo)
        
        with c_start:
            st.button("▶️ Start Combat", use_container_width=True, key="hdr_start",
                      type="primary", on_click=_do_start)
    else:
        # Row 2: Prompt (centered)
        st.markdown(
            "<p style='text-align: center; color: #888; margin: 0.25rem 0;'>Add combatants using the Players and Monsters tabs</p>",
            unsafe_allow_html=True
        )
        
        # Row 3: Undo/Redo only
        c_undo, c_redo, c_spacer = st.columns([0.4, 0.4, 5])
        
        with c_undo:
            st.button("⏪", use_container_width=True, key="hdr_undo_e",
                      disabled=not can_undo(), help="Undo",
                      on_click=_do_undo)
        
        with c_redo:
            st.button("⏩", use_container_width=True, key="hdr_redo_e",
                      disabled=not can_redo(), help="Redo",
                      on_click=_do_redo)


# Button callbacks to avoid st.rerun() in button handlers
def _do_undo():
    undo_last_command()

def _do_redo():
    redo_last_command()

def _do_prev():
    from src.utils.combat import previous_turn
    previous_turn()

def _do_next():
    from src.utils.combat import next_turn
    next_turn()

def _do_end():
    if st.session_state.get('confirm_end_combat', False):
        from src.utils.combat import end_combat
        end_combat()
        st.session_state.confirm_end_combat = False
    else:
        st.session_state.confirm_end_combat = True

def _do_start():
    combatants = st.session_state.get('combatants', [])
    if combatants:
        st.session_state.combatants.sort(
            key=lambda x: (-x['initiative'], -x['dex_modifier'])
        )
        st.session_state.combat_active = True