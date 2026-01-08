# src/config.py
"""Application configuration settings."""

# =============================================================================
# Command System
# =============================================================================
MAX_COMMAND_HISTORY = 50  # Maximum undo/redo stack size

# =============================================================================
# UI Defaults
# =============================================================================
DEFAULT_VIEW_MODE = 'compact'  # 'detailed', 'compact', or 'dense'
DEFAULT_SPEED = 30  # Default movement speed in feet

# Combat Log
COMBAT_LOG_DEFAULT_HEIGHT = 300
COMBAT_LOG_MIN_HEIGHT = 100
COMBAT_LOG_MAX_HEIGHT = 600

# =============================================================================
# API Settings
# =============================================================================
OPEN5E_BASE_URL = "https://api.open5e.com"
API_TIMEOUT = 5  # Seconds
MAX_SEARCH_RESULTS = 10  # Top N results to display

# =============================================================================
# Combat Limits
# =============================================================================
MAX_BULK_ADD = 20  # Maximum monsters to add at once
MAX_INITIATIVE = 30
MIN_INITIATIVE = 1
MAX_AC = 30
MIN_AC = 1
MAX_LEVEL = 20
MIN_LEVEL = 1
MAX_EXHAUSTION = 6
MAX_HP = 9999
MAX_DAMAGE = 9999
MAX_HEALING = 9999

# =============================================================================
# Data Paths
# =============================================================================
DATA_FOLDER = "data"
COMBATS_FOLDER = "combats"
PLAYERS_FOLDER = "players"
MONSTERS_FOLDER = "monsters"
AUTO_ROSTER_FILENAME = "auto_roster.json"
AUTO_LIBRARY_FILENAME = "auto_library.json"

# =============================================================================
# Export Settings
# =============================================================================
EXPORT_VERSION = "3.0"
ROSTER_VERSION = "1.0"
LIBRARY_VERSION = "1.0"

# =============================================================================
# Page Configuration
# =============================================================================
PAGE_TITLE = "D&D 5.5e Combat Tracker"
PAGE_ICON = "⚔️"
PAGE_LAYOUT = "wide"