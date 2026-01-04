# src/utils/command_stack.py
from typing import Protocol, Any
from copy import deepcopy
import streamlit as st

class Command(Protocol):
    """Protocol for commands that can be undone"""
    
    def execute(self) -> None:
        """Execute the command"""
        ...
    
    def undo(self) -> None:
        """Undo the command"""
        ...
    
    def description(self) -> str:
        """Human-readable description for the log"""
        ...
    
    def technical_description(self) -> str:
        """Technical description for command history"""
        ...

class CombatCommand:
    """Base class for combat commands with undo support"""
    
    def __init__(self):
        self.before_state: dict[str, Any] = {}
        self.after_state: dict[str, Any] = {}
    
    def capture_state(self, keys: list[str]) -> dict:
        """Capture specific parts of session state"""
        return {
            key: deepcopy(st.session_state.get(key))
            for key in keys
        }
    
    def restore_state(self, state: dict) -> None:
        """Restore captured state"""
        for key, value in state.items():
            st.session_state[key] = deepcopy(value)
    
    def technical_description(self) -> str:
        """Default technical description - can be overridden"""
        return self.description()