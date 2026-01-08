# src/components/combat_log.py
"""Combat log display with command history toggle."""

import streamlit as st
from src.components.command_history import render_command_history
from src.config import (
    COMBAT_LOG_DEFAULT_HEIGHT,
    COMBAT_LOG_MIN_HEIGHT,
    COMBAT_LOG_MAX_HEIGHT,
)


def render_combat_log() -> None:
    """Render the combat log with command history toggle."""
    
    # Header with toggle
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📜 Combat Log")
    
    with col2:
        show_commands = st.checkbox(
            "📋", 
            value=False, 
            help="Show command history",
            key="show_command_history_toggle"
        )
    
    if show_commands:
        render_command_history()
    else:
        render_log_entries()


def render_log_entries() -> None:
    """Render the combat log entries."""
    
    # Height slider
    log_height = st.slider(
        "Log Height",
        min_value=COMBAT_LOG_MIN_HEIGHT,
        max_value=COMBAT_LOG_MAX_HEIGHT,
        value=COMBAT_LOG_DEFAULT_HEIGHT,
        step=50,
        key="combat_log_height",
        label_visibility="collapsed"
    )
    
    combat_log = st.session_state.get('combat_log', [])
    
    if combat_log:
        log_container = st.container(height=log_height)
        with log_container:
            # Show most recent entries first (reversed)
            for entry in reversed(combat_log[-50:]):
                st.text(entry)
    else:
        st.info("No events yet. Combat actions will appear here.")
    
    # Clear log button
    if st.button("🗑️ Clear Log", use_container_width=True, key="clear_combat_log"):
        st.session_state.combat_log = []
        st.rerun()


def render_combat_log_compact() -> None:
    """Render a compact version of the combat log (no height slider)."""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**📜 Combat Log**")
    
    with col2:
        show_commands = st.checkbox(
            "📋",
            value=False,
            help="Show command history",
            key="show_command_history_compact"
        )
    
    if show_commands:
        render_command_history()
    else:
        combat_log = st.session_state.get('combat_log', [])
        
        if combat_log:
            # Show last 20 entries in a scrollable container
            log_container = st.container(height=250)
            with log_container:
                for entry in reversed(combat_log[-20:]):
                    st.text(entry)
        else:
            st.caption("No events yet")


def get_log_entry_count() -> int:
    """Get the number of entries in the combat log."""
    return len(st.session_state.get('combat_log', []))


def add_log_entry(message: str) -> None:
    """Add an entry to the combat log.
    
    Note: Prefer using commands which auto-log. This is for manual entries.
    """
    if 'combat_log' not in st.session_state:
        st.session_state.combat_log = []
    st.session_state.combat_log.append(message)