# src/components/conditions_reference.py
"""Quick reference guide for conditions and exhaustion."""

import streamlit as st
from src.constants import CONDITIONS, CONDITION_EFFECTS, EXHAUSTION_EFFECTS


def render_conditions_reference():
    """Render the conditions and exhaustion reference as expandable sections."""
    
    # Two columns for conditions
    col1, col2 = st.columns(2)
    
    half = len(CONDITIONS) // 2
    
    with col1:
        st.markdown("##### Conditions")
        for condition in CONDITIONS[:half]:
            with st.expander(condition):
                _render_condition_effects(condition)
    
    with col2:
        st.markdown("##### ​")  # Empty header for alignment (zero-width space)
        for condition in CONDITIONS[half:]:
            with st.expander(condition):
                _render_condition_effects(condition)
    
    st.divider()
    
    # Exhaustion section
    st.markdown("##### Exhaustion")
    
    with st.expander("Exhaustion Levels", expanded=True):
        for level, effect in EXHAUSTION_EFFECTS.items():
            if level == 6:
                st.markdown(f"**Level {level}:** :red[{effect}]")
            else:
                st.markdown(f"**Level {level}:** {effect}")
        
        st.caption("*Effects are cumulative. Long rest removes 1 level (with food/drink).*")


def _render_condition_effects(condition: str) -> None:
    """Render the effects of a condition as a bulleted list."""
    effects_text = CONDITION_EFFECTS.get(condition, "No description")
    
    # Split by bullet points and render each on its own line
    lines = effects_text.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            # Convert • to markdown bullet
            if line.startswith("•"):
                st.markdown(f"- {line[1:].strip()}")
            else:
                st.markdown(line)


def render_conditions_reference_compact():
    """Render a compact version wrapped in a single expander."""
    
    with st.expander("📖 Conditions Quick Reference"):
        tab1, tab2 = st.tabs(["Conditions", "Exhaustion"])
        
        with tab1:
            for condition in CONDITIONS:
                st.markdown(f"**{condition}**")
                _render_condition_effects(condition)
                st.markdown("")
        
        with tab2:
            for level, effect in EXHAUSTION_EFFECTS.items():
                st.markdown(f"**Level {level}:** {effect}")
            st.caption("*Effects are cumulative. Long rest removes 1 level (with food/drink).*")


def render_condition_tooltip(condition: str) -> str:
    """Get tooltip text for a condition."""
    return CONDITION_EFFECTS.get(condition, "Unknown condition")