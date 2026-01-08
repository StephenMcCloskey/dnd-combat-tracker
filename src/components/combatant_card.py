# src/components/combatant_card.py
"""Combatant card display component with multiple view modes."""

import streamlit as st
from src.utils.combat import (
    apply_damage, apply_healing, set_temp_hp, remove_combatant,
    add_condition, remove_condition, set_exhaustion, update_death_saves,
    full_heal, clear_all_conditions,
)
from src.constants import CONDITIONS, EXHAUSTION_EFFECTS, ICONS


def get_hp_color(current: int, maximum: int) -> str:
    """Return color based on HP percentage."""
    if current == 0:
        return "gray"
    pct = current / maximum
    if pct > 0.5:
        return "green"
    elif pct > 0.25:
        return "orange"
    else:
        return "red"


def render_combatant_card(combatant: dict, index: int, is_current_turn: bool, view_mode: str = 'compact'):
    """Render a card for a single combatant.
    
    Args:
        combatant: Combatant data dict
        index: Index in combatants list
        is_current_turn: Whether this is the active combatant
        view_mode: 'detailed', 'compact', or 'dense'
    """
    title = _build_card_title(combatant)
    
    if view_mode == 'dense':
        _render_dense_card(combatant, index, is_current_turn, title)
    elif view_mode == 'compact':
        _render_compact_card(combatant, index, is_current_turn, title)
    else:
        _render_detailed_card(combatant, index, is_current_turn, title)


def _build_card_title(combatant: dict) -> str:
    """Build the title string for a combatant card."""
    name = combatant['name']
    hp = f"{combatant['current_hp']}/{combatant['max_hp']}"
    if combatant['temp_hp'] > 0:
        hp += f"(+{combatant['temp_hp']})"
    
    init = combatant['initiative']
    ac = combatant['ac']
    
    # Status icons
    status = []
    if combatant['current_hp'] == 0:
        status.append(ICONS['dead'])
    elif combatant['current_hp'] < combatant['max_hp'] * 0.25:
        status.append(ICONS['critical'])
    if combatant['conditions']:
        status.append(f"{ICONS['condition']}{len(combatant['conditions'])}")
    if combatant['exhaustion'] > 0:
        status.append(f"{ICONS['exhaustion']}{combatant['exhaustion']}")
    
    status_str = " ".join(status) if status else ""
    
    # Type icon
    type_icon = ICONS['player'] if combatant.get('combatant_type') == 'player' else ICONS['monster']
    
    title = f"{type_icon} **{name}** | HP: {hp} | Init: {init} | AC: {ac}"
    if status_str:
        title += f" | {status_str}"
    
    return title


def _render_dense_card(combatant: dict, index: int, is_current_turn: bool, title: str):
    """Render ultra-compact card for dense view."""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{title}**")
        
        with col2:
            if st.button(ICONS['delete'], key=f"remove_dense_{index}", help="Remove", use_container_width=True):
                remove_combatant(index)
                st.rerun()
        
        # HP bar
        hp_pct = combatant['current_hp'] / combatant['max_hp'] if combatant['max_hp'] > 0 else 0
        st.progress(hp_pct, text=f"HP: {combatant['current_hp']}/{combatant['max_hp']}")
        
        # Quick actions row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"dmg_dense_{index}", clear_on_submit=True):
                dmg = st.number_input("Damage", 0, 999, 0, key=f"dmg_d_{index}", label_visibility="collapsed")
                if st.form_submit_button(ICONS['damage'], use_container_width=True):
                    apply_damage(index, dmg)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_dense_{index}", clear_on_submit=True):
                heal = st.number_input("Heal", 0, 999, 0, key=f"heal_d_{index}", label_visibility="collapsed")
                if st.form_submit_button(ICONS['heal'], use_container_width=True):
                    apply_healing(index, heal)
                    st.rerun()
        
        with col3:
            if st.button("📋", key=f"expand_dense_{index}", help="Show details", use_container_width=True):
                st.session_state[f'expand_{index}'] = not st.session_state.get(f'expand_{index}', False)
                st.rerun()
        
        # Expandable details
        if st.session_state.get(f'expand_{index}', False):
            with st.expander("Details", expanded=True):
                _render_compact_card(combatant, index, is_current_turn, title, in_dense=True)


def _render_compact_card(combatant: dict, index: int, is_current_turn: bool, title: str, in_dense: bool = False):
    """Render compact card - good balance of info and space."""
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
            st.markdown(f"**Speed:** {combatant.get('speed', 30)}")
        
        with col3:
            st.markdown(f"**DEX:** {combatant['dex_modifier']:+d}")
            if combatant.get('combatant_type') == 'player':
                st.markdown(f"**Prof:** +{combatant.get('proficiency_bonus', 0)}")
        
        with col4:
            if combatant.get('combatant_type') == 'player':
                st.markdown(f"**Class:** {combatant.get('class_name', 'Unknown')}")
                st.markdown(f"**Level:** {combatant.get('level', '?')}")
            else:
                st.markdown(f"**CR:** {combatant.get('cr', '?')}")
                st.markdown(f"**Type:** {combatant.get('size', 'Medium')}")
        
        # HP Management
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"damage_form_c_{index}", clear_on_submit=True):
                damage = st.number_input("Damage", min_value=0, step=1, key=f"dmg_c_{index}")
                if st.form_submit_button(ICONS['damage'], use_container_width=True):
                    apply_damage(index, damage)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_form_c_{index}", clear_on_submit=True):
                healing = st.number_input("Heal", min_value=0, step=1, key=f"heal_c_{index}")
                if st.form_submit_button(ICONS['heal'], use_container_width=True):
                    apply_healing(index, healing)
                    st.rerun()
        
        with col3:
            with st.form(f"temp_hp_form_c_{index}", clear_on_submit=True):
                temp_hp = st.number_input("Temp", min_value=0, step=1, key=f"temp_c_{index}")
                if st.form_submit_button(ICONS['shield'], use_container_width=True):
                    set_temp_hp(index, temp_hp)
                    st.rerun()
        
        # Conditions display
        if combatant['conditions'] or combatant['exhaustion'] > 0:
            st.markdown("---")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if combatant['conditions']:
                    st.markdown("**Conditions:** " + ", ".join([f"`{c}`" for c in combatant['conditions']]))
            
            with col2:
                if combatant['exhaustion'] > 0:
                    st.markdown(f"**Exhaustion:** {combatant['exhaustion']}")
        
        # Full controls button
        if not in_dense:
            if st.button("⚙️ Full Controls", key=f"full_ctrl_{index}", use_container_width=True):
                st.session_state.view_mode = 'detailed'
                st.rerun()


def _render_detailed_card(combatant: dict, index: int, is_current_turn: bool, title: str):
    """Render full detailed card - original view."""
    with st.expander(title, expanded=is_current_turn):
        # Type-specific header
        if combatant.get('combatant_type') == 'player':
            st.markdown(f"**{ICONS['player']} Player Character** - {combatant.get('class_name', 'Unknown')} (Level {combatant.get('level', '?')})")
            if combatant.get('has_alert'):
                st.caption("✓ Alert Feat (proficiency to initiative)")
        else:
            monster_info = f"**{ICONS['monster']} Monster/NPC** - CR {combatant.get('cr', '?')}"
            if combatant.get('monster_type'):
                monster_info += f" | {combatant.get('size', 'Medium')} {combatant.get('monster_type', 'Unknown')}"
            st.markdown(monster_info)
        
        st.markdown("---")
        
        # HP Display
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            hp_pct = combatant['current_hp'] / combatant['max_hp'] if combatant['max_hp'] > 0 else 0
            st.markdown(f"**HP:** {combatant['current_hp']} / {combatant['max_hp']}")
            st.progress(hp_pct, text=None)
            if combatant['temp_hp'] > 0:
                st.markdown(f"**Temp HP:** {combatant['temp_hp']}")
        
        with col2:
            st.metric("AC", combatant['ac'])
        
        with col3:
            st.metric("Speed", combatant.get('speed', 30))
        
        # HP Management
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.form(f"damage_form_{index}", clear_on_submit=True):
                damage = st.number_input("Damage", min_value=0, step=1, key=f"dmg_{index}")
                if st.form_submit_button(f"{ICONS['damage']} Apply Damage", use_container_width=True):
                    apply_damage(index, damage)
                    st.rerun()
        
        with col2:
            with st.form(f"heal_form_{index}", clear_on_submit=True):
                healing = st.number_input("Healing", min_value=0, step=1, key=f"heal_{index}")
                if st.form_submit_button(f"{ICONS['heal']} Heal", use_container_width=True):
                    apply_healing(index, healing)
                    st.rerun()
        
        with col3:
            with st.form(f"temp_hp_form_{index}", clear_on_submit=True):
                temp_hp = st.number_input("Temp HP", min_value=0, step=1, key=f"temp_{index}")
                if st.form_submit_button(f"{ICONS['shield']} Set Temp HP", use_container_width=True):
                    set_temp_hp(index, temp_hp)
                    st.rerun()
        
        # Conditions and Exhaustion
        st.markdown("---")
        st.markdown("### Conditions & Status")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Conditions:**")
            
            if combatant['conditions']:
                condition_tags = " ".join([f"`{c}`" for c in combatant['conditions']])
                st.markdown(condition_tags)
            else:
                st.text("None")
            
            col_add, col_remove = st.columns(2)
            
            with col_add:
                available = [c for c in CONDITIONS if c not in combatant['conditions']]
                new_condition = st.selectbox(
                    "Add condition",
                    [""] + available,
                    key=f"add_cond_{index}",
                    label_visibility="collapsed"
                )
                if new_condition and st.button(f"{ICONS['add']} Add", key=f"btn_add_cond_{index}", use_container_width=True):
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
                    if remove_cond and st.button(f"{ICONS['remove']} Remove", key=f"btn_remove_cond_{index}", use_container_width=True):
                        remove_condition(index, remove_cond)
                        st.rerun()
        
        with col2:
            st.markdown("**Exhaustion Level:**")
            current_exhaustion = combatant['exhaustion']
            
            if current_exhaustion > 0:
                st.markdown(f"**Level {current_exhaustion}**")
                for level in range(1, min(current_exhaustion + 1, 7)):
                    st.caption(f"• {EXHAUSTION_EFFECTS[level]}")
            else:
                st.text("None")
            
            col_minus, col_plus = st.columns(2)
            
            with col_minus:
                if st.button(ICONS['remove'], key=f"exhaust_minus_{index}", use_container_width=True, disabled=current_exhaustion == 0):
                    set_exhaustion(index, max(0, current_exhaustion - 1))
                    st.rerun()
            
            with col_plus:
                if st.button(ICONS['add'], key=f"exhaust_plus_{index}", use_container_width=True, disabled=current_exhaustion >= 6):
                    set_exhaustion(index, min(6, current_exhaustion + 1))
                    st.rerun()
        
        # Quick Actions
        st.markdown("---")
        _render_quick_actions(combatant, index)
        
        # Death Saves
        if combatant['current_hp'] == 0:
            st.markdown("---")
            _render_death_saves(combatant, index)
        
        # Notes
        st.markdown("---")
        st.markdown("### 📝 Notes")
        
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
        if st.button(f"{ICONS['delete']} Remove from Combat", key=f"remove_{index}", type="secondary", use_container_width=True):
            remove_combatant(index)
            st.rerun()


def _render_quick_actions(combatant: dict, index: int):
    """Render quick action buttons."""
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if "Prone" in combatant['conditions']:
            if st.button("🧍 Stand Up", key=f"standup_{index}", use_container_width=True):
                remove_condition(index, "Prone")
                st.rerun()
        else:
            if st.button("🤕 Knock Prone", key=f"prone_{index}", use_container_width=True):
                add_condition(index, "Prone")
                st.rerun()
    
    with col2:
        if "Unconscious" in combatant['conditions']:
            if st.button("😊 Wake Up", key=f"wakeup_{index}", use_container_width=True):
                remove_condition(index, "Unconscious")
                st.rerun()
        else:
            if st.button("😵 Unconscious", key=f"unconscious_{index}", use_container_width=True):
                add_condition(index, "Unconscious")
                st.rerun()
    
    with col3:
        if st.button("✨ Full Heal", key=f"fullheal_{index}", use_container_width=True, type="primary"):
            full_heal(index)
            st.rerun()
    
    with col4:
        if combatant['conditions']:
            if st.button("🧹 Clear Conditions", key=f"clearcond_{index}", use_container_width=True):
                clear_all_conditions(index)
                st.rerun()


def _render_death_saves(combatant: dict, index: int):
    """Render death saving throw section."""
    st.markdown("### ⚠️ Death Saving Throws")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Successes**")
        success_count = combatant['death_saves']['successes']
        success_str = f"{ICONS['success']} " * success_count + f"{ICONS['empty']} " * (3 - success_count)
        st.markdown(success_str)
        
        if st.button(f"{ICONS['add']} Success", key=f"success_{index}", use_container_width=True):
            update_death_saves(index, success_delta=1)
            st.rerun()
    
    with col2:
        st.markdown("**Failures**")
        failure_count = combatant['death_saves']['failures']
        failure_str = f"{ICONS['failure']} " * failure_count + f"{ICONS['empty']} " * (3 - failure_count)
        st.markdown(failure_str)
        
        if st.button(f"{ICONS['add']} Failure", key=f"failure_{index}", use_container_width=True):
            update_death_saves(index, failure_delta=1)
            st.rerun()
    
    with col3:
        if combatant['is_stable']:
            st.success("Stable")
        
        if st.button("🔄 Reset", key=f"reset_death_{index}", use_container_width=True):
            update_death_saves(index, reset=True)
            st.rerun()