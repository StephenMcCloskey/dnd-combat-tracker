# src/styles/main.py
"""Main content area styles."""


def get_main_styles() -> str:
    """Return CSS for main content area."""
    return """
<style>
    /* =========================================================================
       App Background
       ========================================================================= */
    .stApp {
        background: linear-gradient(to bottom, #2C1810 0%, #1a0f0a 100%);
    }
    
    /* Remove default top padding that causes white gap */
    .stApp > header {
        background: transparent;
    }
    
    .stMainBlockContainer {
        padding-top: 0 !important;
    }
    
    /* =========================================================================
       Main Content Container
       ========================================================================= */
    .main .block-container {
        background-color: #f8f5f0;
        border-radius: 0 0 10px 10px;
        padding: 1rem 2rem 2rem 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* =========================================================================
       Typography
       ========================================================================= */
    .main h1 {
        color: #8B0000;
        text-align: center;
        padding: 0.5rem 0;
        border-bottom: 3px solid #8B0000;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-size: clamp(1.2rem, 2.5vw, 2rem) !important;
    }
    
    .main h2 {
        color: #8B0000;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main h3 {
        color: #8B0000;
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }
    
    /* =========================================================================
       Metrics
       ========================================================================= */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #2C1810 !important;
    }
    
    .main [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #8B0000;
    }
    
    .main [data-testid="stMetricLabel"] {
        color: #8B0000 !important;
        font-weight: bold;
    }
    
    .main [data-testid="stMetricValue"] {
        color: #2C1810 !important;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    /* =========================================================================
       Buttons
       ========================================================================= */
    .stButton > button {
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="secondary"] {
        background-color: rgba(139, 0, 0, 0.3);
        border: 1px solid #8B0000;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: rgba(139, 0, 0, 0.5);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="primary"] {
        background-color: #8B0000;
        border: 2px solid #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    /* =========================================================================
       Expanders
       ========================================================================= */
    .streamlit-expanderHeader {
        background-color: #f0e6d2;
        border-radius: 5px;
        border: 2px solid #8B0000;
        padding: 0.35rem 1rem !important;
        min-height: 2.5rem !important;
    }
    
    .streamlit-expanderContent {
        padding: 0.5rem 1rem !important;
    }
    
    .main [data-testid="stExpander"] {
        margin-bottom: 0.15rem !important;
    }
    
    .streamlit-expanderHeader p {
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    /* =========================================================================
       Dividers and Spacing
       ========================================================================= */
    .main hr {
        margin: 0.25rem 0 !important;
    }
    
    .main .block-container > div > div > div > div {
        margin-bottom: 0.15rem !important;
    }
    
    .main > div > div > div > div {
        margin-bottom: 0.5rem;
    }
    
    /* =========================================================================
       Columns
       ========================================================================= */
    .main [data-testid="column"] {
        padding: 0.15rem !important;
        min-width: 0 !important;
        flex-shrink: 1 !important;
    }
    
    /* =========================================================================
       Inputs
       ========================================================================= */
    .main [data-testid="stNumberInput"] input {
        text-align: center;
        font-size: 0.9rem;
    }
    
    /* =========================================================================
       Code/Tags
       ========================================================================= */
    code {
        background-color: #FFE4E1;
        color: #8B0000;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        margin: 0.1rem;
    }
    
    /* =========================================================================
       Progress Bars (HP)
       ========================================================================= */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
"""