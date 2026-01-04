# src/components/add_combatant_form.py (COMPLETE UPDATE)
import streamlit as st
import random
from src.utils.combat import add_monster_combatant

def render_add_combatant_form():
    """Render the form to add a new combatant (generic monster/NPC)"""
    
    st.subheader("📋 Quick Add (Generic)")
    st.caption("For NPCs and monsters not in the library")
    
    with st.form("add_combatant_form", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Goblin #1")
        
        col1, col2 = st.columns(2)
        with col1:
            dex_modifier = st.number_input("DEX Mod", min_value=-5, max_value=10, value=0, step=1)
            max_hp = st.number_input("Max HP", min_value=1, value=10, step=1)
            speed = st.number_input("Speed", min_value=0, max_value=120, value=30, step=5)
        
        with col2:
            # Initiative with roll button
            init_col1, init_col2 = st.columns([3, 1])
            with init_col1:
                initiative = st.number_input("Initiative", min_value=1, max_value=30, value=10, step=1, key="init_input")
            with init_col2:
                st.markdown("<br/>", unsafe_allow_html=True)  # Spacing
                if st.form_submit_button("🎲", help="Roll initiative (d20 + DEX)"):
                    roll = random.randint(1, 20)
                    st.session_state['rolled_initiative'] = roll + dex_modifier
            
            # Use rolled initiative if available
            if 'rolled_initiative' in st.session_state:
                initiative = st.session_state['rolled_initiative']
                st.caption(f"Rolled: {initiative}")
            
            ac = st.number_input("AC", min_value=1, max_value=30, value=10, step=1)
        
        # Optional fields
        with st.expander("Optional Details"):
            cr = st.text_input("Challenge Rating", value="?", placeholder="e.g., 1/4, 2, 10")
            size = st.selectbox("Size", ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"], index=2)
            monster_type = st.text_input("Type", value="Unknown", placeholder="e.g., Humanoid, Beast, Dragon")
            notes = st.text_area("Notes", placeholder="Special abilities, attacks, etc.", height=100)
        
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
                    notes=notes.strip() if 'notes' in locals() else "",
                    cr=cr if 'cr' in locals() else "?",
                    monster_type=monster_type if 'monster_type' in locals() else "Unknown",
                    size=size if 'size' in locals() else "Medium"
                )
                # Clear rolled initiative
                if 'rolled_initiative' in st.session_state:
                    del st.session_state['rolled_initiative']
                st.rerun()
            else:
                st.error("Please enter a name")