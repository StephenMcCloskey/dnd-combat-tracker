# src/components/monster_search.py
"""Monster search and library management."""

import streamlit as st
import hashlib
from src.utils.monster_api import (
    search_monster, parse_monster_stats, roll_hp_from_dice,
    get_source_display, clear_monster_cache, get_cache_stats
)
from src.utils.combat import add_monster_combatant
from src.utils.import_export import export_monster_library, import_monster_library
from src.constants import MONSTER_SOURCES
from src.config import MAX_BULK_ADD


def initialize_source_preferences():
    """Initialize source preferences in session state."""
    if 'enabled_monster_sources' not in st.session_state:
        st.session_state.enabled_monster_sources = [
            slug for slug, info in MONSTER_SOURCES.items()
            if info['enabled_default']
        ]
    
    if 'use_monster_cache' not in st.session_state:
        st.session_state.use_monster_cache = True
    
    if 'saved_monsters' not in st.session_state:
        st.session_state.saved_monsters = {}


def save_monster_to_library(monster_data: dict, parsed_stats: dict):
    """Save a monster to the user's library."""
    monster_id = hashlib.md5(
        f"{monster_data['name']}_{monster_data.get('document__slug', '')}".encode()
    ).hexdigest()
    
    st.session_state.saved_monsters[monster_id] = {
        'name': monster_data['name'],
        'source': monster_data.get('document__slug', ''),
        'source_title': monster_data.get('document__title', ''),
        'raw_data': monster_data,
        'parsed_stats': parsed_stats,
        'saved_at': __import__('datetime').datetime.now().isoformat()
    }


def render_saved_monsters():
    """Render the saved monsters library."""
    
    if not st.session_state.saved_monsters:
        st.info("No saved monsters yet. Add monsters from search results.")
        return
    
    st.markdown(f"**📚 {len(st.session_state.saved_monsters)} Saved Monster(s)**")
    
    for monster_id, saved_monster in st.session_state.saved_monsters.items():
        parsed = saved_monster['parsed_stats']
        source_display = get_source_display(
            saved_monster['source'],
            saved_monster['source_title']
        )
        
        with st.expander(f"{saved_monster['name']} (CR {parsed['cr']})"):
            # Compact stats display
            st.caption(f"**HP:** {parsed['max_hp']} · **AC:** {parsed['ac']} · **CR:** {parsed['cr']} · {source_display}")
            
            # Show notes if present
            if parsed.get('notes'):
                with st.container(height=150):
                    st.text(parsed['notes'])
            
            # Quick add options
            col1, col2 = st.columns(2)
            with col1:
                num_instances = st.number_input(
                    "Number",
                    min_value=1,
                    max_value=MAX_BULK_ADD,
                    value=1,
                    key=f"saved_num_{monster_id}"
                )
            with col2:
                auto_roll_init = st.checkbox(
                    "Auto-roll Init",
                    value=True,
                    key=f"saved_init_{monster_id}"
                )
            
            # Shared initiative option
            if num_instances > 1:
                shared_init = st.checkbox(
                    "Share Initiative",
                    value=True,
                    key=f"saved_shared_init_{monster_id}",
                    help="All instances use the same initiative roll"
                )
            else:
                shared_init = False
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    f"➕ Add to Combat",
                    key=f"add_saved_{monster_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    _add_monster_instances(
                        parsed, num_instances, auto_roll_init, shared_init
                    )
                    st.success(f"Added {num_instances} {saved_monster['name']}(s)!")
                    st.rerun()
            
            with col2:
                if st.button(
                    "🗑️ Remove",
                    key=f"remove_saved_{monster_id}",
                    use_container_width=True
                ):
                    del st.session_state.saved_monsters[monster_id]
                    st.success("Monster removed from library")
                    st.rerun()


def render_monster_search():
    """Render the monster search and quick-add interface."""
    
    initialize_source_preferences()
    
    st.markdown("#### 🐉 Monster Search")
    
    # Tabs for search and saved monsters
    tab1, tab2 = st.tabs(["🔍 Search", "📚 Saved Monsters"])
    
    with tab1:
        _render_search_tab()
    
    with tab2:
        _render_library_tab()


def _render_search_tab():
    """Render the search tab content."""
    
    # Source configuration
    with st.expander("⚙️ Configure Sources & Cache", expanded=False):
        st.markdown("**Select sources to search:**")
        
        for slug, info in MONSTER_SOURCES.items():
            current_state = slug in st.session_state.enabled_monster_sources
            
            new_state = st.checkbox(
                f"{info['icon']} {info['name']}",
                value=current_state,
                key=f"source_toggle_{slug}"
            )
            
            if new_state and not current_state:
                st.session_state.enabled_monster_sources.append(slug)
            elif not new_state and current_state:
                st.session_state.enabled_monster_sources.remove(slug)
        
        enabled_count = len(st.session_state.enabled_monster_sources)
        if enabled_count == 0:
            st.warning("⚠️ No sources selected.")
        else:
            st.caption(f"✓ {enabled_count} source(s) enabled")
        
        st.markdown("---")
        
        # Cache toggle
        use_cache = st.checkbox(
            "🔄 Use search cache",
            value=st.session_state.use_monster_cache,
            key="cache_toggle"
        )
        st.session_state.use_monster_cache = use_cache
        
        if use_cache:
            cache_searches, cache_monsters = get_cache_stats()
            st.caption(f"💾 Cached: {cache_searches} searches, {cache_monsters} monsters")
            
            if cache_searches > 0:
                if st.button("🗑️ Clear Cache", use_container_width=True):
                    clear_monster_cache()
                    st.success("Cache cleared!")
                    st.rerun()
    
    # Search form
    with st.form("monster_search_form"):
        search_term = st.text_input("Monster Name", placeholder="e.g., Goblin, Dragon")
        search_button = st.form_submit_button("🔍 Search", use_container_width=True, type="primary")
    
    if search_button and search_term:
        if not st.session_state.enabled_monster_sources:
            st.error("Please enable at least one source.")
        else:
            _perform_search(search_term)
    
    # Display results
    _display_search_results()


def _perform_search(search_term: str):
    """Perform monster search."""
    if st.session_state.use_monster_cache:
        cache_key = f"{search_term.lower().strip()}|{','.join(sorted(st.session_state.enabled_monster_sources))}"
        is_cached = 'monster_search_cache' in st.session_state and cache_key in st.session_state.monster_search_cache
        
        if is_cached:
            st.info("💾 Using cached results")
        
        with st.spinner(f"Searching for {search_term}..."):
            results, error = search_monster(search_term, st.session_state.enabled_monster_sources)
    else:
        st.info("🌐 Calling API (cache disabled)")
        cache_key = f"{search_term.lower().strip()}|{','.join(sorted(st.session_state.enabled_monster_sources))}"
        if 'monster_search_cache' in st.session_state and cache_key in st.session_state.monster_search_cache:
            del st.session_state.monster_search_cache[cache_key]
        
        with st.spinner(f"Searching for {search_term}..."):
            results, error = search_monster(search_term, st.session_state.enabled_monster_sources)
    
    if error:
        st.error(error)
    elif results:
        st.session_state['monster_search_results'] = results
        st.session_state['search_term'] = search_term


def _display_search_results():
    """Display search results."""
    if 'monster_search_results' not in st.session_state or not st.session_state['monster_search_results']:
        return
    
    st.markdown("---")
    result_count = len(st.session_state['monster_search_results'])
    st.markdown(f"**Top {result_count} result(s) for '{st.session_state.get('search_term', '')}'**")
    
    for idx, monster in enumerate(st.session_state['monster_search_results']):
        source = monster.get('document__slug', 'unknown')
        source_title = monster.get('document__title', 'Unknown Source')
        source_display = get_source_display(source, source_title)
        
        with st.expander(f"{monster['name']} (CR {monster.get('challenge_rating', '?')})"):
            parsed = parse_monster_stats(monster)
            
            # Compact stats display
            st.caption(f"**HP:** {parsed['max_hp']} ({parsed['hp_dice'] or 'N/A'}) · **AC:** {parsed['ac']} · **DEX:** {parsed['dex_modifier']:+d} · {source_display}")
            
            st.markdown("**Add Options:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                use_average_hp = st.checkbox("Use Average HP", value=True, key=f"avg_hp_{idx}")
                num_instances = st.number_input("Number", min_value=1, max_value=MAX_BULK_ADD, value=1, key=f"num_{idx}")
            
            with col2:
                auto_roll_init = st.checkbox("Auto-roll Initiative", value=True, key=f"auto_init_{idx}")
                if num_instances > 1:
                    shared_init = st.checkbox("Share Initiative", value=True, key=f"shared_init_{idx}",
                                              help="All instances use the same initiative roll")
                else:
                    shared_init = False
                show_notes = st.checkbox("Include Notes", value=True, key=f"notes_{idx}")
            
            if st.button(f"➕ Add {monster['name']} to Combat", key=f"add_monster_{idx}", use_container_width=True):
                notes = parsed['notes'] if show_notes else ""
                hp = parsed['max_hp'] if use_average_hp else (roll_hp_from_dice(parsed['hp_dice']) or parsed['max_hp'])
                
                _add_monster_instances(
                    {**parsed, 'max_hp': hp, 'notes': notes},
                    num_instances, auto_roll_init, shared_init
                )
                
                # Save to library
                save_monster_to_library(monster, parsed)
                
                st.success(f"Added {num_instances} {monster['name']}(s)!")
                del st.session_state['monster_search_results']
                if 'search_term' in st.session_state:
                    del st.session_state['search_term']
                st.rerun()
            
            # Notes preview
            if show_notes and parsed['notes']:
                with st.expander("📋 Full Stats Preview"):
                    st.text(parsed['notes'])


def _render_library_tab():
    """Render the library tab content."""
    
    st.markdown("##### Monster Library")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.saved_monsters:
            export_data = export_monster_library()
            from src.utils.import_export import get_monster_library_filename
            st.download_button(
                label="📥 Export Library",
                data=export_data,
                file_name=get_monster_library_filename(),
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        uploaded_file = st.file_uploader(
            "📤 Import Library",
            type=['json'],
            key="monster_library_upload",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.read().decode('utf-8')
                success, message = import_monster_library(json_str)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    st.markdown("---")
    render_saved_monsters()


def _add_monster_instances(parsed: dict, num_instances: int, auto_roll_init: bool, shared_init: bool):
    """Add monster instances to combat."""
    import random
    
    # Roll initiative once if shared
    if shared_init and auto_roll_init:
        shared_init_roll = random.randint(1, 20) + parsed['dex_modifier']
    
    for i in range(num_instances):
        instance_name = f"{parsed['name']} {i+1}" if num_instances > 1 else parsed['name']
        
        if auto_roll_init:
            if shared_init:
                init = shared_init_roll
            else:
                init = random.randint(1, 20) + parsed['dex_modifier']
        else:
            init = 10 + parsed['dex_modifier']
        
        add_monster_combatant(
            name=instance_name,
            initiative=init,
            dex_modifier=parsed['dex_modifier'],
            max_hp=parsed['max_hp'],
            ac=parsed['ac'],
            speed=30,
            notes=parsed.get('notes', ''),
            cr=parsed.get('cr', '?'),
            monster_type=parsed.get('type', 'Unknown'),
            size=parsed.get('size', 'Medium')
        )