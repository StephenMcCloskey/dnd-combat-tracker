# src/components/add_combatant_form.py
"""Manual combatant entry form."""

import streamlit as st
import random
from src.utils.combat import add_monster_combatant
from src.constants import SIZES
from src.config import MAX_INITIATIVE, MIN_INITIATIVE, MAX_AC, MAX_HP


def render_add_combatant_form():
    """Render the form to add a new combatant (generic monster/NPC)."""
    
    st.markdown("#### 📋 Quick Add (Generic)")
    st.caption("For NPCs and monsters not in the library")
    
    with st.form("add_combatant_form", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Goblin #1")
        
        col1, col2 = st.columns(2)
        with col1:
            dex_modifier = st.number_input("DEX Mod", min_value=-5, max_value=10, value=0)
            max_hp = st.number_input("Max HP", min_value=1, max_value=MAX_HP, value=10)
            speed = st.number_input("Speed", min_value=0, max_value=120, value=30, step=5)
        
        with col2:
            # Initiative with roll button
            col_init, col_roll = st.columns([3, 1])
            with col_init:
                initiative = st.number_input("Initiative", min_value=MIN_INITIATIVE, max_value=MAX_INITIATIVE, value=10)
            with col_roll:
                st.markdown("<br/>", unsafe_allow_html=True)
                roll_init = st.form_submit_button("🎲")
            
            if roll_init:
                roll = random.randint(1, 20)
                st.session_state['rolled_initiative'] = roll + dex_modifier
            
            if 'rolled_initiative' in st.session_state:
                initiative = st.session_state['rolled_initiative']
                st.caption(f"Rolled: {initiative}")
            
            ac = st.number_input("AC", min_value=1, max_value=MAX_AC, value=10)
        
        # Optional fields
        with st.expander("Optional Details"):
            cr = st.text_input("Challenge Rating", value="?", placeholder="e.g., 1/4, 2")
            size = st.selectbox("Size", SIZES, index=2)
            monster_type = st.text_input("Type", value="Unknown", placeholder="e.g., Humanoid, Beast")
            notes = st.text_area("Notes", placeholder="Special abilities, attacks...", height=80)
        
        submitted = st.form_submit_button("➕ Add Combatant", use_container_width=True, type="primary")
        
        if submitted:
            if name.strip():
                add_monster_combatant(
                    name=name.strip(),
                    initiative=initiative,
                    dex_modifier=dex_modifier,
                    max_hp=max_hp,
                    ac=ac,
                    speed=speed,
                    notes=notes.strip() if 'notes' in dir() else "",
                    cr=cr if 'cr' in dir() else "?",
                    monster_type=monster_type if 'monster_type' in dir() else "Unknown",
                    size=size if 'size' in dir() else "Medium"
                )
                if 'rolled_initiative' in st.session_state:
                    del st.session_state['rolled_initiative']
                st.rerun()
            else:
                st.error("Please enter a name")