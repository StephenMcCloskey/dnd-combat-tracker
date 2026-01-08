# src/styles/components.py
"""Component-specific styles."""


def get_component_styles() -> str:
    """Return CSS for various UI components."""
    return """
<style>
    /* =========================================================================
       Combatant Cards
       ========================================================================= */
    .combatant-card {
        background-color: #FFFFFF;
        border: 2px solid #8B0000;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .combatant-card-active {
        background-color: #f0fff0;
        border: 3px solid #228B22;
        box-shadow: 0 0 10px rgba(34, 139, 34, 0.3);
    }
    
    .combatant-card-dead {
        background-color: #f5f5f5;
        border: 2px solid #666;
        opacity: 0.7;
    }
    
    /* =========================================================================
       HP Bar Colors
       ========================================================================= */
    .hp-full {
        background-color: #4CAF50;
    }
    
    .hp-injured {
        background-color: #FF9800;
    }
    
    .hp-critical {
        background-color: #f44336;
    }
    
    .hp-dead {
        background-color: #9E9E9E;
    }
    
    /* =========================================================================
       Condition Tags
       ========================================================================= */
    .condition-tag {
        display: inline-block;
        background-color: #FFE4E1;
        color: #8B0000;
        padding: 0.15rem 0.4rem;
        border-radius: 3px;
        margin: 0.1rem;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .condition-tag-severe {
        background-color: #FFCDD2;
        border: 1px solid #f44336;
    }
    
    /* =========================================================================
       Death Save Indicators
       ========================================================================= */
    .death-save-success {
        color: #4CAF50;
        font-size: 1.2rem;
    }
    
    .death-save-failure {
        color: #f44336;
        font-size: 1.2rem;
    }
    
    .death-save-empty {
        color: #BDBDBD;
        font-size: 1.2rem;
    }
    
    /* =========================================================================
       Quick Action Buttons
       ========================================================================= */
    .quick-action-btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.85rem;
        min-height: 2rem;
    }
    
    /* =========================================================================
       Empty State
       ========================================================================= */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background-color: rgba(139, 0, 0, 0.1);
        border: 2px dashed #8B0000;
        border-radius: 10px;
        margin: 2rem auto;
        max-width: 800px;
    }
    
    .empty-state h2 {
        color: #8B0000;
        margin-bottom: 1rem;
        font-size: clamp(1.5rem, 4vw, 2rem);
    }
    
    .empty-state p {
        color: #5a4a42;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        margin-bottom: 2rem;
    }
    
    .empty-state-card {
        padding: 1rem;
        background-color: rgba(0,0,0,0.05);
        border-radius: 5px;
        text-align: center;
    }
    
    .empty-state-card strong {
        color: #8B0000;
        font-size: clamp(0.9rem, 2vw, 1rem);
    }
    
    .empty-state-card span {
        color: #5a4a42;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
    }
    
    /* =========================================================================
       Tab Styling
       ========================================================================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #3a2820;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        border: 2px solid #8B0000;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 4px;
        color: #f8f5f0;
        font-weight: 500;
        padding: 0.6rem 1.5rem;
        min-width: 100px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(139, 0, 0, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8B0000 !important;
        color: #FFD700 !important;
    }
    
    /* Tab content area */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    
    /* =========================================================================
       View Mode Toggle
       ========================================================================= */
    .view-mode-btn {
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .view-mode-active {
        background-color: #8B0000;
        color: #FFD700;
        border: 2px solid #FFD700;
    }
    
    .view-mode-inactive {
        background-color: rgba(139, 0, 0, 0.2);
        color: #8B0000;
        border: 1px solid #8B0000;
    }
    
    /* =========================================================================
       Combat Overview Dashboard
       ========================================================================= */
    .dashboard-stat {
        background-color: #FFFFFF;
        border: 2px solid #8B0000;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
    }
    
    .dashboard-stat-label {
        color: #8B0000;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .dashboard-stat-value {
        color: #2C1810;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* =========================================================================
       Reference Cards
       ========================================================================= */
    .reference-card {
        background-color: #FFFFF0;
        border: 1px solid #D4AF37;
        border-radius: 4px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }
    
    .reference-card-title {
        color: #8B0000;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    
    .reference-card-content {
        color: #5a4a42;
        font-size: 0.85rem;
        white-space: pre-line;
    }
    
    /* =========================================================================
       Tooltips
       ========================================================================= */
    .tooltip {
        position: relative;
        cursor: help;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #2C1810;
        color: #f8f5f0;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 1000;
    }
</style>
"""