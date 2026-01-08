# src/layouts/main_tabs.py
"""Main content area with tab navigation."""

import streamlit as st
from src.components.combat_overview import render_combat_overview
from src.components.combatant_card import render_combatant_card
from src.components.death_save_prompt import render_death_save_prompt
from src.components.player_character_form import render_player_character_form
from src.components.monster_search import render_monster_search
from src.components.add_combatant_form import render_add_combatant_form
from src.components.conditions_reference import render_conditions_reference
from src.components.save_load_manager import render_save_load_manager
from src.config import DEFAULT_VIEW_MODE
from src.constants import VIEW_MODES


def render_main_tabs() -> None:
    """Render the main content area with tabs."""
    
    # Initialize view mode
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = DEFAULT_VIEW_MODE
    
    # Create tabs
    tab_combat, tab_players, tab_monsters, tab_reference, tab_saveload = st.tabs([
        "⚔️ Combat",
        "👥 Players", 
        "👹 Monsters",
        "📖 Reference",
        "💾 Save/Load",
    ])
    
    with tab_combat:
        _render_combat_tab()
    
    with tab_players:
        _render_players_tab()
    
    with tab_monsters:
        _render_monsters_tab()
    
    with tab_reference:
        _render_reference_tab()
    
    with tab_saveload:
        _render_saveload_tab()


def _render_combat_tab() -> None:
    """Render the Combat tab content."""
    
    combatants = st.session_state.get('combatants', [])
    combat_active = st.session_state.get('combat_active', False)
    
    if not combatants:
        _render_empty_combat_state()
        return
    
    # Combat Overview Dashboard (only when active)
    if combat_active:
        render_combat_overview()
        st.divider()
    
    # View Mode Toggle
    _render_view_mode_toggle()
    
    st.divider()
    
    # Combatant Cards
    _render_combatant_list()


def _render_empty_combat_state() -> None:
    """Render the empty state when no combatants exist."""
    
    st.markdown("""
    <div class="empty-state">
        <h2>⚔️ Ready to Start Combat?</h2>
        <p>Add combatants using the <strong>Players</strong> and <strong>Monsters</strong> tabs to begin tracking your encounter.</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; max-width: 600px; margin: 0 auto;">
            <div class="empty-state-card">
                <strong>👥 Players Tab</strong><br/>
                <span>Add your party members</span>
            </div>
            <div class="empty-state-card">
                <strong>👹 Monsters Tab</strong><br/>
                <span>Search API or add manually</span>
            </div>
            <div class="empty-state-card">
                <strong>💾 Save/Load Tab</strong><br/>
                <span>Load a saved encounter</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_view_mode_toggle() -> None:
    """Render the view mode toggle buttons."""
    
    cols = st.columns(len(VIEW_MODES))
    
    for col, (mode_key, mode_info) in zip(cols, VIEW_MODES.items()):
        with col:
            is_active = st.session_state.view_mode == mode_key
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                f"{mode_info['icon']} {mode_info['name']}",
                use_container_width=True,
                type=button_type,
                key=f"view_mode_{mode_key}",
                help=mode_info['description'],
            ):
                st.session_state.view_mode = mode_key
                st.rerun()


def _render_combatant_list() -> None:
    """Render the list of combatant cards."""
    
    combatants = st.session_state.get('combatants', [])
    combat_active = st.session_state.get('combat_active', False)
    current_turn_index = st.session_state.get('current_turn_index', 0)
    view_mode = st.session_state.get('view_mode', DEFAULT_VIEW_MODE)
    
    for idx, combatant in enumerate(combatants):
        is_current_turn = combat_active and idx == current_turn_index
        
        # Show death save prompt if it's a player's turn and they're at 0 HP
        if is_current_turn:
            is_player = combatant.get('combatant_type') == 'player'
            at_zero_hp = combatant['current_hp'] == 0
            
            if is_player and at_zero_hp:
                render_death_save_prompt(combatant, idx)
        
        render_combatant_card(combatant, idx, is_current_turn, view_mode)


def _render_players_tab() -> None:
    """Render the Players tab content."""
    
    # Player character form already includes its own header
    render_player_character_form()


def _render_monsters_tab() -> None:
    """Render the Monsters tab content."""
    
    # Monster search already includes its own header
    render_monster_search()
    
    st.divider()
    
    # Quick add generic form (has its own header)
    render_add_combatant_form()


def _render_reference_tab() -> None:
    """Render the Reference tab content."""
    
    st.markdown("#### 📖 Quick Reference")
    st.caption("Click on a condition to see its effects")
    
    render_conditions_reference()


def _render_saveload_tab() -> None:
    """Render the Save/Load tab content."""
    
    # Save/load manager has its own header structure
    render_save_load_manager()