# src/components/quick_stats.py
"""Quick statistics display for header and sidebar."""

import streamlit as st
from src.constants import ICONS


def get_quick_stats() -> dict:
    """Get quick combat statistics.
    
    Returns:
        Dictionary with total, alive, and down counts.
    """
    combatants = st.session_state.get('combatants', [])
    
    total = len(combatants)
    alive = sum(1 for c in combatants if c['current_hp'] > 0)
    down = total - alive
    
    return {
        'total': total,
        'alive': alive,
        'down': down,
    }


def render_quick_stats_inline() -> None:
    """Render quick stats as inline metrics (for header)."""
    stats = get_quick_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total", stats['total'])
    
    with col2:
        st.metric("Alive", stats['alive'])
    
    with col3:
        st.metric("Down", stats['down'])


def render_quick_stats_compact() -> None:
    """Render quick stats in a compact format (for tight spaces)."""
    stats = get_quick_stats()
    
    st.markdown(
        f"**Total:** {stats['total']} | "
        f"**Alive:** {stats['alive']} | "
        f"**Down:** {stats['down']}"
    )


def render_quick_stats_html() -> None:
    """Render quick stats as styled HTML badges."""
    stats = get_quick_stats()
    
    html = f"""
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center;">
        <span class="header-stat">
            <span class="header-stat-label">Total</span>
            <span class="header-stat-value">{stats['total']}</span>
        </span>
        <span class="header-stat">
            <span class="header-stat-label">Alive</span>
            <span class="header-stat-value" style="color: #228B22;">{stats['alive']}</span>
        </span>
        <span class="header-stat">
            <span class="header-stat-label">Down</span>
            <span class="header-stat-value" style="color: #8B0000;">{stats['down']}</span>
        </span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_quick_stats_sidebar() -> None:
    """Render quick stats for sidebar (vertical layout with metrics)."""
    st.subheader("📊 Quick Stats")
    
    stats = get_quick_stats()
    
    st.metric("Combatants", stats['total'])
    st.metric("Alive", stats['alive'])
    
    if stats['down'] > 0:
        st.metric("Down", stats['down'], delta=-stats['down'], delta_color="inverse")
    else:
        st.metric("Down", stats['down'])


def render_round_indicator() -> None:
    """Render the current round number."""
    if not st.session_state.get('combat_active', False):
        return
    
    round_num = st.session_state.get('round_number', 1)
    
    st.markdown(
        f'<div class="round-display">Round {round_num}</div>',
        unsafe_allow_html=True
    )


def render_combat_status_badge() -> None:
    """Render a badge showing combat active/inactive status."""
    if st.session_state.get('combat_active', False):
        st.markdown(
            '<div class="combat-status combat-active">⚔️ Combat Active</div>',
            unsafe_allow_html=True
        )
    else:
        combatants = st.session_state.get('combatants', [])
        if combatants:
            st.markdown(
                f'<div class="combat-status combat-inactive">⏸️ Ready ({len(combatants)} combatants)</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="combat-status combat-inactive">➕ Add Combatants</div>',
                unsafe_allow_html=True
            )