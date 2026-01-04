# src/components/command_history.py
import streamlit as st
from src.utils.command_manager import get_command_history

def render_command_history():
    """Render the command history viewer"""
    
    history = get_command_history()
    
    if not history:
        st.info("No commands in history yet")
        return
    
    st.markdown(f"**📋 Command History ({len(history)} commands)**")
    st.caption("Shows last 50 commands. Current position marked with →")
    
    # Show with position indicator
    current_pos = st.session_state.get('command_stack_position', -1)
    
    # Create container with scroll
    container = st.container(height=400)
    
    with container:
        for idx, (description, technical) in enumerate(history):
            # Mark current position
            if idx == current_pos:
                st.markdown(f"**→ {idx + 1}.** {description}")
                with st.expander("🔍 Technical details", expanded=False):
                    st.code(technical, language="python")
            elif idx <= current_pos:
                st.markdown(f"{idx + 1}. {description}")
            else:
                # Grayed out for undone commands
                st.markdown(f"~~{idx + 1}. {description}~~ *(undone)*")