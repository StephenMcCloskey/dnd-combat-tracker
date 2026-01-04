# src/utils/data_manager.py
from pathlib import Path
import json
from datetime import datetime
import streamlit as st

# Define data directory path (relative to project root)
DATA_DIR = Path(__file__).parent.parent.parent / "data"
COMBAT_DIR = DATA_DIR / "combats"
PLAYER_DIR = DATA_DIR / "players"
MONSTER_DIR = DATA_DIR / "monsters"

def initialize_data_directories():
    """Create data directories if they don't exist"""
    DATA_DIR.mkdir(exist_ok=True)
    COMBAT_DIR.mkdir(exist_ok=True)
    PLAYER_DIR.mkdir(exist_ok=True)
    MONSTER_DIR.mkdir(exist_ok=True)

def get_combat_files():
    """Get list of saved combat files"""
    initialize_data_directories()
    files = list(COMBAT_DIR.glob("*.json"))
    # Sort by modification time, newest first
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files

def get_player_roster_files():
    """Get list of saved player roster files"""
    initialize_data_directories()
    files = list(PLAYER_DIR.glob("*.json"))
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files

def get_monster_library_files():
    """Get list of saved monster library files"""
    initialize_data_directories()
    files = list(MONSTER_DIR.glob("*.json"))
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files

def save_combat_to_file(combat_data: dict, filename: str = None) -> tuple[bool, str, Path]:
    """Save combat data to a file in the data directory
    
    Returns:
        tuple: (success, message, filepath)
    """
    try:
        initialize_data_directories()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"combat_{timestamp}.json"
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = COMBAT_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(combat_data, f, indent=2)
        
        return True, f"Combat saved to {filepath.name}", filepath
    
    except Exception as e:
        return False, f"Error saving combat: {str(e)}", None

def load_combat_from_file(filepath: Path) -> tuple[bool, str, dict]:
    """Load combat data from a file
    
    Returns:
        tuple: (success, message, data)
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return True, f"Combat loaded from {filepath.name}", data
    
    except Exception as e:
        return False, f"Error loading combat: {str(e)}", None

def delete_combat_file(filepath: Path) -> tuple[bool, str]:
    """Delete a combat file
    
    Returns:
        tuple: (success, message)
    """
    try:
        filepath.unlink()
        return True, f"Deleted {filepath.name}"
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"

def save_player_roster_to_file(roster_data: dict, filename: str = None) -> tuple[bool, str, Path]:
    """Save player roster to a file in the data directory
    
    Returns:
        tuple: (success, message, filepath)
    """
    try:
        initialize_data_directories()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"players_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = PLAYER_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(roster_data, f, indent=2)
        
        return True, f"Player roster saved to {filepath.name}", filepath
    
    except Exception as e:
        return False, f"Error saving roster: {str(e)}", None

def load_player_roster_from_file(filepath: Path) -> tuple[bool, str, dict]:
    """Load player roster from a file
    
    Returns:
        tuple: (success, message, data)
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return True, f"Player roster loaded from {filepath.name}", data
    
    except Exception as e:
        return False, f"Error loading roster: {str(e)}", None

def delete_player_roster_file(filepath: Path) -> tuple[bool, str]:
    """Delete a player roster file
    
    Returns:
        tuple: (success, message)
    """
    try:
        filepath.unlink()
        return True, f"Deleted {filepath.name}"
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"

def save_monster_library_to_file(library_data: dict, filename: str = None) -> tuple[bool, str, Path]:
    """Save monster library to a file in the data directory
    
    Returns:
        tuple: (success, message, filepath)
    """
    try:
        initialize_data_directories()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monsters_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = MONSTER_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(library_data, f, indent=2)
        
        return True, f"Monster library saved to {filepath.name}", filepath
    
    except Exception as e:
        return False, f"Error saving library: {str(e)}", None

def load_monster_library_from_file(filepath: Path) -> tuple[bool, str, dict]:
    """Load monster library from a file
    
    Returns:
        tuple: (success, message, data)
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return True, f"Monster library loaded from {filepath.name}", data
    
    except Exception as e:
        return False, f"Error loading library: {str(e)}", None

def delete_monster_library_file(filepath: Path) -> tuple[bool, str]:
    """Delete a monster library file
    
    Returns:
        tuple: (success, message)
    """
    try:
        filepath.unlink()
        return True, f"Deleted {filepath.name}"
    except Exception as e:
        return False, f"Error deleting file: {str(e)}"

# Auto-save/load functions
AUTO_SAVE_ROSTER_FILE = PLAYER_DIR / "auto_roster.json"
AUTO_SAVE_LIBRARY_FILE = MONSTER_DIR / "auto_library.json"

def auto_save_player_roster():
    """Auto-save the current player roster"""
    if 'player_roster' not in st.session_state or not st.session_state.player_roster:
        return
    
    try:
        initialize_data_directories()
        roster_data = {
            'players': st.session_state.player_roster,
            'export_timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        with open(AUTO_SAVE_ROSTER_FILE, 'w') as f:
            json.dump(roster_data, f, indent=2)
    except Exception:
        pass  # Silently fail auto-save

def auto_load_player_roster():
    """Auto-load the player roster on startup"""
    if AUTO_SAVE_ROSTER_FILE.exists():
        try:
            with open(AUTO_SAVE_ROSTER_FILE, 'r') as f:
                data = json.load(f)
            
            if 'players' in data:
                if 'player_roster' not in st.session_state:
                    st.session_state.player_roster = {}
                st.session_state.player_roster = data['players']
                return True
        except Exception:
            pass  # Silently fail auto-load
    return False

def auto_save_monster_library():
    """Auto-save the current monster library"""
    if 'saved_monsters' not in st.session_state or not st.session_state.saved_monsters:
        return
    
    try:
        initialize_data_directories()
        library_data = {
            'monsters': st.session_state.saved_monsters,
            'export_timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        with open(AUTO_SAVE_LIBRARY_FILE, 'w') as f:
            json.dump(library_data, f, indent=2)
    except Exception:
        pass  # Silently fail auto-save

def auto_load_monster_library():
    """Auto-load the monster library on startup"""
    if AUTO_SAVE_LIBRARY_FILE.exists():
        try:
            with open(AUTO_SAVE_LIBRARY_FILE, 'r') as f:
                data = json.load(f)
            
            if 'monsters' in data:
                if 'saved_monsters' not in st.session_state:
                    st.session_state.saved_monsters = {}
                st.session_state.saved_monsters = data['monsters']
                return True
        except Exception:
            pass  # Silently fail auto-load
    return False

def format_file_time(filepath: Path) -> str:
    """Format file modification time for display"""
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    now = datetime.now()
    
    # If today, show time
    if mtime.date() == now.date():
        return f"Today at {mtime.strftime('%I:%M %p')}"
    
    # If yesterday
    elif (now - mtime).days == 1:
        return f"Yesterday at {mtime.strftime('%I:%M %p')}"
    
    # If within a week
    elif (now - mtime).days < 7:
        return mtime.strftime("%A at %I:%M %p")
    
    # Otherwise full date
    else:
        return mtime.strftime("%b %d, %Y at %I:%M %p")