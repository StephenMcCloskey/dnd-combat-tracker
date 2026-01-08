# src/components/player_character_form.py
"""Player character management forms."""

import streamlit as st
import hashlib
import random
from src.utils.combat import add_player_combatant
from src.utils.import_export import export_player_roster_data, import_player_roster_data


def initialize_player_roster():
    """Initialize player character roster in session state."""
    if 'player_roster' not in st.session_state:
        st.session_state.player_roster = {}


def save_player_to_roster(player_data: dict):
    """Save a player character to the roster."""
    player_id = hashlib.md5(player_data['name'].encode()).hexdigest()
    st.session_state.player_roster[player_id] = player_data


def render_player_roster():
    """Render the saved player characters."""
    
    if not st.session_state.player_roster:
        st.info("No saved player characters yet. Add players using the form above.")
        return
    
    st.markdown(f"**👥 {len(st.session_state.player_roster)} Player Character(s)**")
    
    for player_id, player in st.session_state.player_roster.items():
        with st.expander(f"👤 {player['name']} - {player['class_name']} {player['level']}"):
            # Compact stats display
            st.caption(
                f"**HP:** {player['max_hp']} · **AC:** {player['ac']} · "
                f"**Init:** +{player['initiative_bonus']} · **Speed:** {player.get('speed', 30)}"
            )
            
            # Show notes if present
            if player.get('notes'):
                with st.container(height=100):
                    st.text(player['notes'])
            
            # Quick add to combat
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    f"➕ Add to Combat",
                    key=f"add_player_{player_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    init_roll = random.randint(1, 20) + player['initiative_bonus']
                    
                    add_player_combatant(
                        name=player['name'],
                        initiative=init_roll,
                        dex_modifier=player['dex_modifier'],
                        max_hp=player['max_hp'],
                        ac=player['ac'],
                        speed=player.get('speed', 30),
                        class_name=player['class_name'],
                        level=player['level'],
                        proficiency_bonus=player['proficiency_bonus'],
                        has_alert=player.get('has_alert', False),
                        notes=player.get('notes', '')
                    )
                    
                    st.success(f"Added {player['name']} to combat!")
                    st.rerun()
            
            with col2:
                if st.button(
                    "🗑️ Remove",
                    key=f"remove_player_{player_id}",
                    use_container_width=True
                ):
                    del st.session_state.player_roster[player_id]
                    st.success("Player removed from roster")
                    st.rerun()


def parse_character_text(text: str) -> dict:
    """Parse character data from text format."""
    import re
    
    data = {
        'name': '',
        'class_name': '',
        'level': 1,
        'proficiency_bonus': 2,
        'max_hp': 10,
        'ac': 10,
        'speed': 30,
        'dex_modifier': 0,
        'initiative_bonus': 0,
        'has_alert': False,
        'notes': ''
    }
    
    lines = text.strip().split('\n')
    notes_lines = []
    in_notes = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.lower().startswith('notes:'):
            in_notes = True
            after_colon = line.split(':', 1)[1].strip()
            if after_colon:
                notes_lines.append(after_colon)
            continue
        
        if in_notes:
            notes_lines.append(line)
            continue
        
        if line.lower().startswith('name:'):
            data['name'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('class:'):
            data['class_name'] = line.split(':', 1)[1].strip()
        elif line.lower().startswith('level:'):
            match = re.search(r'\d+', line)
            if match:
                data['level'] = int(match.group())
        elif line.lower().startswith('proficiency:'):
            match = re.search(r'[+-]?\d+', line)
            if match:
                data['proficiency_bonus'] = int(match.group().replace('+', ''))
        elif line.lower().startswith('max hp:') or line.lower().startswith('hp:'):
            match = re.search(r'\d+', line)
            if match:
                data['max_hp'] = int(match.group())
        elif line.lower().startswith('ac:'):
            match = re.search(r'\d+', line)
            if match:
                data['ac'] = int(match.group())
        elif line.lower().startswith('speed:'):
            match = re.search(r'\d+', line)
            if match:
                data['speed'] = int(match.group())
        elif line.lower().startswith('dex modifier:') or line.lower().startswith('dex mod:'):
            match = re.search(r'[+-]?\d+', line)
            if match:
                data['dex_modifier'] = int(match.group().replace('+', ''))
        elif line.lower().startswith('initiative:'):
            match = re.search(r'[+-]?\d+', line)
            if match:
                data['initiative_bonus'] = int(match.group().replace('+', ''))
        elif '☑' in line and 'alert' in line.lower():
            data['has_alert'] = True
        elif line.lower() == 'alert feat' or 'alert feat' in line.lower():
            data['has_alert'] = True
    
    data['notes'] = '\n'.join(notes_lines)
    
    if data['has_alert']:
        expected_init = data['dex_modifier'] + data['proficiency_bonus']
        if data['initiative_bonus'] == 0:
            data['initiative_bonus'] = expected_init
    else:
        if data['initiative_bonus'] == 0:
            data['initiative_bonus'] = data['dex_modifier']
    
    return data


def render_player_character_form():
    """Render the form to add/manage player characters."""
    
    initialize_player_roster()
    
    st.markdown("#### 👥 Player Characters")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Player", "📋 Import Text", "👥 Player Roster"])
    
    with tab1:
        _render_add_player_form()
    
    with tab2:
        _render_import_text_form()
    
    with tab3:
        _render_roster_management()


def _render_add_player_form():
    """Render the add player form."""
    
    st.markdown("##### Add Player Character")
    
    with st.form("add_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Character Name*", placeholder="e.g., Aragorn")
            class_name = st.text_input("Class*", placeholder="e.g., Ranger")
        
        with col2:
            level = st.number_input("Level*", min_value=1, max_value=20, value=1)
            proficiency_bonus = st.number_input("Proficiency Bonus*", min_value=2, max_value=6, value=2)
        
        st.markdown("---")
        st.markdown("##### Combat Stats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_hp = st.number_input("Max HP*", min_value=1, value=10)
            ac = st.number_input("AC*", min_value=1, max_value=30, value=10)
            speed = st.number_input("Speed", min_value=0, max_value=120, value=30, step=5)
        
        with col2:
            dex_modifier = st.number_input("DEX Modifier*", min_value=-5, max_value=10, value=0)
            
            st.markdown("**Initiative:**")
            has_alert = st.checkbox("Alert Feat", value=False, help="Adds proficiency to initiative")
            
            if has_alert:
                initiative_bonus = dex_modifier + proficiency_bonus
                st.caption(f"Initiative: +{initiative_bonus} (DEX + Prof)")
            else:
                initiative_bonus = dex_modifier
                st.caption(f"Initiative: +{initiative_bonus} (DEX)")
        
        st.markdown("---")
        
        notes = st.text_area(
            "Notes (Features, Attacks, etc.)",
            placeholder="Rage (3/day), Great Weapon Master...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            add_to_roster = st.form_submit_button("💾 Save to Roster", use_container_width=True, type="primary")
        
        with col2:
            add_to_combat = st.form_submit_button("➕ Add to Combat Now", use_container_width=True)
        
        if add_to_roster or add_to_combat:
            if not name.strip():
                st.error("Please enter a character name")
            elif not class_name.strip():
                st.error("Please enter a class")
            else:
                player_data = {
                    'name': name.strip(),
                    'class_name': class_name.strip(),
                    'level': level,
                    'proficiency_bonus': proficiency_bonus,
                    'max_hp': max_hp,
                    'ac': ac,
                    'speed': speed,
                    'dex_modifier': dex_modifier,
                    'initiative_bonus': initiative_bonus,
                    'has_alert': has_alert,
                    'notes': notes.strip()
                }
                
                if add_to_roster:
                    save_player_to_roster(player_data)
                    st.success(f"✓ {name} saved to roster!")
                    st.rerun()
                
                if add_to_combat:
                    init_roll = random.randint(1, 20) + initiative_bonus
                    
                    add_player_combatant(
                        name=name.strip(),
                        initiative=init_roll,
                        dex_modifier=dex_modifier,
                        max_hp=max_hp,
                        ac=ac,
                        speed=speed,
                        class_name=class_name.strip(),
                        level=level,
                        proficiency_bonus=proficiency_bonus,
                        has_alert=has_alert,
                        notes=notes.strip()
                    )
                    
                    st.success(f"✓ {name} added to combat!")
                    st.rerun()


def _render_import_text_form():
    """Render the text import form."""
    
    st.markdown("##### Import from Text")
    st.caption("Paste character data in a simple format")
    
    with st.expander("📖 See Example Format"):
        st.code("""Name: Aragorn
Class: Ranger
Level: 8
Proficiency: +3
Max HP: 65
AC: 16
Speed: 30
DEX Modifier: +3
Alert Feat
Initiative: +6
Notes:
Favored Enemy: Orcs
Natural Explorer: Forests
Colossus Slayer (1d8)""", language="text")
    
    character_text = st.text_area(
        "Paste Character Data",
        height=200,
        placeholder="Name: Character Name\nClass: Fighter\n..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Preview", use_container_width=True):
            if character_text.strip():
                st.session_state['preview_character'] = parse_character_text(character_text)
            else:
                st.warning("Please paste character data first")
    
    with col2:
        if st.button("💾 Import to Roster", use_container_width=True, type="primary"):
            if character_text.strip():
                parsed = parse_character_text(character_text)
                
                if not parsed['name']:
                    st.error("Could not find character name")
                elif not parsed['class_name']:
                    st.error("Could not find class")
                else:
                    save_player_to_roster(parsed)
                    st.success(f"✓ {parsed['name']} imported!")
                    st.session_state.pop('preview_character', None)
                    st.rerun()
            else:
                st.warning("Please paste character data first")
    
    # Preview display
    if 'preview_character' in st.session_state:
        st.markdown("---")
        st.markdown("##### 👁️ Preview")
        
        preview = st.session_state['preview_character']
        
        st.caption(
            f"**Name:** {preview['name'] or '(missing)'} · "
            f"**Class:** {preview['class_name'] or '(missing)'} {preview['level']} · "
            f"**HP:** {preview['max_hp']} · **AC:** {preview['ac']} · "
            f"**Init:** +{preview['initiative_bonus']}"
        )
        
        if preview['has_alert']:
            st.caption("✓ Alert Feat")
        
        if preview['notes']:
            with st.container(height=100):
                st.text(preview['notes'])


def _render_roster_management():
    """Render roster management section."""
    
    st.markdown("##### Roster Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.player_roster:
            export_data = export_player_roster_data()
            st.download_button(
                label="📥 Export Roster",
                data=export_data,
                file_name=f"dnd_players_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        uploaded_file = st.file_uploader(
            "📤 Import Roster",
            type=['json'],
            key="player_roster_upload",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.read().decode('utf-8')
                success, message = import_player_roster_data(json_str)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    st.markdown("---")
    render_player_roster()


def get_player_roster_filename() -> str:
    """Generate a filename for player roster export."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"dnd_players_{timestamp}.json"