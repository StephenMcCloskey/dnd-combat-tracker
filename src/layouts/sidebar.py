# src/layouts/sidebar.py
"""Sidebar layout with combat log."""

import streamlit as st
from src.components.combat_log import render_combat_log


def render_sidebar() -> None:
    """Render the sidebar with combat log."""
    
    with st.sidebar:
        # Combat Log takes the full sidebar
        render_combat_log()
        
        st.divider()
        
        # Footer with tips
        _render_sidebar_footer()


def _render_sidebar_footer() -> None:
    """Render sidebar footer with helpful tips."""
    
    st.markdown("### 💡 Quick Tips")
    
    tips = [
        "**Undo/Redo**: Use ⏪/⏩ or Ctrl+Z/Ctrl+Shift+Z",
        "**View Modes**: Switch between Detailed/Compact/Dense in Combat tab",
        "**Death Saves**: Players at 0 HP get prompted automatically",
        "**Auto-Save**: Player roster and monster library save automatically",
    ]
    
    for tip in tips:
        st.caption(tip)


def render_sidebar_minimal() -> None:
    """Render a minimal sidebar (combat log only, no tips)."""
    
    with st.sidebar:
        render_combat_log()