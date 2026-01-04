# app.py (COMPLETE UPDATED VERSION)
import streamlit as st
from src.utils.combat import initialize_combat_state, next_turn, previous_turn, end_combat
from src.components.combatant_card import render_combatant_card
from src.components.add_combatant_form import render_add_combatant_form
from src.components.conditions_reference import render_conditions_reference
from src.components.monster_search import render_monster_search
from src.components.player_character_form import render_player_character_form
from src.components.command_history import render_command_history
from src.components.death_save_prompt import render_death_save_prompt
from src.components.save_load_manager import render_save_load_manager
from src.utils.import_export import export_combat_state, import_combat_state, get_export_filename
from src.utils.command_manager import undo_last_command, redo_last_command, can_undo, can_redo
from src.utils.data_manager import auto_load_player_roster, auto_load_monster_library, auto_save_player_roster, auto_save_monster_library

st.set_page_config(page_title="D&D 5.5e Combat Tracker", layout="wide", page_icon="⚔️")

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(to bottom, #2C1810 0%, #1a0f0a 100%);
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #f8f5f0;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Main title styling */
    h1 {
        color: #8B0000;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #8B0000;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #2C1810 0%, #1a0f0a 100%);
        border-right: 3px solid #8B0000;
        overflow-y: auto;
        overflow-x: hidden;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        overflow-x: hidden;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFD700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        word-wrap: break-word;
    }
    
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {
        color: #f8f5f0 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #8B0000;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #8B0000;
        color: white;
        border: 2px solid #FFD700;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #A52A2A;
        border-color: #FFA500;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #228B22;
        border-color: #32CD32;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #2E8B57;
    }
    
    /* Sidebar inputs */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] textarea {
        background-color: #3a2820;
        color: #f8f5f0;
        border: 1px solid #8B0000;
        max-width: 100%;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #3a2820;
        color: #f8f5f0;
        border: 1px solid #8B0000;
    }
    
    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: #3a2820;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #8B0000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #FFD700 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #f8f5f0 !important;
    }
    
    /* Sidebar file uploader */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #3a2820;
        border: 2px dashed #8B0000;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Combat log container */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(.stTextArea) {
        background-color: #1a1410;
        border: 2px solid #8B0000;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Active turn highlight */
    .active-turn {
        background-color: #90EE90;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    
    /* Combat status badges */
    .combat-status {
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        white-space: nowrap;
    }
    
    .combat-active {
        background-color: #2E8B57;
        color: #90EE90;
        border: 2px solid #32CD32;
    }
    
    .combat-inactive {
        background-color: #8B4513;
        color: #FFE4B5;
        border: 2px solid #D2691E;
        font-size: 1rem;
    }
    
    /* Condition tags */
    code {
        background-color: #FFE4E1;
        color: #8B0000;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        margin: 0.1rem;
    }
    
    /* HP bar styling */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        transition: all 0.2s ease;
    }
    
    /* View mode buttons */
    .stButton > button[kind="secondary"] {
        background-color: rgba(139, 0, 0, 0.3);
        border: 1px solid #8B0000;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: rgba(139, 0, 0, 0.5);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="primary"] {
        background-color: #8B0000;
        border: 2px solid #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Undo/Redo button styling */
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Force metric text to be visible */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #2C1810 !important;
    }
    
    /* Make sure main area metrics have white background */
    .main [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #8B0000;
    }
    
    .main [data-testid="stMetricLabel"] {
        color: #8B0000 !important;
        font-weight: bold;
    }
    
    .main [data-testid="stMetricValue"] {
        color: #2C1810 !important;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0e6d2;
        border-radius: 5px;
        border: 2px solid #8B0000;
        padding: 0.35rem 1rem !important;
        min-height: 2.5rem !important;
    }
    
    /* Expander content padding */
    .streamlit-expanderContent {
        padding: 0.5rem 1rem !important;
    }
    
    /* Tighter margins between expanders */
    .main [data-testid="stExpander"] {
        margin-bottom: 0.15rem !important;
    }
    
    /* Reduce expander header vertical spacing */
    .streamlit-expanderHeader p {
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    /* Text in main area */
    .main h2, .main h3 {
        color: #8B0000;
    }
    
    /* Reduce spacing between combatant cards */
    .main .block-container > div > div > div > div {
        margin-bottom: 0.15rem !important;
    }
    
    /* Reduce divider spacing */
    .main hr {
        margin: 0.25rem 0 !important;
    }
    
    /* Dense mode - ultra tight */
    .main [data-testid="column"] {
        padding: 0.15rem !important;
    }
    
    /* Inline card styling */
    .main [data-testid="stNumberInput"] input {
        text-align: center;
        font-size: 0.9rem;
    }
    
    /* Compact button styling */
    .main .stButton > button {
        padding: 0.25rem 0.5rem;
        font-size: 1.2rem;
        min-height: 2rem;
    }
    
    /* Tighter container spacing */
    .main > div > div > div > div {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_combat_state()

# Auto-load player roster and monster library on first run
if 'auto_loaded' not in st.session_state:
    auto_load_player_roster()
    auto_load_monster_library()
    st.session_state.auto_loaded = True

# Initialize view mode
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'compact'  # compact or detailed

st.markdown("""
<style>
    /* Responsive button text */
    .stButton > button {
        font-size: clamp(0.65rem, 1vw, 0.9rem) !important;
        white-space: nowrap !important;
        padding: 0.3rem 0.5rem !important;
    }
    
    /* Responsive active turn text */
    .active-turn {
        font-size: clamp(0.7rem, 1.3vw, 1rem) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        padding: 0.4rem 0.5rem !important;
    }
    
    /* Responsive title */
    .main h1 {
        font-size: clamp(1.2rem, 2.5vw, 2rem) !important;
        padding: 0.5rem 0 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Ensure columns don't wrap */
    [data-testid="column"] {
        min-width: 0 !important;
        flex-shrink: 1 !important;
    }
    
    /* Make header sticky - works in Streamlit */
    .main > div:nth-child(1) > div:nth-child(1) {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: #f8f5f0;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("⚔️ D&D 5.5e Combat Tracker")

# Combat Controls in Header
if st.session_state.combat_active:
    col1, col2, col3, col4, col5, col6, col7 = st.columns([0.8, 0.8, 1, 1, 4, 1, 0.8])
    
    with col1:
        if st.button("⏪", use_container_width=True, key="header_undo", 
                     disabled=not can_undo(), help="Undo (Ctrl+Z)"):
            if undo_last_command():
                st.rerun()
    
    with col2:
        if st.button("⏩", use_container_width=True, key="header_redo",
                     disabled=not can_redo(), help="Redo (Ctrl+Shift+Z)"):
            if redo_last_command():
                st.rerun()
    
    with col3:
        if st.button("⬅️ Prev", use_container_width=True, key="header_prev", help="Previous Turn"):
            previous_turn()
            st.rerun()
    
    with col4:
        if st.button("Next ➡️", use_container_width=True, key="header_next", help="Next Turn"):
            next_turn()
            st.rerun()
    
    with col5:
        current_combatant = st.session_state.combatants[st.session_state.current_turn_index]
        
        # Check if this is a player at 0 HP
        if current_combatant.get('combatant_type') == 'player' and current_combatant['current_hp'] == 0:
            st.markdown(f'<div class="active-turn" style="background-color: #8B0000; color: #FFD700;">💀 R{st.session_state.round_number} - {current_combatant["name"]} - DEATH SAVE</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="active-turn">🎯 R{st.session_state.round_number} - {current_combatant["name"]} (Init: {current_combatant["initiative"]})</div>', unsafe_allow_html=True)
    
    with col6:
        if st.button("🛑 End", use_container_width=True, key="header_end", type="secondary", help="End Combat"):
            if st.session_state.get('confirm_end_combat', False):
                end_combat()
                st.session_state.confirm_end_combat = False
                st.rerun()
            else:
                st.session_state.confirm_end_combat = True
                st.rerun()
    
    with col7:
        if st.session_state.get('confirm_end_combat', False):
            if st.button("✓", use_container_width=True, type="primary", key="header_confirm", help="Confirm End"):
                end_combat()
                st.session_state.confirm_end_combat = False
                st.rerun()
        else:
            st.empty()
    
    if st.session_state.get('confirm_end_combat', False):
        st.warning("⚠️ Confirm to end combat")
else:
    # When no combat active, show start button or message
    st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <div style="display: inline-block; padding: 0.75rem 2rem; background-color: #8B4513; color: #FFE4B5; border-radius: 8px; border: 2px solid #D2691E; font-size: 1rem; font-weight: bold; white-space: nowrap;">
                ➕ Add combatants
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Show start button below if we have combatants
    if len(st.session_state.combatants) > 0:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("▶️ Start Combat", type="primary", use_container_width=True, key="header_start"):
                # Sort by initiative
                st.session_state.combatants.sort(key=lambda x: (-x['initiative'], -x['dex_modifier']))
                st.session_state.combat_active = True
                st.rerun()

st.divider()

# Sidebar
with st.sidebar:
    st.header("Add Combatants")
    
    # Player characters
    render_player_character_form()
    
    st.divider()
    
    # Monster search
    render_monster_search()
    
    st.divider()
    
    # Add combatant form
    render_add_combatant_form()
    
    st.divider()
    
    # Quick stats
    st.subheader("Quick Stats")
    st.metric("Combatants", len(st.session_state.combatants))
    alive = sum(1 for c in st.session_state.combatants if c['current_hp'] > 0)
    st.metric("Alive", alive)
    
    st.divider()
    
    # Combat Log with Command History toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Combat Log")
    with col2:
        show_commands = st.checkbox("📋", value=False, help="Show command history", key="show_command_history")
    
    if show_commands:
        render_command_history()
    else:
        log_height = st.slider("Log Height", 100, 500, 200, 50, key="log_height")
        
        if st.session_state.combat_log:
            log_container = st.container(height=log_height)
            with log_container:
                for entry in reversed(st.session_state.combat_log[-50:]):
                    st.text(entry)
        else:
            st.text("No events yet")
        
        if st.button("Clear Log", use_container_width=True):
            st.session_state.combat_log = []
            st.rerun()
    
    st.divider()
    
    # Save/Load Manager (replaces old save/load section)
    render_save_load_manager()

# Main area
if len(st.session_state.combatants) == 0:
    # Empty state - responsive and styled
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto; padding: 2rem 1rem;">
        <div style="text-align: center; padding: 3rem 2rem; background-color: rgba(139, 0, 0, 0.1); border: 2px dashed #8B0000; border-radius: 10px;">
            <h2 style="color: #FFD700; margin-bottom: 1rem; font-size: clamp(1.5rem, 4vw, 2rem);">⚔️ Ready to Start Combat?</h2>
            <p style="color: #f8f5f0; font-size: clamp(0.9rem, 2vw, 1.1rem); margin-bottom: 2rem;">
                Add combatants using the sidebar to begin tracking your encounter
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; max-width: 600px; margin: 0 auto;">
                <div style="padding: 1rem; background-color: rgba(0,0,0,0.3); border-radius: 5px;">
                    <strong style="color: #FFD700; font-size: clamp(0.9rem, 2vw, 1rem);">👥 Player Characters</strong><br/>
                    <span style="color: #f8f5f0; font-size: clamp(0.8rem, 1.5vw, 0.9rem);">Add your party members</span>
                </div>
                <div style="padding: 1rem; background-color: rgba(0,0,0,0.3); border-radius: 5px;">
                    <strong style="color: #FFD700; font-size: clamp(0.9rem, 2vw, 1rem);">👹 Monsters</strong><br/>
                    <span style="color: #f8f5f0; font-size: clamp(0.8rem, 1.5vw, 0.9rem);">Search the API library</span>
                </div>
                <div style="padding: 1rem; background-color: rgba(0,0,0,0.3); border-radius: 5px;">
                    <strong style="color: #FFD700; font-size: clamp(0.9rem, 2vw, 1rem);">📋 Quick Add</strong><br/>
                    <span style="color: #f8f5f0; font-size: clamp(0.8rem, 1.5vw, 0.9rem);">Manual entry form</span>
                </div>
                <div style="padding: 1rem; background-color: rgba(0,0,0,0.3); border-radius: 5px;">
                    <strong style="color: #FFD700; font-size: clamp(0.9rem, 2vw, 1rem);">💾 Load Combat</strong><br/>
                    <span style="color: #f8f5f0; font-size: clamp(0.8rem, 1.5vw, 0.9rem);">Import saved encounter</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Show reference
    render_conditions_reference()
else:
    # Combat Summary Dashboard
    if st.session_state.combat_active:
        st.markdown("### 📊 Combat Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total = len(st.session_state.combatants)
        alive = sum(1 for c in st.session_state.combatants if c['current_hp'] > 0)
        unconscious = sum(1 for c in st.session_state.combatants if c['current_hp'] == 0)
        conditioned = sum(1 for c in st.session_state.combatants if c['conditions'])
        exhausted = sum(1 for c in st.session_state.combatants if c['exhaustion'] > 0)
        
        with col1:
            st.metric("Total", total)
        with col2:
            st.metric("Alive", alive, delta=None, delta_color="normal")
        with col3:
            st.metric("Down", unconscious, delta=None, delta_color="inverse")
        with col4:
            st.metric("Conditions", conditioned)
        with col5:
            st.metric("Exhausted", exhausted)
        
        st.divider()
    
    # Conditions reference at top
    render_conditions_reference()
    
    # View mode toggle
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Detailed", use_container_width=True, type="primary" if st.session_state.view_mode == 'detailed' else "secondary"):
            st.session_state.view_mode = 'detailed'
            st.rerun()
    with col2:
        if st.button("📊 Compact", use_container_width=True, type="primary" if st.session_state.view_mode == 'compact' else "secondary"):
            st.session_state.view_mode = 'compact'
            st.rerun()
    with col3:
        if st.button("📉 Dense", use_container_width=True, type="primary" if st.session_state.view_mode == 'dense' else "secondary"):
            st.session_state.view_mode = 'dense'
            st.rerun()
    
    st.divider()
    
    # Display all combatants (single column for all modes)
    for idx, combatant in enumerate(st.session_state.combatants):
        is_current_turn = st.session_state.combat_active and idx == st.session_state.current_turn_index
        
        # Show death save prompt if it's a player's turn and they're at 0 HP
        if is_current_turn and combatant.get('combatant_type') == 'player' and combatant['current_hp'] == 0:
            render_death_save_prompt(combatant, idx)
        
        render_combatant_card(combatant, idx, is_current_turn, st.session_state.view_mode)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("💡 **Tip:** Use Undo/Redo buttons to fix mistakes")

with col2:
    st.caption("📖 **Quick Ref:** Check the reference guide for condition effects")

with col3:
    st.caption("💾 **Remember:** Export your combat to save progress")

# Auto-save player roster and monster library
auto_save_player_roster()
auto_save_monster_library()