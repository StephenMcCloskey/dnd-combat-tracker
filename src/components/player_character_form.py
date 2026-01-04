import streamlit as st
import hashlib
import random

def initialize_player_roster():
    """Initialize player character roster in session state"""
    if 'player_roster' not in st.session_state:
        st.session_state.player_roster = {}

def save_player_to_roster(player_data):
    """Save a player character to the roster"""
    # Create a unique ID for the player (based on name)
    player_id = hashlib.md5(player_data['name'].encode()).hexdigest()
    
    st.session_state.player_roster[player_id] = player_data

def export_player_roster_data():
    """Export player roster to JSON string"""
    import json
    from datetime import datetime
    
    if 'player_roster' not in st.session_state:
        st.session_state.player_roster = {}
    
    roster = {
        'players': st.session_state.player_roster,
        'export_timestamp': datetime.now().isoformat(),
        'version': '1.0'
    }
    return json.dumps(roster, indent=2)

def import_player_roster_data(json_str):
    """Import player roster from JSON string"""
    import json
    
    try:
        roster = json.loads(json_str)
        
        if 'players' not in roster:
            return False, "Invalid player roster file"
        
        # Initialize if doesn't exist
        if 'player_roster' not in st.session_state:
            st.session_state.player_roster = {}
        
        # Merge imported players (don't overwrite existing)
        imported_count = 0
        for player_id, player_data in roster['players'].items():
            if player_id not in st.session_state.player_roster:
                st.session_state.player_roster[player_id] = player_data
                imported_count += 1
        
        return True, f"Imported {imported_count} player(s)"
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error importing roster: {str(e)}"

def get_player_roster_filename():
    """Generate a filename for player roster export"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"dnd_players_{timestamp}.json"

def render_player_roster():
    """Render the saved player characters"""
    from src.utils.combat import add_player_combatant
    
    if not st.session_state.player_roster:
        st.info("No saved player characters yet. Add players using the form above.")
        return
    
    st.markdown(f"**👥 {len(st.session_state.player_roster)} Player Character(s)**")
    
    for player_id, player in st.session_state.player_roster.items():
        with st.expander(f"👤 {player['name']} - {player['class_name']} {player['level']}"):
            # Display stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("HP", player['max_hp'])
            with col2:
                st.metric("AC", player['ac'])
            with col3:
                st.metric("Initiative", f"+{player['initiative_bonus']}")
            with col4:
                st.metric("Speed", player.get('speed', 30))
            
            # Show notes if present
            if player.get('notes'):
                st.text_area("Notes", value=player['notes'], key=f"player_notes_view_{player_id}", height=100, disabled=True)
            
            # Quick add to combat
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    f"➕ Add to Combat",
                    key=f"add_player_{player_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    # Roll initiative
                    import random
                    init_roll = random.randint(1, 20) + player['initiative_bonus']
                    
                    # Add to combat using new function
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

def parse_character_text(text):
    """Parse character data from text format"""
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
        
        # Check if we've hit the notes section
        if line.lower().startswith('notes:'):
            in_notes = True
            # Check if there's content after "Notes:"
            after_colon = line.split(':', 1)[1].strip()
            if after_colon:
                notes_lines.append(after_colon)
            continue
        
        if in_notes:
            notes_lines.append(line)
            continue
        
        # Parse specific fields
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
    
    # Join notes
    data['notes'] = '\n'.join(notes_lines)
    
    # Validate initiative calculation
    if data['has_alert']:
        expected_init = data['dex_modifier'] + data['proficiency_bonus']
        if data['initiative_bonus'] == 0:
            data['initiative_bonus'] = expected_init
    else:
        if data['initiative_bonus'] == 0:
            data['initiative_bonus'] = data['dex_modifier']
    
    return data

def render_player_character_form():
    """Render the form to add/manage player characters"""
    from src.utils.combat import add_combatant, log_event
    
    # Initialize roster
    initialize_player_roster()
    
    st.subheader("👥 Player Characters")
    
    # Tabs for add and roster
    tab1, tab2, tab3 = st.tabs(["➕ Add Player", "📋 Import Text", "👥 Player Roster"])
    
    with tab1:
        st.markdown("### Add Player Character")
        
        with st.form("add_player_form", clear_on_submit=True):
            # Basic info
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Character Name*", placeholder="e.g., May")
                class_name = st.text_input("Class*", placeholder="e.g., Barbarian")
            
            with col2:
                level = st.number_input("Level*", min_value=1, max_value=20, value=1, step=1)
                proficiency_bonus = st.number_input(
                    "Proficiency Bonus*",
                    min_value=2,
                    max_value=6,
                    value=2,
                    step=1,
                    help="Typically +2 at level 1-4, +3 at 5-8, +4 at 9-12, +5 at 13-16, +6 at 17-20"
                )
            
            st.markdown("---")
            st.markdown("#### Combat Stats")
            
            col1, col2 = st.columns(2)
            
            with col1:
                max_hp = st.number_input("Max HP*", min_value=1, value=10, step=1)
                ac = st.number_input("Armor Class (AC)*", min_value=1, max_value=30, value=10, step=1)
                speed = st.number_input("Speed", min_value=0, max_value=120, value=30, step=5)
            
            with col2:
                dex_modifier = st.number_input(
                    "DEX Modifier*",
                    min_value=-5,
                    max_value=10,
                    value=0,
                    step=1,
                    help="Used for initiative calculation"
                )
                
                # Initiative calculation
                st.markdown("**Initiative Bonus:**")
                has_alert = st.checkbox(
                    "Alert Feat (adds proficiency to initiative)",
                    value=False,
                    help="Alert feat grants initiative proficiency"
                )
                
                if has_alert:
                    initiative_bonus = dex_modifier + proficiency_bonus
                    st.info(f"Initiative: +{initiative_bonus} (DEX {dex_modifier:+d} + Prof {proficiency_bonus:+d})")
                else:
                    initiative_bonus = dex_modifier
                    st.info(f"Initiative: +{initiative_bonus} (DEX {dex_modifier:+d})")
            
            st.markdown("---")
            st.markdown("#### Additional Info")
            
            notes = st.text_area(
                "Notes (Class Features, Feats, Attacks, etc.)",
                placeholder="e.g., Alert feat, Sentinel, Rage (3/day)\n\nAttacks:\nClaws +6 (1d6+4 slashing)\nBite +6 (1d8 piercing)\nTail +6 (1d8+1d6)",
                height=150,
                help="Include important features, attacks, and abilities"
            )
            
            # Submit buttons
            col1, col2 = st.columns(2)
            
            with col1:
                add_to_roster = st.form_submit_button(
                    "💾 Save to Roster",
                    use_container_width=True,
                    type="primary"
                )
            
            with col2:
                add_to_combat = st.form_submit_button(
                    "➕ Add to Combat Now",
                    use_container_width=True
                )
            
            if add_to_roster or add_to_combat:
                if not name.strip():
                    st.error("Please enter a character name")
                elif not class_name.strip():
                    st.error("Please enter a class")
                else:
                    # Create player data
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
                        # Save to roster
                        save_player_to_roster(player_data)
                        st.success(f"✓ {name} saved to player roster!")
                        st.rerun()
                    
                    if add_to_combat:
                        from src.utils.combat import add_player_combatant
                        import random
                        
                        # Roll initiative and add directly
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
    
    with tab2:
        st.markdown("### Import from Text")
        st.caption("Paste character data in a simple format and import directly to roster")
        
        # Show example format
        with st.expander("📖 See Example Format"):
            st.code("""Name: May
Class: Barbarian
Level: 4
Proficiency: +2
Max HP: 46
AC: 17
Speed: 30
DEX Modifier: +2
☑ Alert Feat
Initiative: +4
Notes:
Alert feat, Sentinel, Rage (3/day)
Attacks:
Claws +6 (1d6+4 slashing)
Bite +6 (1d8 piercing)
Tail +6 (1d8+1d6)""", language="text")
            
            st.info("💡 **Tips:**\n- Field names are case-insensitive\n- Use ☑ or mention 'Alert Feat' for the feat\n- Everything after 'Notes:' is treated as notes\n- Missing fields will use defaults")
        
        # Text input area
        character_text = st.text_area(
            "Paste Character Data",
            height=300,
            placeholder="Name: Character Name\nClass: Class Name\nLevel: 1\n...",
            help="Paste character information in the format shown in the example"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Preview", use_container_width=True, type="secondary"):
                if character_text.strip():
                    st.session_state['preview_character'] = parse_character_text(character_text)
                else:
                    st.warning("Please paste character data first")
        
        with col2:
            if st.button("💾 Import to Roster", use_container_width=True, type="primary"):
                if character_text.strip():
                    parsed = parse_character_text(character_text)
                    
                    if not parsed['name']:
                        st.error("Could not find character name. Please include 'Name:' field")
                    elif not parsed['class_name']:
                        st.error("Could not find class. Please include 'Class:' field")
                    else:
                        save_player_to_roster(parsed)
                        st.success(f"✓ {parsed['name']} imported to roster!")
                        st.session_state.pop('preview_character', None)
                        st.rerun()
                else:
                    st.warning("Please paste character data first")
        
        # Show preview if available
        if 'preview_character' in st.session_state:
            st.markdown("---")
            st.markdown("### 👁️ Preview")
            
            preview = st.session_state['preview_character']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Name:** {preview['name'] or '(missing)'}")
                st.markdown(f"**Class:** {preview['class_name'] or '(missing)'} {preview['level']}")
                st.markdown(f"**Proficiency:** +{preview['proficiency_bonus']}")
                st.markdown(f"**Max HP:** {preview['max_hp']}")
            
            with col2:
                st.markdown(f"**AC:** {preview['ac']}")
                st.markdown(f"**Speed:** {preview['speed']}")
                st.markdown(f"**DEX Modifier:** {preview['dex_modifier']:+d}")
                st.markdown(f"**Initiative:** +{preview['initiative_bonus']}")
                if preview['has_alert']:
                    st.markdown("✓ **Alert Feat**")
            
            if preview['notes']:
                st.markdown("**Notes:**")
                st.text_area("", value=preview['notes'], height=150, disabled=True, key="preview_notes", label_visibility="collapsed")
            
            if not preview['name'] or not preview['class_name']:
                st.warning("⚠️ Missing required fields. Please add Name and Class before importing.")
    
    with tab3:
        # Roster management
        st.markdown("### Player Roster Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export roster
            if st.session_state.player_roster:
                export_data = export_player_roster_data()
                st.download_button(
                    label="📥 Export Roster",
                    data=export_data,
                    file_name=get_player_roster_filename(),
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            # Import roster
            uploaded_file = st.file_uploader(
                "📤 Import Roster",
                type=['json'],
                key="player_roster_upload"
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
        
        # Display roster
        render_player_roster()