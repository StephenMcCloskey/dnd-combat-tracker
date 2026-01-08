# src/constants.py
"""D&D 5.5e game constants and reference data."""

# =============================================================================
# Conditions (5.5e / 2024 PHB)
# =============================================================================
CONDITIONS: list[str] = [
    "Blinded",
    "Charmed",
    "Deafened",
    "Frightened",
    "Grappled",
    "Incapacitated",
    "Invisible",
    "Paralyzed",
    "Petrified",
    "Poisoned",
    "Prone",
    "Restrained",
    "Stunned",
    "Unconscious",
]

CONDITION_EFFECTS: dict[str, str] = {
    "Blinded": (
        "• Can't see, auto-fails sight checks\n"
        "• Attacks have disadvantage\n"
        "• Attacks against have advantage"
    ),
    "Charmed": (
        "• Can't attack charmer\n"
        "• Charmer has advantage on social checks"
    ),
    "Deafened": (
        "• Can't hear, auto-fails hearing checks"
    ),
    "Frightened": (
        "• Disadvantage on checks/attacks while source in sight\n"
        "• Can't move closer to source"
    ),
    "Grappled": (
        "• Speed becomes 0\n"
        "• Ends if grappler incapacitated"
    ),
    "Incapacitated": (
        "• Can't take actions or reactions"
    ),
    "Invisible": (
        "• Impossible to see without special senses\n"
        "• Attacks have advantage\n"
        "• Attacks against have disadvantage"
    ),
    "Paralyzed": (
        "• Incapacitated, can't move or speak\n"
        "• Auto-fail STR/DEX saves\n"
        "• Attacks have advantage\n"
        "• Hits from within 5ft are crits"
    ),
    "Petrified": (
        "• Turned to stone, incapacitated\n"
        "• Can't move or speak\n"
        "• Auto-fail STR/DEX saves\n"
        "• Attacks have advantage\n"
        "• Resistance to all damage\n"
        "• Immune to poison/disease"
    ),
    "Poisoned": (
        "• Disadvantage on attacks and ability checks"
    ),
    "Prone": (
        "• Disadvantage on attacks\n"
        "• Melee attacks against have advantage\n"
        "• Ranged attacks against have disadvantage\n"
        "• Costs half movement to stand"
    ),
    "Restrained": (
        "• Speed becomes 0\n"
        "• Attacks have disadvantage\n"
        "• Attacks against have advantage\n"
        "• Disadvantage on DEX saves"
    ),
    "Stunned": (
        "• Incapacitated, can't move\n"
        "• Can speak only falteringly\n"
        "• Auto-fail STR/DEX saves\n"
        "• Attacks have advantage"
    ),
    "Unconscious": (
        "• Incapacitated, can't move/speak\n"
        "• Unaware of surroundings\n"
        "• Drops held items, falls prone\n"
        "• Auto-fail STR/DEX saves\n"
        "• Attacks have advantage\n"
        "• Hits from within 5ft are crits"
    ),
}

# =============================================================================
# Exhaustion (5.5e / 2024 PHB)
# =============================================================================
EXHAUSTION_EFFECTS: dict[int, str] = {
    1: "Disadvantage on ability checks",
    2: "Speed halved",
    3: "Disadvantage on attacks & saves",
    4: "HP max halved",
    5: "Speed reduced to 0",
    6: "Death",
}

EXHAUSTION_DESCRIPTION: str = """
**Level 1:** Disadvantage on ability checks
**Level 2:** Speed halved
**Level 3:** Disadvantage on attack rolls and saving throws
**Level 4:** HP maximum halved
**Level 5:** Speed reduced to 0
**Level 6:** Death

*Effects are cumulative. Long rest removes 1 level (with food/drink).*
"""

# =============================================================================
# Creature Sizes
# =============================================================================
SIZES: list[str] = [
    "Tiny",
    "Small",
    "Medium",
    "Large",
    "Huge",
    "Gargantuan",
]

SIZE_SPACE: dict[str, str] = {
    "Tiny": "2½ × 2½ ft",
    "Small": "5 × 5 ft",
    "Medium": "5 × 5 ft",
    "Large": "10 × 10 ft",
    "Huge": "15 × 15 ft",
    "Gargantuan": "20 × 20 ft",
}

# =============================================================================
# Proficiency Bonus by Level
# =============================================================================
PROFICIENCY_BY_LEVEL: dict[int, int] = {
    1: 2, 2: 2, 3: 2, 4: 2,
    5: 3, 6: 3, 7: 3, 8: 3,
    9: 4, 10: 4, 11: 4, 12: 4,
    13: 5, 14: 5, 15: 5, 16: 5,
    17: 6, 18: 6, 19: 6, 20: 6,
}

def get_proficiency_bonus(level: int) -> int:
    """Get proficiency bonus for a given level."""
    if level < 1:
        return 2
    if level > 20:
        return 6
    return PROFICIENCY_BY_LEVEL[level]

# =============================================================================
# Ability Scores
# =============================================================================
ABILITIES: list[str] = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

ABILITY_NAMES: dict[str, str] = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "CHA": "Charisma",
}

def ability_modifier(score: int) -> int:
    """Calculate ability modifier from score."""
    return (score - 10) // 2

# =============================================================================
# Death Saving Throws
# =============================================================================
DEATH_SAVE_SUCCESS_THRESHOLD = 10  # Roll >= 10 is success
DEATH_SAVE_SUCCESSES_NEEDED = 3
DEATH_SAVE_FAILURES_NEEDED = 3
DEATH_SAVE_CRIT_SUCCESS = 20  # Regain 1 HP
DEATH_SAVE_CRIT_FAIL = 1  # 2 failures

# =============================================================================
# Monster Sources (Open5e)
# =============================================================================
MONSTER_SOURCES: dict[str, dict] = {
    "wotc-srd": {
        "name": "SRD (Official WotC)",
        "icon": "📕",
        "enabled_default": True,
    },
    "tob": {
        "name": "Tome of Beasts",
        "icon": "📘",
        "enabled_default": False,
    },
    "tob2": {
        "name": "Tome of Beasts 2",
        "icon": "📘",
        "enabled_default": False,
    },
    "tob3": {
        "name": "Tome of Beasts 3",
        "icon": "📘",
        "enabled_default": False,
    },
    "cc": {
        "name": "Creature Codex",
        "icon": "📗",
        "enabled_default": False,
    },
    "menagerie": {
        "name": "Level Up: Monstrous Menagerie",
        "icon": "📙",
        "enabled_default": False,
    },
    "a5e-ag": {
        "name": "Level Up: Adventurer's Guide",
        "icon": "📙",
        "enabled_default": False,
    },
}

# =============================================================================
# Default Monster Types
# =============================================================================
MONSTER_TYPES: list[str] = [
    "Aberration",
    "Beast",
    "Celestial",
    "Construct",
    "Dragon",
    "Elemental",
    "Fey",
    "Fiend",
    "Giant",
    "Humanoid",
    "Monstrosity",
    "Ooze",
    "Plant",
    "Undead",
]

# =============================================================================
# Common Challenge Ratings
# =============================================================================
CHALLENGE_RATINGS: list[str] = [
    "0", "1/8", "1/4", "1/2",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
]

# =============================================================================
# UI Icons
# =============================================================================
ICONS = {
    "player": "👥",
    "monster": "👹",
    "dead": "💀",
    "critical": "🩸",
    "condition": "⚠️",
    "exhaustion": "😫",
    "damage": "💥",
    "heal": "💚",
    "shield": "🛡️",
    "undo": "⏪",
    "redo": "⏩",
    "save": "💾",
    "load": "📂",
    "delete": "🗑️",
    "add": "➕",
    "remove": "➖",
    "dice": "🎲",
    "combat": "⚔️",
    "reference": "📖",
    "settings": "⚙️",
    "stable": "✓",
    "success": "✅",
    "failure": "❌",
    "empty": "⬜",
}

# =============================================================================
# View Modes
# =============================================================================
VIEW_MODES: dict[str, dict] = {
    "detailed": {
        "name": "Detailed",
        "icon": "📋",
        "description": "Full controls and information",
    },
    "compact": {
        "name": "Compact",
        "icon": "📊",
        "description": "Balanced view for active combat",
    },
    "dense": {
        "name": "Dense",
        "icon": "📉",
        "description": "Ultra-compact for large encounters",
    },
}