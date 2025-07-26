import streamlit as st
import random

def setup_page_config():
    st.set_page_config(
        page_title="🌟 Smart AI Expiry Tracker",
        page_icon="🛍",
        layout="wide"
    )

def apply_theme(theme):
    if theme == "dark":
        theme_styles = """
        .stApp {
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
            color: #ffffff !important;
        }
        .stSidebar {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #ffffff !important;
            background: rgba(255,255,255,0.1) !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        .stMetric {
            background: rgba(30,30,50,0.8) !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        .stMetric [data-testid="metric-container"] {
            background: rgba(30,30,50,0.8) !important;
            color: #ffffff !important;
        }
        .stMetric [data-testid="metric-container"] > div {
            color: #ffffff !important;
        }
        .stMetric label {
            color: #ffffff !important;
        }
        .stMetric [data-testid="metric-container"] [data-testid="metric-value"] {
            color: #ffffff !important;
        }
        .stRadio > div {
            background: rgba(255,255,255,0.15) !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }
        .stRadio > div > label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        .stRadio > div > label > div {
            color: #ffffff !important;
        }
        .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
            color: #ffffff !important;
        }
        .stRadio > div > label > div[data-testid="stMarkdownContainer"] p {
            color: #ffffff !important;
        }
        """
    else:  # light theme
        theme_styles = """
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
            color: #333333 !important;
        }
        .stSidebar {
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(0,0,0,0.05) !important;
            border-radius: 10px !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #333333 !important;
            background: rgba(255,255,255,0.8) !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        .stMetric {
            background: rgba(255,255,255,0.8) !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        }
        .stMetric [data-testid="metric-container"] {
            background: rgba(255,255,255,0.8) !important;
            color: #333333 !important;
        }
        .stMetric [data-testid="metric-container"] > div {
            color: #333333 !important;
        }
        .stMetric label {
            color: #333333 !important;
        }
        .stMetric [data-testid="metric-container"] [data-testid="metric-value"] {
            color: #333333 !important;
        }
        .stRadio > div {
            background: rgba(102, 126, 234, 0.1) !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
        }
        .stRadio > div > label {
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        .stRadio > div > label > div {
            color: #333333 !important;
        }
        .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
            color: #333333 !important;
        }
        .stRadio > div > label > div[data-testid="stMarkdownContainer"] p {
            color: #333333 !important;
        }
        """

    common_styles = """
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    h1 {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    h3 {
        color: inherit !important;
    }
    
    @keyframes glow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }
    
    .tip, .quote {
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin: 1rem 0;
        padding: 15px;
        border-radius: 10px;
        background: rgba(102, 126, 234, 0.15);
        border-left: 4px solid #667eea;
        color: inherit;
    }
    
    .login-header {
        font-size: 2.7rem;
        text-align: center;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .login-subheader {
        text-align: center;
        font-style: italic;
        font-size: 1.2rem;
        margin-top: -10px;
        opacity: 0.8;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        transition: all 0.3s ease !important;
        padding: 12px 30px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 12px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333333 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
    }
    
    .stTextInput label {
        color: inherit !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333333 !important;
    }
    
    .stSelectbox label {
        color: inherit !important;
        font-weight: 600 !important;
    }
    
    .stForm {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        color: #333333 !important;
    }
    
    .stForm h3 {
        color: #333333 !important;
    }
    
    .stForm label {
        color: #333333 !important;
    }
    
    .stForm [data-testid="stMarkdownContainer"] {
        color: #333333 !important;
    }
    
    /* Fix file uploader visibility */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        border: 2px dashed rgba(102, 126, 234, 0.3) !important;
    }
    
    .stFileUploader label {
        color: inherit !important;
        font-weight: 600 !important;
    }
    """

    st.markdown(f"<style>{theme_styles + common_styles}</style>", unsafe_allow_html=True)

def get_daily_content():
    tips = [
        "🥕 Store carrots in water for longer freshness.",
        "🥛 Keep milk in the coldest part of the fridge.",
        "🍞 Freeze bread slices to make them last longer.",
        "🥦 Wrap broccoli in foil to keep it crisp.",
        "🍓 Rinse berries with vinegar water to preserve them.",
        "🧀 Keep cheese in parchment, not plastic!"
    ]
    quotes = [
        "\"Fresh is best\" 🥬",
        "\"Waste not, want not\" 🌍",
        "\"Good food is worth preserving\" 🍱",
        "\"Smart tracking saves smart money\" 💰",
        "\"Track today, save tomorrow\" 📆"
    ]
    
    st.markdown(f"<div class='tip'>💡 Tip of the Day: <i>{random.choice(tips)}</i></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='quote'>🌟 Quote of the Day: <i>{random.choice(quotes)}</i></div>", unsafe_allow_html=True)
