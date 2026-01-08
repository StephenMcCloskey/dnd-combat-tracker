# src/components/save_load_manager.py
"""Save/load manager UI for combats, rosters, and libraries."""

import streamlit as st
import json
from src.utils.data_manager import (
    get_combat_files, get_player_roster_files, get_monster_library_files,
    save_combat_to_file, load_combat_from_file, delete_combat_file,
    save_player_roster_to_file, load_player_roster_from_file, delete_player_roster_file,
    save_monster_library_to_file, load_monster_library_from_file, delete_monster_library_file,
    format_file_time
)
from src.utils.import_export import (
    export_combat_state, import_combat_state,
    export_player_roster_data, import_player_roster_data,
    export_monster_library, import_monster_library,
    get_export_filename
)


def render_save_load_manager():
    """Render the save/load manager UI."""
    
    st.markdown("#### 💾 Save/Load Manager")
    
    tab1, tab2, tab3 = st.tabs(["⚔️ Combat", "👥 Players", "👹 Monsters"])
    
    with tab1:
        render_combat_save_load()
    
    with tab2:
        render_player_save_load()
    
    with tab3:
        render_monster_save_load()


def render_combat_save_load():
    """Render combat save/load interface."""
    
    st.markdown("##### Current Combat")
    
    if len(st.session_state.get('combatants', [])) > 0:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            save_name = st.text_input(
                "Save as:",
                placeholder="my_encounter",
                key="combat_save_name",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("💾 Save", use_container_width=True, type="primary", key="save_combat_btn"):
                if save_name.strip():
                    combat_data_str = export_combat_state()
                    combat_data = json.loads(combat_data_str)
                    success, message, filepath = save_combat_to_file(combat_data, save_name.strip())
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Enter a name for the save")
        
        st.caption("Or download to your computer:")
        export_data = export_combat_state()
        st.download_button(
            label="📥 Download Combat",
            data=export_data,
            file_name=get_export_filename(),
            mime="application/json",
            use_container_width=True,
            key="download_combat_btn"
        )
    else:
        st.info("Add combatants to save a combat")
    
    st.markdown("---")
    st.markdown("##### Saved Combats")
    
    combat_files = get_combat_files()
    
    if combat_files:
        for filepath in combat_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.caption(f"📄 **{filepath.stem}** - {format_file_time(filepath)}")
            
            with col2:
                if st.button("📂", key=f"load_combat_{filepath.stem}", help="Load"):
                    success, message, data = load_combat_from_file(filepath)
                    if success:
                        json_str = json.dumps(data)
                        success, message = import_combat_state(json_str)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(message)
            
            with col3:
                if st.button("🗑️", key=f"delete_combat_{filepath.stem}", help="Delete"):
                    success, message = delete_combat_file(filepath)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.caption("No saved combats yet")
    
    st.markdown("---")
    st.caption("Or upload from your computer:")
    uploaded_file = st.file_uploader(
        "Upload Combat",
        type=['json'],
        key="upload_combat_file",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            json_str = uploaded_file.read().decode('utf-8')
            success, message = import_combat_state(json_str)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_player_save_load():
    """Render player roster save/load interface."""
    
    st.markdown("##### Current Roster")
    
    if st.session_state.get('player_roster'):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            save_name = st.text_input(
                "Save as:",
                placeholder="my_party",
                key="roster_save_name",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("💾 Save", use_container_width=True, type="primary", key="save_roster_btn"):
                if save_name.strip():
                    roster_data_str = export_player_roster_data()
                    roster_data = json.loads(roster_data_str)
                    success, message, filepath = save_player_roster_to_file(roster_data, save_name.strip())
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Enter a name for the save")
        
        st.caption("Or download to your computer:")
        export_data = export_player_roster_data()
        st.download_button(
            label="📥 Download Roster",
            data=export_data,
            file_name=f"dnd_players_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            key="download_roster_btn"
        )
    else:
        st.info("Add players to save a roster")
    
    st.markdown("---")
    st.markdown("##### Saved Rosters")
    
    roster_files = get_player_roster_files()
    
    if roster_files:
        for filepath in roster_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.caption(f"👥 **{filepath.stem}** - {format_file_time(filepath)}")
            
            with col2:
                if st.button("📂", key=f"load_roster_{filepath.stem}", help="Load"):
                    success, message, data = load_player_roster_from_file(filepath)
                    if success:
                        json_str = json.dumps(data)
                        success, message = import_player_roster_data(json_str)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(message)
            
            with col3:
                if st.button("🗑️", key=f"delete_roster_{filepath.stem}", help="Delete"):
                    success, message = delete_player_roster_file(filepath)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.caption("No saved rosters yet")
    
    st.markdown("---")
    st.caption("Or upload from your computer:")
    uploaded_file = st.file_uploader(
        "Upload Roster",
        type=['json'],
        key="upload_roster_file",
        label_visibility="collapsed"
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
            st.error(f"Error: {str(e)}")


def render_monster_save_load():
    """Render monster library save/load interface."""
    
    st.markdown("##### Current Library")
    
    if st.session_state.get('saved_monsters'):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            save_name = st.text_input(
                "Save as:",
                placeholder="my_monsters",
                key="library_save_name",
                label_visibility="collapsed"
            )
        
        with col2:
            if st.button("💾 Save", use_container_width=True, type="primary", key="save_library_btn"):
                if save_name.strip():
                    library_data_str = export_monster_library()
                    library_data = json.loads(library_data_str)
                    success, message, filepath = save_monster_library_to_file(library_data, save_name.strip())
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Enter a name for the save")
        
        st.caption("Or download to your computer:")
        export_data = export_monster_library()
        st.download_button(
            label="📥 Download Library",
            data=export_data,
            file_name=f"dnd_monsters_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            key="download_library_btn"
        )
    else:
        st.info("Add monsters to save a library")
    
    st.markdown("---")
    st.markdown("##### Saved Libraries")
    
    library_files = get_monster_library_files()
    
    if library_files:
        for filepath in library_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.caption(f"👹 **{filepath.stem}** - {format_file_time(filepath)}")
            
            with col2:
                if st.button("📂", key=f"load_library_{filepath.stem}", help="Load"):
                    success, message, data = load_monster_library_from_file(filepath)
                    if success:
                        json_str = json.dumps(data)
                        success, message = import_monster_library(json_str)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(message)
            
            with col3:
                if st.button("🗑️", key=f"delete_library_{filepath.stem}", help="Delete"):
                    success, message = delete_monster_library_file(filepath)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.caption("No saved libraries yet")
    
    st.markdown("---")
    st.caption("Or upload from your computer:")
    uploaded_file = st.file_uploader(
        "Upload Library",
        type=['json'],
        key="upload_library_file",
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
            st.error(f"Error: {str(e)}")