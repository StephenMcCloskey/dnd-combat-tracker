# src/styles/header.py
"""Sticky header styles."""


def get_header_styles() -> str:
    """Return CSS for sticky header."""
    return """
<style>
    /* =========================================================================
       Sticky Header - Target Streamlit's DOM structure
       ========================================================================= */
    
    /* Make the first block container element sticky */
    .main .block-container > div:first-child {
        position: sticky;
        top: 0;
        z-index: 999;
        background: linear-gradient(to bottom, #2C1810 0%, #3a2518 100%);
        padding: 0.75rem 1rem;
        margin: -1rem -2rem 0 -2rem;
        border-bottom: 3px solid #8B0000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    /* Ensure metrics in header have dark theme */
    .main .block-container > div:first-child [data-testid="stMetric"] {
        background-color: #3a2820 !important;
        border: 1px solid #8B0000 !important;
        padding: 0.5rem !important;
    }
    
    .main .block-container > div:first-child [data-testid="stMetricLabel"] {
        color: #FFD700 !important;
    }
    
    .main .block-container > div:first-child [data-testid="stMetricValue"] {
        color: #f8f5f0 !important;
    }
    
    /* Header buttons */
    .main .block-container > div:first-child .stButton > button {
        background-color: #8B0000;
        color: #f8f5f0;
        border: 2px solid #FFD700;
    }
    
    .main .block-container > div:first-child .stButton > button:hover {
        background-color: #A52A2A;
        border-color: #FFA500;
    }
    
    .main .block-container > div:first-child .stButton > button[kind="primary"] {
        background-color: #228B22;
        border-color: #32CD32;
    }
    
    .main .block-container > div:first-child .stButton > button:disabled {
        background-color: #4a3830;
        border-color: #666;
        opacity: 0.5;
    }
    
    /* Divider in header */
    .main .block-container > div:first-child hr {
        border-color: #8B0000;
        margin: 0.5rem 0 !important;
    }
    
    /* =========================================================================
       Header Title
       ========================================================================= */
    .header-title {
        color: #FFD700 !important;
        font-size: clamp(1rem, 2vw, 1.5rem) !important;
        font-weight: bold !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Override any h1 in header area */
    .main .block-container > div:first-child h1 {
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Text in header should be light */
    .main .block-container > div:first-child p,
    .main .block-container > div:first-child span,
    .main .block-container > div:first-child label {
        color: #f8f5f0 !important;
    }
    
    /* =========================================================================
       Active Turn Indicator
       ========================================================================= */
    .active-turn {
        background-color: #90EE90;
        padding: 0.4rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        font-size: clamp(0.7rem, 1.3vw, 1rem) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    .active-turn-death {
        background-color: #8B0000;
        color: #FFD700;
        padding: 0.4rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        font-size: clamp(0.7rem, 1.3vw, 1rem) !important;
        white-space: nowrap !important;
    }
    
    /* =========================================================================
       Combat Status Badges
       ========================================================================= */
    .combat-status {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        white-space: nowrap;
    }
    
    .combat-active {
        background-color: #2E8B57;
        color: #90EE90;
        border: 2px solid #32CD32;
    }
    
    .combat-inactive {
        background-color: #8B4513;
        color: #FFE4B5;
        border: 2px solid #D2691E;
    }
    
    /* =========================================================================
       Header Quick Stats
       ========================================================================= */
    .header-stat {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin: 0 0.25rem;
        background-color: #3a2820;
        border: 1px solid #8B0000;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        color: #f8f5f0;
    }
    
    .header-stat-label {
        color: #FFD700;
        font-size: 0.75rem;
    }
    
    .header-stat-value {
        color: #f8f5f0;
        font-weight: bold;
    }
    
    /* =========================================================================
       Header Buttons
       ========================================================================= */
    .sticky-header .stButton > button {
        font-size: clamp(0.65rem, 1vw, 0.9rem) !important;
        white-space: nowrap !important;
        padding: 0.3rem 0.5rem !important;
        min-height: 2.2rem;
    }
    
    /* =========================================================================
       Round/Turn Display
       ========================================================================= */
    .round-display {
        background-color: #8B0000;
        color: #FFD700;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.9rem;
        text-align: center;
    }
</style>
"""