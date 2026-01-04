# src/utils/import_export.py (COMPLETE UPDATED VERSION)
import json
import streamlit as st
from datetime import datetime

def export_combat_state():
    """Export current combat state to JSON"""
    state = {
        'combatants': st.session_state.combatants,
        'current_turn_index': st.session_state.current_turn_index,
        'round_number': st.session_state.round_number,
        'combat_active': st.session_state.combat_active,
        'combat_log': st.session_state.combat_log,
        'export_timestamp': datetime.now().isoformat(),
        'version': '3.0'
    }
    return json.dumps(state, indent=2)

def import_combat_state(json_str):
    """Import combat state from JSON"""
    try:
        state = json.loads(json_str)
        
        # Validate required fields
        required_fields = ['combatants', 'current_turn_index', 'round_number', 'combat_active']
        if not all(field in state for field in required_fields):
            return False, "Invalid combat state file: missing required fields"
        
        # Load state
        st.session_state.combatants = state['combatants']
        st.session_state.current_turn_index = state['current_turn_index']
        st.session_state.round_number = state['round_number']
        st.session_state.combat_active = state['combat_active']
        st.session_state.combat_log = state.get('combat_log', [])
        
        return True, "Combat state loaded successfully!"
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error loading combat state: {str(e)}"

def get_export_filename():
    """Generate a filename for export"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"dnd_combat_{timestamp}.json"

def export_monster_library():
    """Export saved monsters to JSON"""
    if 'saved_monsters' not in st.session_state:
        st.session_state.saved_monsters = {}
    
    library = {
        'monsters': st.session_state.saved_monsters,
        'export_timestamp': datetime.now().isoformat(),
        'version': '1.0'
    }
    return json.dumps(library, indent=2)

def import_monster_library(json_str):
    """Import monster library from JSON"""
    try:
        library = json.loads(json_str)
        
        if 'monsters' not in library:
            return False, "Invalid monster library file"
        
        # Initialize if doesn't exist
        if 'saved_monsters' not in st.session_state:
            st.session_state.saved_monsters = {}
        
        # Merge imported monsters (don't overwrite existing)
        imported_count = 0
        for monster_id, monster_data in library['monsters'].items():
            if monster_id not in st.session_state.saved_monsters:
                st.session_state.saved_monsters[monster_id] = monster_data
                imported_count += 1
        
        return True, f"Imported {imported_count} monster(s)"
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error importing library: {str(e)}"

def get_monster_library_filename():
    """Generate a filename for monster library export"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"dnd_monsters_{timestamp}.json"

def export_player_roster_data():
    """Export player roster to JSON string"""
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"dnd_players_{timestamp}.json"