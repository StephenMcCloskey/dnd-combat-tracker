import streamlit as st
from src.utils.combat import update_death_saves
import random

def render_death_save_prompt(combatant, index):
    """Render death saving throw prompt for unconscious players"""
    
    st.markdown("---")
    
    # Create a prominent warning box
    st.markdown("""
    <div style="background-color: #8B0000; padding: 1rem; border-radius: 8px; border: 3px solid #FFD700; margin: 1rem 0;">
        <h3 style="color: #FFD700; margin: 0; text-align: center;">💀 DEATH SAVING THROW REQUIRED 💀</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{combatant['name']}** is unconscious and must make a death saving throw!")
    
    # Show current death saves
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Successes**")
        success_count = combatant['death_saves']['successes']
        success_str = "✅ " * success_count + "⬜ " * (3 - success_count)
        st.markdown(success_str)
    
    with col2:
        st.markdown("**Failures**")
        failure_count = combatant['death_saves']['failures']
        failure_str = "❌ " * failure_count + "⬜ " * (3 - failure_count)
        st.markdown(failure_str)
    
    with col3:
        if combatant['is_stable']:
            st.success("✓ Stable")
        else:
            st.warning("Unstable")
    
    st.markdown("---")
    
    # Roll buttons
    st.markdown("### Roll d20 or enter result:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎲 Roll d20", key=f"death_roll_{index}", use_container_width=True, type="primary"):
            roll = random.randint(1, 20)
            st.session_state[f'death_roll_result_{index}'] = roll
            st.rerun()
    
    with col2:
        manual_roll = st.number_input("Or enter:", min_value=1, max_value=20, value=10, key=f"death_manual_{index}", label_visibility="collapsed")
        if st.button("Use Manual", key=f"death_use_manual_{index}", use_container_width=True):
            st.session_state[f'death_roll_result_{index}'] = manual_roll
            st.rerun()
    
    with col3:
        if st.button("✅ Success", key=f"death_success_{index}", use_container_width=True):
            st.session_state[f'death_roll_result_{index}'] = None
            update_death_saves(index, success_delta=1)
            st.rerun()
    
    with col4:
        if st.button("❌ Failure", key=f"death_failure_{index}", use_container_width=True):
            st.session_state[f'death_roll_result_{index}'] = None
            update_death_saves(index, failure_delta=1)
            st.rerun()
    
    # Show roll result if rolled
    if f'death_roll_result_{index}' in st.session_state and st.session_state[f'death_roll_result_{index}'] is not None:
        roll = st.session_state[f'death_roll_result_{index}']
        
        st.markdown("---")
        
        if roll == 20:
            st.success(f"### 🎉 NATURAL 20! - {combatant['name']} regains 1 HP!")
            if st.button("✨ Apply Recovery", key=f"death_nat20_{index}", use_container_width=True, type="primary"):
                from src.utils.combat import apply_healing
                apply_healing(index, 1)
                st.session_state[f'death_roll_result_{index}'] = None
                st.rerun()
        
        elif roll == 1:
            st.error(f"### 💀 NATURAL 1! - TWO failures!")
            if st.button("Apply 2 Failures", key=f"death_nat1_{index}", use_container_width=True):
                update_death_saves(index, failure_delta=2)
                st.session_state[f'death_roll_result_{index}'] = None
                st.rerun()
        
        elif roll >= 10:
            st.success(f"### ✅ SUCCESS (rolled {roll})")
            if st.button("Apply Success", key=f"death_apply_success_{index}", use_container_width=True):
                update_death_saves(index, success_delta=1)
                st.session_state[f'death_roll_result_{index}'] = None
                st.rerun()
        
        else:
            st.error(f"### ❌ FAILURE (rolled {roll})")
            if st.button("Apply Failure", key=f"death_apply_failure_{index}", use_container_width=True):
                update_death_saves(index, failure_delta=1)
                st.session_state[f'death_roll_result_{index}'] = None
                st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reroll", key=f"death_reroll_{index}", use_container_width=True):
                st.session_state[f'death_roll_result_{index}'] = None
                st.rerun()
    
    st.markdown("---")
    
    # Quick notes about death saves
    with st.expander("ℹ️ Death Saving Throw Rules"):
        st.markdown("""
        **Death Saving Throws:**
        - Roll d20 with no modifiers
        - **10 or higher** = Success
        - **9 or lower** = Failure
        - **Natural 20** = Regain 1 HP (no longer dying)
        - **Natural 1** = 2 Failures
        - **3 Successes** = Stabilized (unconscious but not dying)
        - **3 Failures** = Death
        - Taking damage while down = 1 automatic failure
        - Critical hit within 5ft = 2 automatic failures
        - Any healing brings you back to consciousness
        """)