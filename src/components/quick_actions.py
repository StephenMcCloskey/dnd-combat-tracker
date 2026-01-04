# src/components/combatant_card.py (COMPLETE UPDATE)
import streamlit as st
from src.utils.combat import (
    apply_damage, apply_healing, set_temp_hp, remove_combatant, 
    add_condition, remove_condition, set_exhaustion, update_death_saves
)

def render_quick_actions(combatant, index):
    """Render quick action buttons for common operations"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Toggle Prone
        if "Prone" in combatant['conditions']:
            if st.button("🧍 Stand Up", key=f"standup_{index}", use_container_width=True):
                # Import here to avoid circular imports
                from src.utils.combat import remove_condition
                remove_condition(index, "Prone")
                st.rerun()
        else:
            if st.button("🤕 Knock Prone", key=f"prone_{index}", use_container_width=True):
                # Import here to avoid circular imports
                from src.utils.combat import add_condition
                add_condition(index, "Prone")
                st.rerun()
    
    with col2:
        # Toggle Unconscious
        if "Unconscious" in combatant['conditions']:
            if st.button("😊 Wake Up", key=f"wakeup_{index}", use_container_width=True):
                # Import here to avoid circular imports
                from src.utils.combat import remove_condition
                remove_condition(index, "Unconscious")
                st.rerun()
        else:
            if st.button("😵 Unconscious", key=f"unconscious_{index}", use_container_width=True):
                # Import here to avoid circular imports
                from src.utils.combat import add_condition
                add_condition(index, "Unconscious")
                st.rerun()
    
    with col3:
        # Full Heal
        if st.button("✨ Full Heal", key=f"fullheal_{index}", use_container_width=True, type="primary"):
            # Import here to avoid circular imports
            from src.utils.combat import full_heal
            full_heal(index)
            st.rerun()
    
    with col4:
        # Clear All Conditions
        if combatant['conditions']:
            if st.button("🧹 Clear Conditions", key=f"clearcond_{index}", use_container_width=True):
                # Import here to avoid circular imports
                from src.utils.combat import clear_all_conditions
                clear_all_conditions(index)
                st.rerun()

def get_hp_color(current, maximum):
    """Return color based on HP percentage"""
    if current == 0:
        return "gray"
    pct = current / maximum
    if pct > 0.5:
        return "green"
    elif pct > 0.25:
        return "orange"
    else:
        return "red"

def render_combatant_card(combatant, index, is_current_turn, view_mode='compact'):
    """Render a card for a single combatant
    
    Args:
        combatant: Combatant data dict
        index: Index in combatants list
        is_current_turn: Whether this is the active combatant
        view_mode: 'detailed', 'compact', or 'dense'
    """
    
    # Create title with status indicators
    title_parts = [f"**{combatant['name']}**"]
    
    # Add type indicator
    if combatant.get('combatant_type') == 'player':
        title_parts.append(f"👥 {combatant.get('class_name', 'Player')} {combatant.get('level', '?')}")
    else:
        cr = combatant.get('cr', '?')
        title_parts.append(f"👹 CR {cr}")
    
    title_parts.append(f"Init: {combatant['initiative']}")
    title_parts.append(f"AC: {combatant['ac']}")
    
    # Add status indicators
    status_icons = []
    if combatant['current_hp'] == 0:
        status_icons.append("💀")
    elif combatant['current_hp'] < combatant['max_hp'] * 0.25:
        status_icons.append("🩸")
    
    if combatant['conditions']:
        status_icons.append(f"⚠️({len(combatant['conditions'])})")
    
    if combatant['exhaustion'] > 0:
        status_icons.append(f"😫({combatant['exhaustion']})")
    
    if status_icons:
        title_parts.append(" ".join(status_icons))
    
    title = " | ".join(title_parts)
    
    # Choose rendering based on view mode
    if view_mode == 'dense':
        render_dense_card(combatant, index, is_current_turn, title)
    elif view_mode == 'compact':
        render_compact_card(combatant, index, is_current_turn, title)
    else:  # detailed
        render_detailed_card(combatant, index, is_current_turn, title)

def render_dense_card(combatant, index, is_current_turn, title):
    """Render ultra-compact card for dense view"""
    
    # Compact container
    with st.container():
        # Header with name and quick stats
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{title}**")
        
        with col2:
            if st.button("🗑️", key=f"remove_dense_{index}", help="Remove", use_container_width=True):
                remove_combatant(index)
                st.rerun()
        
        # HP bar
        hp_pct = combatant['current_hp'] / combatant['max_hp'] if combatant['max_hp'] > 0 else 0
        color = get_hp_color(combatant['current_hp'], combatant['max_hp'])
        st.progress(hp_pct, text=f"HP: {combatant['current_hp']}/{combatant['max_hp']}")
        
        # Quick actions row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"dmg_dense_{index}", clear_on_submit=True):
                dmg = st.number_input("Damage", 0, 999, 0, key=f"dmg_d_{index}", label_visibility="collapsed")
                if st.form_submit_button("💥", use_container_width=True):
                    apply_damage(index, dmg)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_dense_{index}", clear_on_submit=True):
                heal = st.number_input("Heal", 0, 999, 0, key=f"heal_d_{index}", label_visibility="collapsed")
                if st.form_submit_button("💚", use_container_width=True):
                    apply_healing(index, heal)
                    st.rerun()
        
        with col3:
            if st.button("📋", key=f"expand_dense_{index}", help="Show details", use_container_width=True):
                st.session_state[f'expand_{index}'] = not st.session_state.get(f'expand_{index}', False)
                st.rerun()
        
        # Expandable details
        if st.session_state.get(f'expand_{index}', False):
            with st.expander("Details", expanded=True):
                render_compact_card(combatant, index, is_current_turn, title, in_dense=True)

def render_compact_card(combatant, index, is_current_turn, title, in_dense=False):
    """Render compact card - good balance of info and space"""
    
    # Main card in expander
    expanded = is_current_turn if not in_dense else True
    
    with st.expander(title, expanded=expanded):
        
        # Single row stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"**HP:** {combatant['current_hp']}/{combatant['max_hp']}")
            hp_pct = combatant['current_hp'] / combatant['max_hp'] if combatant['max_hp'] > 0 else 0
            st.progress(hp_pct, text=None)
            if combatant['temp_hp'] > 0:
                st.caption(f"Temp: {combatant['temp_hp']}")
        
        with col2:
            st.markdown(f"**AC:** {combatant['ac']}")
            st.markdown(f"**Speed:** {combatant['speed']}")
        
        with col3:
            st.markdown(f"**DEX:** {combatant['dex_modifier']:+d}")
            if combatant.get('combatant_type') == 'player':
                st.markdown(f"**Prof:** +{combatant.get('proficiency_bonus', 0)}")
        
        with col4:
            # Type-specific info
            if combatant.get('combatant_type') == 'player':
                st.markdown(f"**Class:** {combatant.get('class_name', 'Unknown')}")
                st.markdown(f"**Level:** {combatant.get('level', '?')}")
            else:
                st.markdown(f"**CR:** {combatant.get('cr', '?')}")
                st.markdown(f"**Type:** {combatant.get('size', 'Medium')}")
        
        # HP Management - compact
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"damage_form_c_{index}", clear_on_submit=True):
                damage = st.number_input("Damage", min_value=0, step=1, key=f"dmg_c_{index}")
                if st.form_submit_button("💥", use_container_width=True):
                    apply_damage(index, damage)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_form_c_{index}", clear_on_submit=True):
                healing = st.number_input("Heal", min_value=0, step=1, key=f"heal_c_{index}")
                if st.form_submit_button("💚", use_container_width=True):
                    apply_healing(index, healing)
                    st.rerun()
        
        with col3:
            with st.form(f"temp_hp_form_c_{index}", clear_on_submit=True):
                temp_hp = st.number_input("Temp", min_value=0, step=1, key=f"temp_c_{index}")
                if st.form_submit_button("🛡️", use_container_width=True):
                    set_temp_hp(index, temp_hp)
                    st.rerun()
        
        # Conditions - compact display
        if combatant['conditions'] or combatant['exhaustion'] > 0:
            st.markdown("---")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if combatant['conditions']:
                    st.markdown("**Conditions:** " + ", ".join([f"`{c}`" for c in combatant['conditions']]))
            
            with col2:
                if combatant['exhaustion'] > 0:
                    st.markdown(f"**Exhaustion:** {combatant['exhaustion']}")
        
        # Show full controls button
        if not in_dense:
            if st.button("⚙️ Full Controls", key=f"full_ctrl_{index}", use_container_width=True):
                st.session_state.view_mode = 'detailed'
                st.rerun()

def render_detailed_card(combatant, index, is_current_turn, title):
    """Render full detailed card - original view"""
    
    with st.expander(title, expanded=is_current_turn):
        
        # Type-specific header info
        if combatant.get('combatant_type') == 'player':
            st.markdown(f"**👥 Player Character** - {combatant.get('class_name', 'Unknown')} (Level {combatant.get('level', '?')})")
            if combatant.get('has_alert'):
                st.caption("✓ Alert Feat (proficiency to initiative)")
        else:
            monster_info = f"**👹 Monster/NPC** - CR {combatant.get('cr', '?')}"
            if combatant.get('monster_type'):
                monster_info += f" | {combatant.get('size', 'Medium')} {combatant.get('monster_type', 'Unknown')}"
            st.markdown(monster_info)
        
        st.markdown("---")
        
        # HP Display
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            hp_pct = combatant['current_hp'] / combatant['max_hp'] if combatant['max_hp'] > 0 else 0
            color = get_hp_color(combatant['current_hp'], combatant['max_hp'])
            
            st.markdown(f"**HP:** {combatant['current_hp']} / {combatant['max_hp']}")
            st.progress(hp_pct, text=None)
            
            if combatant['temp_hp'] > 0:
                st.markdown(f"**Temp HP:** {combatant['temp_hp']}")
        
        with col2:
            st.metric("AC", combatant['ac'])
        
        with col3:
            st.metric("Speed", combatant['speed'])
        
        # HP Management
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"damage_form_{index}", clear_on_submit=True):
                damage = st.number_input("Damage", min_value=0, step=1, key=f"dmg_{index}")
                if st.form_submit_button("💥 Apply Damage", use_container_width=True):
                    apply_damage(index, damage)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_form_{index}", clear_on_submit=True):
                healing = st.number_input("Healing", min_value=0, step=1, key=f"heal_{index}")
                if st.form_submit_button("💚 Heal", use_container_width=True):
                    apply_healing(index, healing)
                    st.rerun()
        
        with col3:
            with st.form(f"temp_hp_form_{index}", clear_on_submit=True):
                temp_hp = st.number_input("Temp HP", min_value=0, step=1, key=f"temp_{index}")
                if st.form_submit_button("🛡️ Set Temp HP", use_container_width=True):
                    set_temp_hp(index, temp_hp)
                    st.rerun()
        
        # Conditions and Exhaustion
        st.markdown("---")
        st.markdown("### Conditions & Status")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Conditions:**")
            
            # Available conditions
            all_conditions = [
                "Blinded", "Charmed", "Deafened", "Frightened", 
                "Grappled", "Incapacitated", "Invisible", "Paralyzed", 
                "Petrified", "Poisoned", "Prone", "Restrained", 
                "Stunned", "Unconscious"
            ]
            
            # Display current conditions as tags
            if combatant['conditions']:
                condition_tags = " ".join([f"`{c}`" for c in combatant['conditions']])
                st.markdown(condition_tags)
            else:
                st.text("None")
            
            # Add condition
            col_add, col_remove = st.columns(2)
            
            with col_add:
                new_condition = st.selectbox(
                    "Add condition",
                    [""] + [c for c in all_conditions if c not in combatant['conditions']],
                    key=f"add_cond_{index}",
                    label_visibility="collapsed"
                )
                if new_condition and st.button("➕ Add", key=f"btn_add_cond_{index}", use_container_width=True):
                    add_condition(index, new_condition)
                    st.rerun()
            
            with col_remove:
                if combatant['conditions']:
                    remove_cond = st.selectbox(
                        "Remove condition",
                        [""] + combatant['conditions'],
                        key=f"remove_cond_{index}",
                        label_visibility="collapsed"
                    )
                    if remove_cond and st.button("➖ Remove", key=f"btn_remove_cond_{index}", use_container_width=True):
                        remove_condition(index, remove_cond)
                        st.rerun()
        
        with col2:
            st.markdown("**Exhaustion Level:**")
            
            current_exhaustion = combatant['exhaustion']
            
            # Display exhaustion level with effects
            if current_exhaustion > 0:
                exhaustion_effects = {
                    1: "Disadvantage on ability checks",
                    2: "Speed halved",
                    3: "Disadvantage on attacks & saves",
                    4: "HP max halved",
                    5: "Speed reduced to 0",
                    6: "Death"
                }
                
                st.markdown(f"**Level {current_exhaustion}**")
                
                # Show all cumulative effects
                for level in range(1, min(current_exhaustion + 1, 7)):
                    st.caption(f"• {exhaustion_effects[level]}")
            else:
                st.text("None")
            
            # Buttons to adjust exhaustion
            col_minus, col_plus = st.columns(2)
            
            with col_minus:
                if st.button("➖", key=f"exhaust_minus_{index}", use_container_width=True, disabled=current_exhaustion == 0):
                    set_exhaustion(index, max(0, current_exhaustion - 1))
                    st.rerun()
            
            with col_plus:
                if st.button("➕", key=f"exhaust_plus_{index}", use_container_width=True, disabled=current_exhaustion >= 6):
                    set_exhaustion(index, min(6, current_exhaustion + 1))
                    st.rerun()
        
        # Quick Actions
        st.markdown("---")
        render_quick_actions(combatant, index)
        
        # Death Saves (if at 0 HP)
        if combatant['current_hp'] == 0:
            st.markdown("---")
            st.markdown("### ⚠️ Death Saving Throws")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Successes**")
                success_count = combatant['death_saves']['successes']
                success_str = "✅ " * success_count + "⬜ " * (3 - success_count)
                st.markdown(success_str)
                
                if st.button("➕ Success", key=f"success_{index}", use_container_width=True):
                    update_death_saves(index, success_delta=1)
                    st.rerun()
            
            with col2:
                st.markdown("**Failures**")
                failure_count = combatant['death_saves']['failures']
                failure_str = "❌ " * failure_count + "⬜ " * (3 - failure_count)
                st.markdown(failure_str)
                
                if st.button("➕ Failure", key=f"failure_{index}", use_container_width=True):
                    update_death_saves(index, failure_delta=1)
                    st.rerun()
            
            with col3:
                if combatant['is_stable']:
                    st.success("Stable")
                
                if st.button("🔄 Reset", key=f"reset_death_{index}", use_container_width=True):
                    update_death_saves(index, reset=True)
                    st.rerun()
        
        # Notes
        st.markdown("---")
        st.markdown("### 📝 Notes")
        
        # Show different note sections for players vs monsters
        if combatant.get('combatant_type') == 'player':
            st.caption("Class features, feats, attacks, spells, etc.")
        else:
            st.caption("Special abilities, actions, traits")
        
        notes = st.text_area(
            "Notes", 
            value=combatant['notes'], 
            key=f"notes_{index}", 
            height=150,
            label_visibility="collapsed"
        )
        if notes != combatant['notes']:
            combatant['notes'] = notes
        
        # Remove button
        st.markdown("---")
        if st.button("🗑️ Remove from Combat", key=f"remove_{index}", type="secondary", use_container_width=True):
            remove_combatant(index)
            st.rerun()