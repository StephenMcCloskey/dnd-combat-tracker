# D&D 5.5e Combat Tracker

A local Streamlit application for tracking combat encounters in Dungeons & Dragons 5.5e (2024 rules) with full undo/redo functionality and command history.

## Project Overview

This is a comprehensive combat tracker designed for D&D 5.5e that helps Dungeon Masters manage initiative order, hit points, conditions, death saving throws, and all combat-related mechanics in a user-friendly interface. Features integration with the Open5e API for quick monster lookup, personal monster library system, player character management, and a complete undo/redo system with command history.

## Features

### Core Combat Management
- **Initiative Tracking**: Automatic sorting by initiative and DEX modifier
- **Turn Management**: Header-based navigation with Previous/Next buttons always visible
- **Smart Turn Skipping**: Monsters at 0 HP are automatically skipped; players at 0 HP get death save prompts
- **Undo/Redo System**: Full command history with 50-command buffer
  - Undo button (↩) in header with Ctrl+Z shortcut
  - Redo button (↪) in header with Ctrl+Shift+Z shortcut
  - Command history viewer shows all actions with technical details
  - All actions are undoable: damage, healing, conditions, turn changes, adding/removing combatants
- **Round Counter**: Tracks combat rounds with prominent display in header
- **HP Management**: Damage, healing, and temporary HP tracking (all undoable)
- **Death Saving Throws**: Full tracking with success/failure counters, stabilization, and prominent prompts
- **Combat Confirmation**: Safety check before ending combat to prevent accidental data loss
- **Command Log**: Separate human-readable log and technical command history

### Combatant Types
- **Player Characters**: Full support with class, level, proficiency, Alert feat
  - TypedDict model: `PlayerCombatant`
  - Fields: class_name, level, proficiency_bonus, has_alert
  - Distinguished with 👥 icon
- **Monsters/NPCs**: Support for CR, size, type
  - TypedDict model: `MonsterCombatant`
  - Fields: cr, monster_type, size
  - Distinguished with 👹 icon
- **Unified Base**: All combatants share core fields (HP, AC, speed, conditions, etc.)

### Player Character System
- **Player Character Form**: Dedicated form for adding PCs with detailed stats
  - Name, Class, Level tracking
  - Proficiency bonus input with level-based suggestions
  - Max HP, AC, Speed, DEX modifier
  - Alert feat checkbox (adds proficiency to initiative)
  - Automatic initiative calculation
  - Notes field for class features, feats, attacks, abilities
- **Text Import**: Paste character data in simple text format
  - Smart parsing of character fields
  - Preview before importing
  - Supports flexible formatting
  - Auto-detects Alert feat
- **Player Roster**: 
  - Save players for quick re-use across sessions
  - Quick-add to combat with auto-rolled initiative
  - Visual distinction from monsters (👥/👤 icons)
  - Auto-saves to `data/players/auto_roster.json`
  - Manual save/load with custom names
  - Export/Import roster as JSON
  - Separate from monster library
- **Two Add Options**:
  - Save to Roster (for future use)
  - Add to Combat Now (immediate with rolled initiative)

### Monster Integration (Open5e API)
- **API Search**: Search 400+ SRD monsters from Open5e database
- **Smart Ranking**: Results sorted by relevance (exact match → starts with → contains)
- **Source Filtering**: 
  - 📕 SRD (Official WotC) - Default
  - 📘 Tome of Beasts (1, 2, 3)
  - 📗 Creature Codex
  - 📙 Level Up: Monstrous Menagerie & Adventurer's Guide
- **Search Cache**: Optional caching system (toggle on/off)
  - Reduces API calls
  - Case-insensitive cache keys
  - Source-aware caching
- **Monster Library**: 
  - Auto-save monsters added to combat
  - Personal collection that persists across sessions
  - Quick-add from library without API calls
  - Auto-saves to `data/monsters/auto_library.json`
  - Manual save/load with custom names
  - Export/Import library as JSON
- **Bulk Add**: Add multiple instances of same monster (e.g., 5 goblins)
- **Initiative Options**: Auto-roll or shared initiative for groups
- **HP Options**: Use average HP or roll from hit dice
- **Auto-populate**: Name, HP, AC, DEX mod, speed, CR, type, size, notes with abilities/actions

### Status Effects
- **14 Standard Conditions**: Blinded, Charmed, Deafened, Frightened, Grappled, Incapacitated, Invisible, Paralyzed, Petrified, Poisoned, Prone, Restrained, Stunned, Unconscious
- **Exhaustion System**: 6 levels with cumulative effects display
- **Visual Indicators**: Icons in combatant titles showing status at a glance
  - 💀 = 0 HP (unconscious)
  - 🩸 = Critically wounded (<25% HP)
  - ⚠️(n) = Has n conditions
  - 😫(n) = Exhaustion level n
- **All condition changes are undoable**

### Quality of Life Features
- **View Modes**: Three layout options for different needs
  - 📋 **Detailed**: Full controls and information (best for setup/management)
  - 📊 **Compact**: Horizontal stats, quick actions (default, best for active combat)
  - 📉 **Dense**: Ultra-compact with expandable details (best for large encounters 8+ combatants)
- **Responsive Design**: Adapts to sidebar open/closed state
- **Quick Actions**: 
  - Toggle Prone/Stand Up
  - Toggle Unconscious/Wake Up
  - Full Heal (restores HP and clears conditions)
  - Clear All Conditions
  - All actions are undoable
- **Death Save Prompts**: Prominent UI when player at 0 HP has their turn
  - d20 roller with natural 1/20 handling
  - Manual entry option
  - Visual success/failure tracking
- **Initiative Roller**: Built-in d20 roller with DEX modifier for manual entry
- **Combat Log**: Scrollable event history with adjustable height (100-600px)
  - Separate from command history
  - Shows human-readable action descriptions
  - Toggle to command history view (📋 button)
- **Command History**: Technical view of all commands
  - Shows last 50 commands
  - Displays current position in history
  - Shows undone commands as grayed out
  - Expandable technical details for each command
- **Combat Overview Dashboard**: Real-time statistics (total, alive, down, conditioned, exhausted)
- **Quick Reference**: Collapsible guide for all conditions and exhaustion effects
- **Notes Field**: Custom notes per combatant with full stat blocks for monsters

### Save/Load System
- **Local File Storage**: All data saved to `data/` folder in project directory
  - `data/combats/` - Combat encounters
  - `data/players/` - Player rosters
  - `data/monsters/` - Monster libraries
- **Auto-Save**: Player roster and monster library auto-save on changes
  - `auto_roster.json` - Automatically saved roster
  - `auto_library.json` - Automatically saved library
- **Auto-Load**: Auto-loads roster and library on app startup
- **Manual Save/Load**: Save with custom names, load from list, delete old saves
- **File Management**: 
  - List all saved files with timestamps
  - "Today at 2:30 PM" style time formatting
  - Load/delete buttons for each save
  - Sort by newest first
- **Download/Upload**: Still supports downloading to computer for backup/sharing
- **State Preservation**: Saves all combatants, HP, conditions, turn order, rounds, combat log

### UI/UX
- **Dark Fantasy Theme**: D&D-inspired color scheme with dark leather sidebar
- **Modular CSS**: Styles organized into separate modules (main, sidebar, header, components)
- **Responsive Layout**: Wide layout optimized for desktop use, adapts to sidebar state
- **Sticky Header**: Combat controls always visible at top
  - Undo/Redo buttons
  - Previous/Next turn navigation
  - Current turn indicator with death save warning
  - End Combat with confirmation
- **Tabbed Interface**: 
  - ⚔️ Combat - Main combat view with combatant cards
  - 👥 Players - Player character management
  - 👹 Monsters - Monster search and library
  - 📖 Reference - Conditions and exhaustion quick reference
  - 💾 Save/Load - File management
- **Three View Modes**: Detailed, Compact (default), Dense
- **Visual Feedback**: Color-coded HP bars, status icons, and hover effects
- **Empty State**: Helpful welcome screen with clear next steps
- **Overflow Handling**: Sidebar scrolls, text wraps properly, no horizontal overflow

## Technical Stack

- **Framework**: Streamlit
- **Package Manager**: uv
- **Language**: Python 3.13+
- **API**: Open5e REST API (https://api.open5e.com)
- **Dependencies**: requests (for API calls)
- **Data Format**: JSON for import/export and local storage
- **Type System**: TypedDict for combatant models
- **Architecture**: Command pattern with undo/redo stack

## Project Structure

```
dnd-combat-tracker/
├── app.py                              # Main Streamlit application entry point
├── pyproject.toml                      # Project dependencies
├── uv.lock                             # Locked dependency versions
├── CLAUDE.md                           # This documentation file
├── README.md                           # Project readme
├── .gitignore                          # Git ignore (includes data/)
├── data/                               # Local data storage (git-ignored)
│   ├── combats/                        # Saved combat encounters
│   ├── players/                        # Player rosters
│   │   └── auto_roster.json            # Auto-saved roster
│   └── monsters/                       # Monster libraries
│       └── auto_library.json           # Auto-saved library
└── src/
    ├── __init__.py
    ├── config.py                       # Application configuration settings
    ├── constants.py                    # D&D 5.5e game constants and reference data
    ├── styles/                         # CSS styling modules
    │   ├── __init__.py                 # apply_all_styles() function
    │   ├── main.py                     # Main content area styles
    │   ├── sidebar.py                  # Sidebar styles
    │   ├── header.py                   # Sticky header styles
    │   └── components.py               # Component-specific styles (cards, tabs, etc.)
    ├── layouts/                        # Page layout modules
    │   ├── __init__.py                 # Layout exports
    │   ├── sticky_header.py            # Header with title, stats, and combat controls
    │   ├── sidebar.py                  # Sidebar with combat log and tips
    │   └── main_tabs.py                # Main tabbed content area (Combat/Players/Monsters/Reference/Save)
    ├── components/                     # Reusable UI components
    │   ├── __init__.py
    │   ├── add_combatant_form.py       # Manual combatant entry form (generic monsters)
    │   ├── combat_controls.py          # Turn navigation and combat control buttons
    │   ├── combat_log.py               # Combat log display with command history toggle
    │   ├── combat_overview.py          # Combat statistics dashboard
    │   ├── combatant_card.py           # Individual combatant display (3 view modes)
    │   ├── command_history.py          # Command history viewer with position indicator
    │   ├── conditions_reference.py     # Quick reference guide for conditions/exhaustion
    │   ├── death_save_prompt.py        # Prominent death save UI for unconscious players
    │   ├── monster_search.py           # Monster search & library UI
    │   ├── player_character_form.py    # Player character management (form, import, roster)
    │   └── save_load_manager.py        # Save/load UI with local file management
    └── utils/                          # Core logic and utilities
        ├── __init__.py
        ├── models.py                   # TypedDict models (PlayerCombatant, MonsterCombatant)
        ├── command_stack.py            # Command pattern base classes
        ├── commands.py                 # Specific command implementations (all undoable actions)
        ├── command_manager.py          # Command execution and undo/redo management
        ├── combat.py                   # Core combat logic (public API wrapping commands)
        ├── data_manager.py             # Local file management (save/load/delete)
        ├── import_export.py            # JSON export/import functionality
        └── monster_api.py              # Open5e API integration with caching
```

## Architecture

### Command Pattern with Undo/Redo

The app uses a command pattern to enable full undo/redo functionality:

**Key Components:**
1. **Command Base Classes** (`command_stack.py`)
   - `Command` protocol: defines execute(), undo(), description(), technical_description()
   - `CombatCommand` base class: handles state capture/restore with deepcopy

2. **Command Implementations** (`commands.py`)
   - Each action is a command class (e.g., `ApplyDamageCommand`, `NextTurnCommand`)
   - Commands capture state before execution
   - `undo()` restores previous state
   - Both human-readable and technical descriptions

3. **Command Manager** (`command_manager.py`)
   - Maintains command stack (max 50 commands)
   - Tracks current position in stack
   - Clears stack on combat end
   - Adds descriptions to combat log

4. **Combat Functions** (`combat.py`)
   - Public API wraps commands (e.g., `apply_damage()` creates and executes `ApplyDamageCommand`)
   - All state changes go through command system
   - Legacy `log_event()` for backward compatibility

**Command Flow:**
```
User clicks "Apply 10 damage" button
    ↓
apply_damage(index=0, damage=10)
    ↓
Creates command: cmd = ApplyDamageCommand(index=0, damage=10)
    ↓
execute_command(cmd)
    ↓
Command captures state, modifies, captures again
    ↓
Adds to stack and log
```

**Undo Flow:**
```
User clicks "Undo" button
    ↓
undo_last_command()
    ↓
Gets command at current position
    ↓
cmd.undo() restores before_state
    ↓
Moves position back
```

### Layout Architecture

The app uses a modular layout system:

1. **`app.py`** - Entry point, orchestrates layout rendering
2. **`layouts/sticky_header.py`** - Always-visible header with combat controls
3. **`layouts/sidebar.py`** - Combat log and tips
4. **`layouts/main_tabs.py`** - Tabbed content area with view mode selection

### Style Architecture

CSS is modularized for maintainability:

1. **`styles/main.py`** - App background, typography, buttons, inputs
2. **`styles/sidebar.py`** - Sidebar theming and components
3. **`styles/header.py`** - Sticky header and turn indicators
4. **`styles/components.py`** - Cards, tabs, conditions, death saves

### Type System

**TypedDict Models** (`models.py`):
```python
BaseCombatant:       # Shared fields
  - name, initiative, dex_modifier
  - max_hp, current_hp, temp_hp
  - ac, speed
  - conditions, exhaustion
  - death_saves, is_stable, notes

PlayerCombatant(BaseCombatant):
  - combatant_type: 'player'
  - class_name, level
  - proficiency_bonus, has_alert

MonsterCombatant(BaseCombatant):
  - combatant_type: 'monster'
  - cr, monster_type, size

Combatant = PlayerCombatant | MonsterCombatant
```

### Configuration

**`config.py`** - Application settings:
- Command system (MAX_COMMAND_HISTORY = 50)
- UI defaults (DEFAULT_VIEW_MODE, COMBAT_LOG_HEIGHT)
- API settings (OPEN5E_BASE_URL, API_TIMEOUT)
- Combat limits (MAX_BULK_ADD, MAX_HP, etc.)
- Page configuration (PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT)

**`constants.py`** - D&D 5.5e game data:
- CONDITIONS list and CONDITION_EFFECTS descriptions
- EXHAUSTION_EFFECTS by level
- SIZES and SIZE_SPACE
- PROFICIENCY_BY_LEVEL
- MONSTER_SOURCES for Open5e
- VIEW_MODES configuration
- ICONS dictionary

### State Management

**Session State Structure:**
```python
st.session_state:
  # Combat state
  - combatants: list[Combatant]           # All combatants in initiative order
  - current_turn_index: int               # Active combatant index
  - round_number: int                     # Current round
  - combat_active: bool                   # Is combat started?
  - combat_log: list[str]                 # Human-readable log
  
  # Command system
  - command_stack: list[Command]          # Command history (max 50)
  - command_stack_position: int           # Current position in stack
  
  # Persistent data
  - player_roster: dict[str, dict]        # Saved players
  - saved_monsters: dict[str, dict]       # Saved monsters
  - monster_search_cache: dict[str, dict] # API search cache
  
  # UI state
  - view_mode: str                        # 'detailed', 'compact', or 'dense'
  - confirm_end_combat: bool              # End combat confirmation flag
```

## Installation & Setup

```bash
# Clone or create project directory
mkdir dnd-combat-tracker
cd dnd-combat-tracker

# Initialize with uv
uv init

# Add dependencies
uv add streamlit requests

# Data directories will be created automatically on first run
```

## Running the Application

```bash
# From the project root directory
uv run streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use

### Setup Phase

#### Adding Player Characters:

**Method 1: Manual Form**
1. Go to "👥 Players" tab
2. Click "➕ Add Player" tab
3. Fill in character details
4. Choose "💾 Save to Roster" or "➕ Add to Combat Now"

**Method 2: Text Import**
1. Click "📋 Import Text" tab
2. Paste character data in simple format
3. Click "👁 Preview" to verify
4. Click "💾 Import to Roster"

**Method 3: From Saved Roster**
1. Click "👥 Player Roster" tab
2. Click "➕ Add to Combat" on saved player

#### Adding Monsters:

**From API Search:**
1. Go to "👹 Monsters" tab
2. Search for monster name
3. Configure options (number, HP, initiative)
4. Click "➕ Add to Combat"

**From Saved Library:**
1. Click "📚 Saved Monsters" tab
2. Click "➕ Add to Combat"

**Manual Entry:**
1. Scroll to "📋 Quick Add (Generic)" section
2. Fill in stats
3. Click "➕ Add Combatant"

### During Combat

1. Click "▶️ Start Combat" when ready
2. Use header controls for turn navigation
3. Choose view mode (Detailed/Compact/Dense)
4. Expand combatant cards to manage HP, conditions, etc.
5. Use Undo/Redo for mistakes
6. Players at 0 HP get death save prompts on their turn

### Ending Combat

1. Click "🛑 End" in header
2. Click "✓ Confirm" to finalize
3. Combat clears, saved data persists

## D&D 5.5e Rules Implemented

### Initiative
- D20 + DEX modifier roll
- Alert feat adds proficiency bonus (not flat +5)
- Sorted highest to lowest, ties by DEX
- Auto-roll option for monsters and players

### Hit Points
- Current HP / Max HP tracking
- Temporary HP (consumed first, doesn't stack)
- 0 HP = unconscious + death saves
- HP rolling from hit dice for monsters

### Death Saving Throws
- 3 successes = stabilized
- 3 failures = death
- Natural 20 = regain 1 HP
- Natural 1 = 2 failures
- Reset on healing

### Conditions & Exhaustion
- Full 5.5e condition list with effects
- 6 exhaustion levels (cumulative)
- Level 6 = death

## Development Notes

### Adding New Undoable Actions

1. Create command class in `src/utils/commands.py`
2. Add public function in `src/utils/combat.py`
3. Use in components with `st.rerun()` after

### Adding New Components

1. Create file in `src/components/`
2. Import in layouts or other components as needed
3. Use lazy imports to avoid circular dependencies

### Avoiding Circular Imports

Components should import from utils inside functions when needed:
```python
def _do_next():
    from src.utils.combat import next_turn
    next_turn()
```

## Known Limitations

- Local storage only (no cloud sync)
- Single DM per instance
- Desktop-focused layout
- API-dependent monster search
- No automated attack/damage rolls
- No spell slot tracking (use notes)

---

**Version**: 3.1.0  
**Last Updated**: January 2025  
**D&D Rules**: 5.5e (2024 PHB)  
**API**: Open5e v1