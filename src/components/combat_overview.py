# src/components/combat_overview.py
"""Combat overview dashboard with statistics."""

import streamlit as st


def get_combat_stats() -> dict:
    """Calculate combat statistics.
    
    Returns:
        Dictionary with combat statistics.
    """
    combatants = st.session_state.get('combatants', [])
    
    total = len(combatants)
    alive = sum(1 for c in combatants if c['current_hp'] > 0)
    unconscious = sum(1 for c in combatants if c['current_hp'] == 0)
    
    # Count players vs monsters
    players = sum(1 for c in combatants if c.get('combatant_type') == 'player')
    monsters = total - players
    
    players_alive = sum(
        1 for c in combatants 
        if c.get('combatant_type') == 'player' and c['current_hp'] > 0
    )
    monsters_alive = sum(
        1 for c in combatants 
        if c.get('combatant_type') != 'player' and c['current_hp'] > 0
    )
    
    # Conditions and exhaustion
    conditioned = sum(1 for c in combatants if c['conditions'])
    exhausted = sum(1 for c in combatants if c['exhaustion'] > 0)
    
    # Stabilized
    stabilized = sum(
        1 for c in combatants 
        if c['current_hp'] == 0 and c.get('is_stable', False)
    )
    
    return {
        'total': total,
        'alive': alive,
        'unconscious': unconscious,
        'players': players,
        'monsters': monsters,
        'players_alive': players_alive,
        'monsters_alive': monsters_alive,
        'conditioned': conditioned,
        'exhausted': exhausted,
        'stabilized': stabilized,
    }


def render_combat_overview() -> None:
    """Render the combat overview dashboard."""
    if not st.session_state.get('combat_active', False):
        return
    
    stats = get_combat_stats()
    
    st.markdown("### 📊 Combat Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total", stats['total'])
    
    with col2:
        st.metric("Alive", stats['alive'])
    
    with col3:
        st.metric("Down", stats['unconscious'])
    
    with col4:
        st.metric("Conditions", stats['conditioned'])
    
    with col5:
        st.metric("Exhausted", stats['exhausted'])


def render_combat_overview_detailed() -> None:
    """Render a more detailed combat overview with player/monster breakdown."""
    if not st.session_state.get('combat_active', False):
        return
    
    stats = get_combat_stats()
    
    st.markdown("### 📊 Combat Overview")
    
    # Row 1: Basic counts
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total", stats['total'])
    
    with col2:
        st.metric("Alive", stats['alive'])
    
    with col3:
        st.metric("Down", stats['unconscious'])
    
    with col4:
        st.metric("Stabilized", stats['stabilized'])
    
    with col5:
        st.metric("Conditions", stats['conditioned'])
    
    with col6:
        st.metric("Exhausted", stats['exhausted'])
    
    # Row 2: Player/Monster breakdown
    if stats['players'] > 0 or stats['monsters'] > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Players", f"{stats['players_alive']}/{stats['players']}")
        
        with col2:
            players_down = stats['players'] - stats['players_alive']
            if players_down > 0:
                st.metric("👥 Players Down", players_down, delta=-players_down, delta_color="inverse")
            else:
                st.metric("👥 Players Down", 0)
        
        with col3:
            st.metric("👹 Monsters", f"{stats['monsters_alive']}/{stats['monsters']}")
        
        with col4:
            monsters_down = stats['monsters'] - stats['monsters_alive']
            if monsters_down > 0:
                st.metric("👹 Monsters Down", monsters_down, delta=-monsters_down, delta_color="normal")
            else:
                st.metric("👹 Monsters Down", 0)