# app.py
"""D&D 5.5e Combat Tracker - Main Application Entry Point."""

import streamlit as st
from src.styles import apply_all_styles
from src.layouts import render_sticky_header, render_sidebar, render_main_tabs
from src.utils.combat import initialize_combat_state
from src.utils.data_manager import (
    auto_load_player_roster,
    auto_load_monster_library,
    auto_save_player_roster,
    auto_save_monster_library,
)
from src.config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT


def main():
    """Main application entry point."""
    
    # Page configuration (must be first Streamlit command)
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
    )
    
    # Apply all CSS styles
    apply_all_styles()
    
    # Initialize combat state
    initialize_combat_state()
    
    # Auto-load saved data on first run
    _auto_load_data()
    
    # Render layout
    render_sticky_header()
    render_sidebar()
    render_main_tabs()
    
    # Render footer
    _render_footer()
    
    # Auto-save data
    _auto_save_data()


def _auto_load_data():
    """Auto-load player roster and monster library on first run."""
    if 'auto_loaded' not in st.session_state:
        auto_load_player_roster()
        auto_load_monster_library()
        st.session_state.auto_loaded = True


def _auto_save_data():
    """Auto-save player roster and monster library."""
    auto_save_player_roster()
    auto_save_monster_library()


def _render_footer():
    """Render the application footer."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("💡 **Tip:** Use Undo/Redo to fix mistakes")
    
    with col2:
        st.caption("📖 **Reference:** Check the Reference tab for conditions")
    
    with col3:
        st.caption("💾 **Save:** Use Save/Load tab to preserve progress")


if __name__ == "__main__":
    main()