import streamlit as st

def render_conditions_reference():
    """Render a quick reference guide for conditions"""
    
    conditions_info = {
        "Blinded": "• Can't see, auto-fails sight checks\n• Attacks have disadvantage\n• Attacks against have advantage",
        "Charmed": "• Can't attack charmer\n• Charmer has advantage on social checks",
        "Deafened": "• Can't hear, auto-fails hearing checks",
        "Frightened": "• Disadvantage on checks/attacks while source in sight\n• Can't move closer to source",
        "Grappled": "• Speed becomes 0\n• Ends if grappler incapacitated",
        "Incapacitated": "• Can't take actions or reactions",
        "Invisible": "• Impossible to see without special senses\n• Attacks have advantage\n• Attacks against have disadvantage",
        "Paralyzed": "• Incapacitated, can't move or speak\n• Auto-fail STR/DEX saves\n• Attacks have advantage\n• Hits from within 5ft are crits",
        "Petrified": "• Turned to stone, incapacitated\n• Can't move or speak\n• Auto-fail STR/DEX saves\n• Attacks have advantage\n• Resistance to all damage\n• Immune to poison/disease",
        "Poisoned": "• Disadvantage on attacks and ability checks",
        "Prone": "• Disadvantage on attacks\n• Melee attacks against have advantage\n• Ranged attacks against have disadvantage\n• Costs half movement to stand",
        "Restrained": "• Speed becomes 0\n• Attacks have disadvantage\n• Attacks against have advantage\n• Disadvantage on DEX saves",
        "Stunned": "• Incapacitated, can't move\n• Can speak only falteringly\n• Auto-fail STR/DEX saves\n• Attacks have advantage",
        "Unconscious": "• Incapacitated, can't move/speak\n• Unaware of surroundings\n• Drops held items, falls prone\n• Auto-fail STR/DEX saves\n• Attacks have advantage\n• Hits from within 5ft are crits"
    }
    
    exhaustion_info = """
**Level 1:** Disadvantage on ability checks
**Level 2:** Speed halved
**Level 3:** Disadvantage on attack rolls and saving throws
**Level 4:** HP maximum halved
**Level 5:** Speed reduced to 0
**Level 6:** Death

*Effects are cumulative. Long rest removes 1 level (with food/drink).*
"""
    
    with st.expander("📖 Conditions Quick Reference"):
        tab1, tab2 = st.tabs(["Conditions", "Exhaustion"])
        
        with tab1:
            for condition, effect in conditions_info.items():
                st.markdown(f"**{condition}**")
                st.text(effect)
                st.markdown("")
        
        with tab2:
            st.markdown(exhaustion_info)