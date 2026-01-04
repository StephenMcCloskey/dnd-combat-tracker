# D&D 5.5e Combat Tracker

A local Streamlit application for tracking combat encounters in Dungeons & Dragons 5.5e (2024 rules) with full undo/redo functionality and command history.

## Project Overview

This is a comprehensive combat tracker designed for D&D 5.5e that helps Dungeon Masters manage initiative order, hit points, conditions, death saving throws, and all combat-related mechanics in a user-friendly interface. Features integration with the Open5e API for quick monster lookup, personal monster library system, player character management, and a complete undo/redo system with command history.

## Features

### Core Combat Management
- **Initiative Tracking**: Automatic sorting by initiative and DEX modifier
- **Turn Management**: Header-based navigation with Previous/Next buttons always visible
- **Undo/Redo System**: Full command history with 50-command buffer
  - Undo button (⏪) in header with Ctrl+Z shortcut
  - Redo button (⏩) in header with Ctrl+Shift+Z shortcut
  - Command history viewer shows all actions with technical details
  - All actions are undoable: damage, healing, conditions, turn changes, adding/removing combatants
- **Round Counter**: Tracks combat rounds with prominent display in header
- **HP Management**: Damage, healing, and temporary HP tracking (all undoable)
- **Death Saving Throws**: Full tracking with success/failure counters and stabilization
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
- **Initiative Roller**: Auto-roll d20 + DEX for each monster
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
  - 📉 **Dense**: Ultra-compact with 2-column layout (best for large encounters 8+ combatants)
- **Smart Layout**: Two-column display in dense mode with 4+ combatants
- **Responsive Design**: Adapts to sidebar open/closed state
- **Quick Actions**: 
  - Toggle Prone/Stand Up
  - Toggle Unconscious/Wake Up
  - Full Heal (restores HP and clears conditions)
  - Clear All Conditions
  - All actions are undoable
- **Initiative Roller**: Built-in d20 roller with DEX modifier for manual entry
- **Combat Log**: Scrollable event history with adjustable height (100-500px)
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
- **State Preservation**: Saves all combatants, HP, conditions, turn order, rounds, combat log, and command history

### UI/UX
- **Dark Fantasy Theme**: D&D-inspired color scheme with dark leather sidebar
- **Responsive Layout**: Wide layout optimized for desktop use, adapts to sidebar state
- **Header Controls**: Combat navigation always visible at top
  - Undo/Redo (columns 1-2)
  - Previous/Next turn (columns 3-4)
  - Current turn indicator (column 5)
  - End Combat/Confirm (columns 6-7)
- **Three View Modes**: 
  - Detailed (full information)
  - Compact (balanced, default)
  - Dense (maximum efficiency, 2-column layout)
- **Visual Feedback**: Color-coded HP bars, status icons, and hover effects
- **Intuitive Organization**: Sidebar for setup, header for combat, main area for details
- **Readable Metrics**: High-contrast text on white background boxes
- **Empty State**: Helpful welcome screen with clear next steps
- **Overflow Handling**: Sidebar scrolls, text wraps properly, no horizontal overflow
- **Keyboard Shortcuts**: Ctrl+Z (undo), Ctrl+Shift+Z (redo)

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
├── app.py                              # Main Streamlit application
├── pyproject.toml                      # Project dependencies
├── uv.lock                             # Locked dependency versions
├── CLAUDE.md                           # This documentation file
├── .gitignore                          # Git ignore (includes data/)
├── data/                               # Local data storage (git-ignored)
│   ├── combats/                        # Saved combat encounters
│   ├── players/                        # Player rosters
│   │   └── auto_roster.json           # Auto-saved roster
│   └── monsters/                       # Monster libraries
│       └── auto_library.json          # Auto-saved library
└── src/
    ├── __init__.py
    ├── components/
    │   ├── __init__.py
    │   ├── add_combatant_form.py       # Manual combatant entry form
    │   ├── combatant_card.py           # Individual combatant display (3 view modes)
    │   ├── command_history.py          # Command history viewer
    │   ├── conditions_reference.py     # Quick reference guide
    │   ├── monster_search.py           # Monster search & library UI
    │   ├── player_character_form.py    # Player character management
    │   ├── quick_actions.py            # Quick action buttons
    │   └── save_load_manager.py        # Save/load UI with local files
    └── utils/
        ├── __init__.py
        ├── models.py                   # TypedDict models (NEW)
        ├── command_stack.py            # Command pattern base classes (NEW)
        ├── commands.py                 # Specific command implementations (NEW)
        ├── command_manager.py          # Command execution and undo/redo (NEW)
        ├── combat.py                   # Core combat logic (uses commands)
        ├── data_manager.py             # Local file management (NEW)
        ├── import_export.py            # JSON export/import functionality
        └── monster_api.py              # Open5e API integration
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
apply_damage(index=0, damage=10)
  ↓
Creates command
cmd = ApplyDamageCommand(index=0, damage=10)
  ↓
Executes via manager
execute_command(cmd)
  ↓
Command captures state, modifies, captures again
cmd.before_state = capture_state(['combatants'])
... modify combatants ...
cmd.after_state = capture_state(['combatants'])
  ↓
Adds to stack and log
command_stack.append(cmd)
combat_log.append(cmd.description())
```

**Undo Flow:**
```
User clicks "Undo" button
undo_last_command()
  ↓
Gets command at current position
cmd = command_stack[position]
  ↓
Restores previous state
cmd.undo()  # restore_state(before_state)
  ↓
Moves position back
position -= 1
```

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

Benefits:
- IDE autocomplete and type checking
- Clear distinction between player and monster fields
- Still JSON-serializable (just dicts)
- No runtime overhead

### State Management

**Session State Structure:**
```python
st.session_state:
  - combatants: list[Combatant]           # All combatants in initiative order
  - current_turn_index: int               # Active combatant index
  - round_number: int                     # Current round
  - combat_active: bool                   # Is combat started?
  - combat_log: list[str]                 # Human-readable log
  - command_stack: list[Command]          # Command history (max 50)
  - command_stack_position: int           # Current position in stack
  - player_roster: dict[str, dict]        # Saved players
  - saved_monsters: dict[str, dict]       # Saved monsters
  - monster_search_cache: dict[str, dict] # API search cache
  - view_mode: str                        # 'detailed', 'compact', or 'dense'
```

**Data Flow:**
1. User action in UI component
2. Component calls function in `combat.py`
3. Function creates and executes command
4. Command modifies `st.session_state`
5. Streamlit reruns, UI updates
6. Auto-save triggers for roster/library changes

### File Storage

**Auto-Save Files:**
- `data/players/auto_roster.json` - Saved on every roster change
- `data/monsters/auto_library.json` - Saved on every library change
- Loaded automatically on app startup

**Manual Save Files:**
- User-named files in respective directories
- Timestamped if no name provided
- Listed with modification times
- Can be loaded/deleted from UI

**File Format:**
All files are JSON with structure:
```json
{
  "players": { ... },      // or "combatants", "monsters"
  "export_timestamp": "...",
  "version": "1.0"
}
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

# Create directory structure
mkdir -p src/components src/utils
touch src/__init__.py
touch src/components/__init__.py
touch src/utils/__init__.py

# Create main app file
touch app.py

# Data directories will be created automatically
# But you can create them manually if desired:
mkdir -p data/combats data/players data/monsters

# Copy source files into appropriate directories
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
1. In sidebar, find "👥 Player Characters" section (at top)
2. Click "➕ Add Player" tab
3. Fill in character details:
   - Name, Class, Level
   - Proficiency bonus (auto-suggested based on level)
   - Max HP, AC, Speed
   - DEX Modifier
   - Check "Alert Feat" if character has it (adds proficiency to initiative)
   - Add notes (features, attacks, abilities)
4. Choose:
   - "💾 Save to Roster" - Saves for future use (auto-saved)
   - "➕ Add to Combat Now" - Adds immediately with rolled initiative

**Method 2: Text Import**
1. Click "📋 Import Text" tab
2. Paste character data in simple format:
   ```
   Name: Character Name
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
   Features and abilities here
   Attacks go here
   ```
3. Click "👁 Preview" to verify parsing
4. Click "💾 Import to Roster" to save

**Method 3: From Saved Roster**
1. Click "👥 Player Roster" tab
2. Find your saved player (auto-loaded on startup)
3. Click "➕ Add to Combat"
4. Initiative rolled automatically

#### Adding Monsters from API:
1. In sidebar, click "👹 Quick Add Monster"
2. Configure sources if desired (⚙️ Configure Sources & Cache)
3. Search for monster name (e.g., "Goblin")
4. Select from top 10 relevant results
5. Configure options:
   - Number to add (1-20)
   - Use average HP or roll from dice
   - Auto-roll initiative
   - Include notes
6. Click "➕ Add to Combat"
7. Monster automatically saved to library (auto-saved)

#### Adding from Saved Library:
1. Click "📚 Saved Monsters" tab
2. Find your saved monster (auto-loaded on startup)
3. Set number to add
4. Click "➕ Add to Combat"

#### Manual Entry:
1. Scroll to manual form in sidebar
2. Enter name, DEX mod, max HP, AC, speed
3. Optional: CR, size, type
4. Roll initiative or enter manually (🎲 button available)
5. Click "➕ Add Combatant"

### Starting Combat
1. Once combatants added, click "▶️ Start Combat" in header
2. Combatants automatically sorted by initiative
3. Turn order established
4. Command history begins tracking

### During Combat
1. Use header controls:
   - "⏪ Undo" - Undo last action (Ctrl+Z)
   - "⏩ Redo" - Redo last undone action (Ctrl+Shift+Z)
   - "⬅️ Previous" - Go to previous turn
   - "Next ➡️" - Advance to next turn
   - Round/turn indicator shows current combatant
2. **Choose your view mode:**
   - **📋 Detailed** - Full controls, all features visible
   - **📊 Compact** - Balanced view (default), quick damage/heal
   - **📉 Dense** - Minimal cards, 2-column layout for large encounters
3. Expand combatant cards to manage:
   - Apply damage or healing (undoable)
   - Set temporary HP (undoable)
   - Add/remove conditions (undoable)
   - Track death saves (undoable)
   - Adjust exhaustion levels (undoable)
   - Use quick actions (all undoable)
   - Add notes
4. Monitor Combat Overview Dashboard
5. Check Combat Log for event history
6. Toggle to Command History (📋 button) to see technical details

### Using Undo/Redo
- **Undo**: Click ⏪ button or press Ctrl+Z
  - Reverts last action
  - Can undo up to 50 actions
  - Works for: damage, healing, conditions, turn changes, adding/removing combatants
- **Redo**: Click ⏩ button or press Ctrl+Shift+Z
  - Re-applies undone action
  - Redo history cleared when new action taken
- **View History**: Click 📋 checkbox next to Combat Log
  - Shows all commands with position marker
  - Undone commands shown as grayed out
  - Expand for technical details

### Ending Combat
1. Click "🛑 End Combat" in header
2. Click "✓ Confirm" to finalize
3. All combatants cleared (saved monsters/players remain in libraries)
4. Command history cleared

### Managing Data

#### Player Roster:
- **Auto-Save**: Roster auto-saves to `data/players/auto_roster.json` on changes
- **Auto-Load**: Roster auto-loads on app startup
- **Manual Save**: Enter name and click 💾 Save in Save/Load Manager
- **Load**: Select from saved rosters list, click 📂 Load
- **Delete**: Click 🗑️ Delete on any saved roster
- **Download**: Export to computer for backup/sharing
- **Upload**: Import from computer
- **Remove Player**: Delete individual players from roster

#### Monster Library:
- **Auto-Save**: Library auto-saves to `data/monsters/auto_library.json` on changes
- **Auto-Load**: Library auto-loads on app startup
- **Manual Save**: Enter name and click 💾 Save in Save/Load Manager
- **Load**: Select from saved libraries list, click 📂 Load
- **Delete**: Click 🗑️ Delete on any saved library
- **Download**: Export to computer for backup/sharing
- **Upload**: Import from computer
- **Remove Monster**: Delete individual monsters from library

#### Combat State:
- **Save**: Enter name and click 💾 Save in Save/Load Manager (saves to `data/combats/`)
- **Load**: Select from saved combats list, click 📂 Load
- **Delete**: Click 🗑️ Delete on any saved combat
- **Download**: Export to computer for backup/sharing
- **Upload**: Import from computer
- **Includes**: All combatants, HP, conditions, turn order, rounds, combat log, command history

#### Search Cache:
- **Toggle**: Enable/disable in Configure Sources & Cache
- **View Stats**: See cached searches and monster count
- **Clear**: Remove all cached searches

#### Backing Up Data:
The `data/` folder contains all your saved files:
1. **Local Backup**: Copy entire `data/` folder to backup location
2. **Share Between Computers**: 
   - Export roster/library to download
   - Move JSON file to other computer
   - Upload in other instance
3. **Version Control**: `data/` is git-ignored by default
4. **Cloud Backup**: Sync `data/` folder with Dropbox/Google Drive/etc.

## D&D 5.5e Rules Implemented

### Initiative
- D20 + DEX modifier roll
- Alert feat adds proficiency bonus to initiative (not flat +5)
- Sorted highest to lowest
- Ties broken by DEX modifier
- Rolled once per combat
- Auto-roll option for monsters and players

### Hit Points
- Current HP / Max HP tracking
- Temporary HP (consumed first, doesn't stack)
- 0 HP = unconscious + death saves
- Instant death if damage exceeds max HP
- HP rolling from hit dice for monsters
- Speed tracking (default 30ft)

### Death Saving Throws
- 3 successes = stabilized
- 3 failures = death
- Critical hit within 5ft = 2 failures
- Natural 20 = regain 1 HP
- Reset on healing
- All changes undoable

### Conditions
- Full 5.5e condition list
- Effects listed in quick reference
- Multiple conditions can stack
- Quick toggle for common conditions (Prone, Unconscious)
- All condition changes undoable

### Exhaustion
- 6 levels with cumulative effects
- Level 6 = death
- Long rest removes 1 level (with food/drink)
- All effects displayed
- All changes undoable

## Development Notes

### Adding New Features

**Adding a New Undoable Action:**
1. Create command class in `src/utils/commands.py`:
   ```python
   class MyActionCommand(CombatCommand):
       def __init__(self, param1, param2):
           super().__init__()
           self.param1 = param1
           self.param2 = param2
       
       def execute(self):
           self.before_state = self.capture_state(['relevant_keys'])
           # Modify state
           self.after_state = self.capture_state(['relevant_keys'])
       
       def undo(self):
           self.restore_state(self.before_state)
       
       def description(self):
           return "Human readable description"
       
       def technical_description(self):
           return f"MyAction(param1={self.param1}, param2={self.param2})"
   ```

2. Add public function in `src/utils/combat.py`:
   ```python
   def my_action(param1, param2):
       cmd = MyActionCommand(param1, param2)
       execute_command(cmd)
   ```

3. Use in components:
   ```python
   from src.utils.combat import my_action
   
   if st.button("Do Action"):
       my_action(value1, value2)
       st.rerun()
   ```

**Adding New Combatant Fields:**
1. Update TypedDict in `src/utils/models.py`
2. Update initialization in `add_player_combatant()` or `add_monster_combatant()`
3. Update UI in `src/components/combatant_card.py`

**Adding New Component:**
1. Create file in `src/components/`
2. Import combat functions (use lazy imports to avoid circular dependencies)
3. Use `st.rerun()` after state changes
4. Keep UI rendering separate from logic

## Known Limitations

### Technical
- **Local storage only**: No database, files stored in `data/` folder
- **No multi-user support**: Single DM per instance
- **Session-based cache**: Search cache cleared on page refresh
- **Desktop-focused layout**: Not optimized for mobile devices
- **API-dependent**: Monster search requires internet for Open5e API
- **SRD content only**: No proprietary monsters without manual entry
- **50-command limit**: Command history capped at 50 actions
- **No cloud sync**: Data doesn't sync across devices (by design)

### Features
- **No automated attack rolls**: Attack/damage rolls done externally
- **No spell tracking**: Beyond notes field
- **No lair/legendary actions UI**: Must track manually
- **No automated concentration checks**: Manual tracking
- **No multi-combat history**: One combat at a time
- **No campaign management**: Combat-focused only
- **No OCR**: Can't read character sheet images
- **Text import**: Relies on specific formatting
- **No class resources**: Spell slots, rage, ki must be tracked in notes
- **No equipment system**: Weight/encumbrance not tracked

### Performance
- **Large combats**: 20+ combatants may slow UI
- **Search cache**: Limited to session
- **No pagination**: Search results show top 10 only
- **Deepcopy overhead**: State capture uses memory for large combats

## Troubleshooting

### Undo/Redo Issues
- **Undo button disabled**: No actions to undo (position at -1)
- **Redo button disabled**: No actions to redo (position at end of stack)
- **Undo doesn't work**: Command stack may be corrupted, restart app
- **Lost history after combat end**: Expected behavior, stack clears on combat end
- **Can't undo past 50 actions**: Stack limited to 50 commands

### Player Character Issues
- **Text import not parsing**: Check format matches example, ensure "Name:" and "Class:" fields present
- **Initiative wrong**: Verify Alert feat checkbox matches character, check DEX modifier
- **Missing notes**: Ensure "Notes:" line present, everything after becomes notes
- **Can't save to roster**: Must have Name and Class at minimum
- **Player disappeared**: Check auto-load worked, check `data/players/auto_roster.json` exists
- **Roster not persisting**: Check `data/` folder permissions

### Monster Search Issues
- **"No monsters found"**: Check source filters, try broader search terms
- **Timeout errors**: Check internet connection, try again
- **Wrong results**: Disable cache to get fresh data
- **Missing sources**: Enable desired sources in configuration
- **Library not persisting**: Check `data/monsters/auto_library.json` exists

### Combat Issues
- **Can't start combat**: Ensure at least one combatant added
- **Turn navigation not working**: Check if combat is active
- **Combatants out of order**: Initiative sorted on combat start, not during
- **Lost combatants**: Check if combat was ended (clears all)
- **Undo not working after turn change**: Each turn change is a separate undoable action

### Data Persistence
- **Files not saving**: Check `data/` folder permissions, check disk space
- **Auto-save not working**: Check `data/players/` and `data/monsters/` folders exist
- **Can't find saved files**: Check you're in the right directory (data/combats/, data/players/, data/monsters/)
- **Combat lost on refresh**: Expected - combats don't auto-save, must save manually
- **Import not working**: Verify JSON file format and version
- **Roster merge issues**: Import only adds new players, doesn't overwrite existing
- **Lost all data**: Check if `data/` folder was deleted, restore from backup

### UI Issues
- **Metrics not visible**: Check browser dark mode, metrics have white backgrounds with borders
- **Sidebar scrolling**: Sidebar scrolls vertically, content should not overflow
- **Slow performance**: Reduce number of combatants, clear old logs, switch to dense view mode
- **Cards too large**: Switch to Compact or Dense view mode
- **Can't see all combatants**: Use Dense mode for two-column layout
- **Text overflowing**: Sidebar has proper word-wrapping and overflow handling
- **Keyboard shortcuts not working**: Ensure focus is on app, not browser controls

### Circular Import Errors
- **"cannot import name 'X'"**: Check for circular imports between components and utils
- **Fix**: Use lazy imports (import inside functions) in component files
- **Example**: Import combat functions inside button callbacks, not at module level

## Credits

- **Open5e API**: Free monster database (https://open5e.com)
- **Streamlit**: Web framework
- **D&D 5.5e (2024)**: Rules reference

---

**Version**: 3.0.0  
**Last Updated**: January 2026  
**D&D Rules**: 5.5e (2024 PHB)  
**API**: Open5e v1  
**New in 3.0**: 
- Complete command pattern with undo/redo
- TypedDict models for type safety
- Player/Monster type separation
- Local file storage with auto-save/load
- Command history viewer
- Speed field for all combatants
- 50-command history buffer