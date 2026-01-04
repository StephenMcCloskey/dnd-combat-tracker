# src/utils/command_manager.py
import streamlit as st
from src.utils.command_stack import Command

MAX_COMMAND_HISTORY = 50

def initialize_command_stack():
    """Initialize command stack in session state"""
    if 'command_stack' not in st.session_state:
        st.session_state.command_stack = []
    if 'command_stack_position' not in st.session_state:
        st.session_state.command_stack_position = -1

def execute_command(command: Command) -> None:
    """Execute a command and add it to the undo stack"""
    initialize_command_stack()
    
    # Execute the command
    command.execute()
    
    # Clear any "redo" history if we're not at the end
    if st.session_state.command_stack_position < len(st.session_state.command_stack) - 1:
        st.session_state.command_stack = st.session_state.command_stack[:st.session_state.command_stack_position + 1]
    
    # Add to stack
    st.session_state.command_stack.append(command)
    st.session_state.command_stack_position = len(st.session_state.command_stack) - 1
    
    # Limit stack size to MAX_COMMAND_HISTORY
    if len(st.session_state.command_stack) > MAX_COMMAND_HISTORY:
        # Remove oldest command
        st.session_state.command_stack.pop(0)
        st.session_state.command_stack_position -= 1
    
    # Add to combat log
    if 'combat_log' not in st.session_state:
        st.session_state.combat_log = []
    st.session_state.combat_log.append(command.description())

def undo_last_command() -> bool:
    """Undo the last command. Returns True if successful."""
    initialize_command_stack()
    
    if st.session_state.command_stack_position < 0:
        return False  # Nothing to undo
    
    command = st.session_state.command_stack[st.session_state.command_stack_position]
    command.undo()
    st.session_state.command_stack_position -= 1
    
    # Update combat log
    st.session_state.combat_log.append(f"⏪ UNDO: {command.description()}")
    
    return True

def redo_last_command() -> bool:
    """Redo the last undone command. Returns True if successful."""
    initialize_command_stack()
    
    if st.session_state.command_stack_position >= len(st.session_state.command_stack) - 1:
        return False  # Nothing to redo
    
    st.session_state.command_stack_position += 1
    command = st.session_state.command_stack[st.session_state.command_stack_position]
    command.execute()
    
    # Update combat log
    st.session_state.combat_log.append(f"⏩ REDO: {command.description()}")
    
    return True

def can_undo() -> bool:
    """Check if undo is available"""
    initialize_command_stack()
    return st.session_state.command_stack_position >= 0

def can_redo() -> bool:
    """Check if redo is available"""
    initialize_command_stack()
    return st.session_state.command_stack_position < len(st.session_state.command_stack) - 1

def get_command_history() -> list[tuple[str, str]]:
    """Get list of (description, technical_description) tuples for display"""
    initialize_command_stack()
    return [(cmd.description(), cmd.technical_description()) for cmd in st.session_state.command_stack]

def clear_command_stack():
    """Clear the command stack (call when combat ends)"""
    if 'command_stack' in st.session_state:
        st.session_state.command_stack = []
    if 'command_stack_position' in st.session_state:
        st.session_state.command_stack_position = -1