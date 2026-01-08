# src/styles/__init__.py
"""Styling module for the D&D Combat Tracker."""

import streamlit as st
from .main import get_main_styles
from .sidebar import get_sidebar_styles
from .header import get_header_styles
from .components import get_component_styles


def apply_all_styles() -> None:
    """Apply all CSS styles to the Streamlit app."""
    st.markdown(get_main_styles(), unsafe_allow_html=True)
    st.markdown(get_sidebar_styles(), unsafe_allow_html=True)
    st.markdown(get_header_styles(), unsafe_allow_html=True)
    st.markdown(get_component_styles(), unsafe_allow_html=True)


__all__ = [
    "apply_all_styles",
    "get_main_styles",
    "get_sidebar_styles",
    "get_header_styles",
    "get_component_styles",
]