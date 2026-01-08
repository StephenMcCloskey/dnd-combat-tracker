# src/styles/sidebar.py
"""Sidebar styles."""


def get_sidebar_styles() -> str:
    """Return CSS for sidebar."""
    return """
<style>
    /* =========================================================================
       Sidebar Container
       ========================================================================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #2C1810 0%, #1a0f0a 100%);
        border-right: 3px solid #8B0000;
        overflow-y: auto;
        overflow-x: hidden;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        overflow-x: hidden;
    }
    
    /* =========================================================================
       Sidebar Typography
       ========================================================================= */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFD700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        word-wrap: break-word;
    }
    
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {
        color: #f8f5f0 !important;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #8B0000;
    }
    
    /* =========================================================================
       Sidebar Buttons
       ========================================================================= */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #8B0000;
        color: white;
        border: 2px solid #FFD700;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #A52A2A;
        border-color: #FFA500;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #228B22;
        border-color: #32CD32;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #2E8B57;
    }
    
    /* =========================================================================
       Sidebar Inputs
       ========================================================================= */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] textarea {
        background-color: #3a2820;
        color: #f8f5f0;
        border: 1px solid #8B0000;
        max-width: 100%;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #3a2820;
        color: #f8f5f0;
        border: 1px solid #8B0000;
    }
    
    /* =========================================================================
       Sidebar Metrics
       ========================================================================= */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: #3a2820;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #8B0000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #FFD700 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #f8f5f0 !important;
    }
    
    /* =========================================================================
       Sidebar File Uploader
       ========================================================================= */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #3a2820;
        border: 2px dashed #8B0000;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* =========================================================================
       Combat Log Container
       ========================================================================= */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(.stTextArea) {
        background-color: #1a1410;
        border: 2px solid #8B0000;
        border-radius: 8px;
        padding: 0.5rem;
    }
</style>
"""