import requests
import random
from difflib import SequenceMatcher

# Available sources in Open5e
AVAILABLE_SOURCES = {
    'wotc-srd': {'name': 'SRD (Official WotC)', 'icon': '📕', 'enabled_default': True},
    'tob': {'name': 'Tome of Beasts', 'icon': '📘', 'enabled_default': False},
    'tob2': {'name': 'Tome of Beasts 2', 'icon': '📘', 'enabled_default': False},
    'tob3': {'name': 'Tome of Beasts 3', 'icon': '📘', 'enabled_default': False},
    'cc': {'name': 'Creature Codex', 'icon': '📗', 'enabled_default': False},
    'menagerie': {'name': 'Level Up: Monstrous Menagerie', 'icon': '📙', 'enabled_default': False},
    'a5e-ag': {'name': 'Level Up: Adventurer\'s Guide', 'icon': '📙', 'enabled_default': False},
}

def get_source_display(source_slug, source_title=None):
    """Get display name and icon for a source"""
    for slug, info in AVAILABLE_SOURCES.items():
        if slug in source_slug:
            return f"{info['icon']} {info['name']}"
    
    # Fallback to title if not in our list
    if source_title:
        return f"📚 {source_title}"
    return f"📚 {source_slug}"

def calculate_match_score(search_term, monster_name):
    """Calculate relevance score for a monster name match"""
    search_lower = search_term.lower().strip()
    name_lower = monster_name.lower().strip()
    
    # Exact match
    if search_lower == name_lower:
        return 1000
    
    # Starts with search term
    if name_lower.startswith(search_lower):
        return 900
    
    # Search term is a complete word in the name
    words = name_lower.split()
    if search_lower in words:
        return 800
    
    # Contains search term
    if search_lower in name_lower:
        return 700
    
    # Use sequence matcher for fuzzy matching
    ratio = SequenceMatcher(None, search_lower, name_lower).ratio()
    
    # Bonus for shorter names (more likely to be relevant)
    length_penalty = len(name_lower) / 50.0  # Normalize to 0-1 range
    
    # Final score
    return ratio * 500 - length_penalty * 50

def search_monster(name, enabled_sources=None):
    """Search for a monster by name using Open5e API
    
    Args:
        name: Monster name to search for
        enabled_sources: List of source slugs to include (None = all sources)
    """
    import streamlit as st
    
    # Initialize cache if it doesn't exist
    if 'monster_search_cache' not in st.session_state:
        st.session_state.monster_search_cache = {}
    
    # Create cache key (case-insensitive search term + sources)
    cache_key = f"{name.lower().strip()}|{','.join(sorted(enabled_sources)) if enabled_sources else 'all'}"
    
    # Check cache first
    if cache_key in st.session_state.monster_search_cache:
        cached_results = st.session_state.monster_search_cache[cache_key]
        return cached_results['results'], cached_results.get('error')
    
    try:
        url = f"https://api.open5e.com/monsters/?search={name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data['count'] == 0:
            # Cache the "not found" result
            st.session_state.monster_search_cache[cache_key] = {
                'results': None,
                'error': "No monsters found with that name"
            }
            return None, "No monsters found with that name"
        
        # Get results
        results = data['results']
        
        # Filter by enabled sources if specified
        if enabled_sources is not None:
            filtered_results = []
            for monster in results:
                source_slug = monster.get('document__slug', '')
                # Check if any enabled source is in the document slug
                if any(source in source_slug for source in enabled_sources):
                    filtered_results.append(monster)
            results = filtered_results
        
        if not results:
            # Cache the "no results in sources" result
            st.session_state.monster_search_cache[cache_key] = {
                'results': None,
                'error': "No monsters found in selected sources"
            }
            return None, "No monsters found in selected sources"
        
        # Calculate scores and sort
        scored_results = []
        for monster in results:
            score = calculate_match_score(name, monster['name'])
            scored_results.append((score, monster))
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 10 most relevant results
        top_results = [monster for score, monster in scored_results[:10]]
        
        # Cache the successful results
        st.session_state.monster_search_cache[cache_key] = {
            'results': top_results,
            'error': None
        }
        
        return top_results, None
        
    except requests.Timeout:
        error_msg = "Request timed out. Please try again."
        # Don't cache timeout errors
        return None, error_msg
    except requests.RequestException as e:
        error_msg = f"Error connecting to API: {str(e)}"
        # Don't cache connection errors
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        # Don't cache unexpected errors
        return None, error_msg

def clear_monster_cache():
    """Clear the monster search cache"""
    import streamlit as st
    if 'monster_search_cache' in st.session_state:
        st.session_state.monster_search_cache = {}

def get_cache_stats():
    """Get statistics about the current cache"""
    import streamlit as st
    if 'monster_search_cache' not in st.session_state:
        return 0, 0
    
    cache = st.session_state.monster_search_cache
    total_searches = len(cache)
    total_monsters = sum(
        len(entry['results']) if entry['results'] else 0 
        for entry in cache.values()
    )
    
    return total_searches, total_monsters

def parse_monster_stats(monster_data):
    """Parse monster data from Open5e API into combatant format"""
    
    # Calculate DEX modifier from ability score
    dex_score = monster_data.get('dexterity', 10)
    dex_mod = (dex_score - 10) // 2
    
    # Get HP (can be average or rolled)
    hp_average = monster_data.get('hit_points', 10)
    hp_dice = monster_data.get('hit_dice', None)
    
    # Get AC
    ac = monster_data.get('armor_class', 10)
    
    # Roll initiative (d20 + DEX)
    initiative = random.randint(1, 20) + dex_mod
    
    # Build notes with useful info
    notes_parts = []
    
    # Size, type, alignment
    size = monster_data.get('size', 'Medium')
    type_info = monster_data.get('type', 'Unknown')
    alignment = monster_data.get('alignment', 'Unaligned')
    notes_parts.append(f"{size} {type_info}, {alignment}")
    
    # CR and proficiency
    cr = monster_data.get('challenge_rating', '0')
    notes_parts.append(f"CR: {cr}")
    
    # Speed
    speed = monster_data.get('speed', {})
    if isinstance(speed, dict):
        speed_str = ', '.join([f"{k}: {v}" for k, v in speed.items()])
        notes_parts.append(f"Speed: {speed_str}")
    
    # Saving throws
    if monster_data.get('strength_save'):
        notes_parts.append(f"Saves: STR +{monster_data['strength_save']}")
    
    # Special abilities (first 3)
    special_abilities = monster_data.get('special_abilities', [])
    if special_abilities:
        notes_parts.append("\nSpecial Abilities:")
        for ability in special_abilities[:3]:
            name = ability.get('name', 'Unknown')
            desc = ability.get('desc', '')
            # Truncate long descriptions
            if len(desc) > 100:
                desc = desc[:97] + "..."
            notes_parts.append(f"• {name}: {desc}")
    
    # Actions (first 2)
    actions = monster_data.get('actions', [])
    if actions:
        notes_parts.append("\nActions:")
        for action in actions[:2]:
            name = action.get('name', 'Unknown')
            desc = action.get('desc', '')
            if len(desc) > 100:
                desc = desc[:97] + "..."
            notes_parts.append(f"• {name}: {desc}")
    
    notes = '\n'.join(notes_parts)
    
    return {
        'name': monster_data.get('name', 'Unknown Monster'),
        'max_hp': hp_average,
        'hp_dice': hp_dice,
        'ac': ac,
        'dex_modifier': dex_mod,
        'initiative': initiative,
        'cr': cr,
        'size': size,
        'type': type_info,
        'notes': notes,
        'full_data': monster_data  # Keep full data for reference
    }

def roll_hp_from_dice(hit_dice_str):
    """Roll HP from hit dice string (e.g., '2d6+2')"""
    try:
        import re
        
        # Parse hit dice string
        match = re.match(r'(\d+)d(\d+)([+-]\d+)?', hit_dice_str)
        if not match:
            return None
        
        num_dice = int(match.group(1))
        die_size = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        # Roll the dice
        total = sum(random.randint(1, die_size) for _ in range(num_dice))
        total += modifier
        
        return max(1, total)  # Minimum 1 HP
        
    except Exception:
        return None