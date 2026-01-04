import streamlit as st
from src.utils.monster_api import search_monster, parse_monster_stats, roll_hp_from_dice, AVAILABLE_SOURCES, get_source_display, clear_monster_cache, get_cache_stats
from src.utils.combat import add_combatant, log_event
from src.utils.import_export import export_monster_library, import_monster_library, get_monster_library_filename
import hashlib

def initialize_source_preferences():
    """Initialize source preferences in session state"""
    if 'enabled_monster_sources' not in st.session_state:
        # Enable only defaults
        st.session_state.enabled_monster_sources = [
            slug for slug, info in AVAILABLE_SOURCES.items() 
            if info['enabled_default']
        ]
    
    if 'use_monster_cache' not in st.session_state:
        st.session_state.use_monster_cache = True
    
    if 'saved_monsters' not in st.session_state:
        st.session_state.saved_monsters = {}

def save_monster_to_library(monster_data, parsed_stats):
    """Save a monster to the user's library"""
    # Create a unique ID for the monster
    monster_id = hashlib.md5(
        f"{monster_data['name']}_{monster_data.get('document__slug', '')}".encode()
    ).hexdigest()
    
    # Store both raw API data and parsed stats
    st.session_state.saved_monsters[monster_id] = {
        'name': monster_data['name'],
        'source': monster_data.get('document__slug', ''),
        'source_title': monster_data.get('document__title', ''),
        'raw_data': monster_data,
        'parsed_stats': parsed_stats,
        'saved_at': __import__('datetime').datetime.now().isoformat()
    }

def render_saved_monsters():
    """Render the saved monsters library"""
    from src.utils.combat import add_monster_combatant
    
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
        
        with st.expander(f"{saved_monster['name']} (CR {parsed['cr']}) - {source_display}"):
            # Display stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("HP", parsed['max_hp'])
            with col2:
                st.metric("AC", parsed['ac'])
            with col3:
                st.metric("CR", parsed['cr'])
            
            # Quick add options
            col1, col2 = st.columns(2)
            with col1:
                num_instances = st.number_input(
                    "Number to Add", 
                    min_value=1, 
                    max_value=20, 
                    value=1, 
                    key=f"saved_num_{monster_id}"
                )
            with col2:
                auto_roll_init = st.checkbox(
                    "Auto-roll Initiative", 
                    value=True, 
                    key=f"saved_init_{monster_id}"
                )
            
            # NEW: Shared initiative option
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
                    # Roll initiative once if shared
                    if shared_init and auto_roll_init:
                        import random
                        shared_init_roll = random.randint(1, 20) + parsed['dex_modifier']
                    
                    # Add multiple instances
                    for i in range(num_instances):
                        instance_name = f"{parsed['name']} {i+1}" if num_instances > 1 else parsed['name']
                        
                        # Roll initiative
                        if auto_roll_init:
                            if shared_init:
                                init = shared_init_roll
                            else:
                                import random
                                init = random.randint(1, 20) + parsed['dex_modifier']
                        else:
                            init = 10 + parsed['dex_modifier']
                        
                        # Add to combat using new function
                        add_monster_combatant(
                            name=instance_name,
                            initiative=init,
                            dex_modifier=parsed['dex_modifier'],
                            max_hp=parsed['max_hp'],
                            ac=parsed['ac'],
                            speed=30,  # Default
                            notes=parsed['notes'],
                            cr=parsed['cr'],
                            monster_type=parsed.get('type', 'Unknown'),
                            size=parsed.get('size', 'Medium')
                        )
                    
                    if shared_init and num_instances > 1:
                        st.success(f"Added {num_instances} {saved_monster['name']}(s) with shared initiative!")
                    else:
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
    """Render the monster search and quick-add interface"""
    
    # Initialize preferences
    initialize_source_preferences()
    
    st.subheader("🐉 Quick Add Monster")
    
    # Tabs for search and saved monsters
    tab1, tab2 = st.tabs(["🔍 Search", "📚 Saved Monsters"])
    
    with tab1:
        # Source configuration
        with st.expander("⚙️ Configure Sources & Cache", expanded=False):
            st.markdown("**Select which sources to search:**")
            
            # Create checkboxes for each source
            for slug, info in AVAILABLE_SOURCES.items():
                current_state = slug in st.session_state.enabled_monster_sources
                
                new_state = st.checkbox(
                    f"{info['icon']} {info['name']}",
                    value=current_state,
                    key=f"source_toggle_{slug}"
                )
                
                # Update session state if changed
                if new_state and not current_state:
                    st.session_state.enabled_monster_sources.append(slug)
                elif not new_state and current_state:
                    st.session_state.enabled_monster_sources.remove(slug)
            
            # Show current selection count
            enabled_count = len(st.session_state.enabled_monster_sources)
            if enabled_count == 0:
                st.warning("⚠️ No sources selected. Please enable at least one source.")
            else:
                st.success(f"✓ {enabled_count} source(s) enabled")
            
            st.markdown("---")
            
            # Cache toggle
            use_cache = st.checkbox(
                "🔄 Use search cache (faster, fewer API calls)",
                value=st.session_state.use_monster_cache,
                key="cache_toggle"
            )
            st.session_state.use_monster_cache = use_cache
            
            if use_cache:
                # Cache statistics and management
                cache_searches, cache_monsters = get_cache_stats()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"💾 Cached: {cache_searches} searches")
                with col2:
                    st.caption(f"📊 {cache_monsters} monsters")
                
                if cache_searches > 0:
                    if st.button("🗑️ Clear Cache", use_container_width=True):
                        clear_monster_cache()
                        st.success("Cache cleared!")
                        st.rerun()
            else:
                st.caption("⚠️ Cache disabled - all searches will call API")
        
        # Search form
        with st.form("monster_search_form"):
            search_term = st.text_input("Monster Name", placeholder="e.g., Goblin, Dragon, Beholder")
            search_button = st.form_submit_button("🔍 Search", use_container_width=True, type="primary")
        
        if search_button and search_term:
            if not st.session_state.enabled_monster_sources:
                st.error("Please enable at least one source in the configuration.")
            else:
                # Check if we're using cache
                if st.session_state.use_monster_cache:
                    cache_key = f"{search_term.lower().strip()}|{','.join(sorted(st.session_state.enabled_monster_sources))}"
                    is_cached = 'monster_search_cache' in st.session_state and cache_key in st.session_state.monster_search_cache
                    
                    if is_cached:
                        st.info("💾 Using cached results")
                    
                    with st.spinner(f"Searching for {search_term}..."):
                        results, error = search_monster(search_term, st.session_state.enabled_monster_sources)
                else:
                    # Force bypass cache
                    st.info("🌐 Calling API (cache disabled)")
                    # Temporarily clear the specific cache entry
                    cache_key = f"{search_term.lower().strip()}|{','.join(sorted(st.session_state.enabled_monster_sources))}"
                    if 'monster_search_cache' in st.session_state and cache_key in st.session_state.monster_search_cache:
                        del st.session_state.monster_search_cache[cache_key]
                    
                    with st.spinner(f"Searching for {search_term}..."):
                        results, error = search_monster(search_term, st.session_state.enabled_monster_sources)
                
                if error:
                    st.error(error)
                elif results:
                    # Store results in session state
                    st.session_state['monster_search_results'] = results
                    st.session_state['search_term'] = search_term
    
    # Display results if available
    if 'monster_search_results' in st.session_state and st.session_state['monster_search_results']:
        st.markdown("---")
        result_count = len(st.session_state['monster_search_results'])
        st.markdown(f"**Top {result_count} result(s) for '{st.session_state.get('search_term', '')}'**")
        
        if result_count > 5:
            st.caption("Showing most relevant matches")
        
        for idx, monster in enumerate(st.session_state['monster_search_results']):
            # Get source document info
            source = monster.get('document__slug', 'unknown')
            source_title = monster.get('document__title', 'Unknown Source')
            
            # Get display name
            source_display = get_source_display(source, source_title)
            
            with st.expander(f"{monster['name']} (CR {monster.get('challenge_rating', '?')}) - {source_display}"):
                # Parse monster stats
                parsed = parse_monster_stats(monster)
                
                # Display preview
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("HP", parsed['max_hp'])
                    if parsed['hp_dice']:
                        st.caption(f"Hit Dice: {parsed['hp_dice']}")
                
                with col2:
                    st.metric("AC", parsed['ac'])
                    st.caption(f"DEX Mod: {parsed['dex_modifier']:+d}")
                
                with col3:
                    st.metric("CR", parsed['cr'])
                    st.caption(f"{parsed['size']} {parsed['type']}")
                
                # Show full source info
                st.caption(f"📚 Source: {source_title}")
                
                st.markdown("**Add Options:**")
    
                col1, col2 = st.columns(2)
                
                with col1:
                    use_average_hp = st.checkbox("Use Average HP", value=True, key=f"avg_hp_{idx}")
                    num_instances = st.number_input("Number to Add", min_value=1, max_value=20, value=1, key=f"num_{idx}")
                
                with col2:
                    auto_roll_init = st.checkbox("Auto-roll Initiative", value=True, key=f"auto_init_{idx}")
                    # NEW: Shared initiative option (only show if adding multiple)
                    if num_instances > 1:
                        shared_init = st.checkbox("Share Initiative", value=True, key=f"shared_init_{idx}", 
                                                help="All instances use the same initiative roll")
                    else:
                        shared_init = False
                    
                    show_notes = st.checkbox("Include Notes", value=True, key=f"notes_{idx}")
                
                # Add button
                if st.button(f"➕ Add {monster['name']} to Combat", key=f"add_monster_{idx}", use_container_width=True):
                    from src.utils.combat import add_monster_combatant
                    
                    # Roll initiative once if shared
                    if shared_init and auto_roll_init:
                        import random
                        shared_init_roll = random.randint(1, 20) + parsed['dex_modifier']
                    
                    # Add multiple instances if requested
                    for i in range(num_instances):
                        # Determine name
                        if num_instances > 1:
                            instance_name = f"{parsed['name']} {i+1}"
                        else:
                            instance_name = parsed['name']
                        
                        # Determine HP
                        if use_average_hp:
                            hp = parsed['max_hp']
                        else:
                            # Roll HP from hit dice
                            if parsed['hp_dice']:
                                rolled_hp = roll_hp_from_dice(parsed['hp_dice'])
                                hp = rolled_hp if rolled_hp else parsed['max_hp']
                            else:
                                hp = parsed['max_hp']
                        
                        # Determine initiative
                        if auto_roll_init:
                            if shared_init:
                                # Use the shared roll
                                init = shared_init_roll
                            else:
                                # Roll individually
                                import random
                                init = random.randint(1, 20) + parsed['dex_modifier']
                        else:
                            init = 10 + parsed['dex_modifier']
                        
                        # Determine notes
                        notes = parsed['notes'] if show_notes else ""
                        
                        # Add to combat using new function
                        add_monster_combatant(
                            name=instance_name,
                            initiative=init,
                            dex_modifier=parsed['dex_modifier'],
                            max_hp=hp,
                            ac=parsed['ac'],
                            speed=30,  # Default, could parse from API
                            notes=notes,
                            cr=parsed['cr'],
                            monster_type=parsed['type'],
                            size=parsed['size']
                        )
                    
                    if shared_init and num_instances > 1:
                        st.success(f"Added {num_instances} {monster['name']}(s) to combat with shared initiative {shared_init_roll}!")
                    else:
                        st.success(f"Added {num_instances} {monster['name']}(s) to combat!")
                    
                    # Save to library
                    save_monster_to_library(monster, parsed)
                    
                    # Clear search results
                    del st.session_state['monster_search_results']
                    if 'search_term' in st.session_state:
                        del st.session_state['search_term']
                    
                    st.rerun()
                
                # Show full notes preview
                if show_notes:
                    with st.expander("📋 Full Stats Preview"):
                        st.text(parsed['notes'])
    
    with tab2:
        # Monster library management
        st.markdown("### Monster Library")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export library
            if st.session_state.saved_monsters:
                export_data = export_monster_library()
                st.download_button(
                    label="📥 Export Library",
                    data=export_data,
                    file_name=get_monster_library_filename(),
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            # Import library
            uploaded_file = st.file_uploader(
                "📤 Import Library", 
                type=['json'], 
                key="monster_library_upload"
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
        
        # Display saved monsters
        render_saved_monsters()