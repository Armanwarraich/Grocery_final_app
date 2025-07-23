import streamlit as st
import random

def setup_page_config():
    st.set_page_config(
        page_title="🌟 Smart AI Expiry Tracker",
        page_icon="🛍",
        layout="wide"
    )

def apply_theme(theme):
    dark_styles = """
    body {
        background: linear-gradient(135deg, #141e30, #243b55);
        font-family: 'Segoe UI', sans-serif;
    }
    """

    light_styles = """
    body {
        background: linear-gradient(135deg, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
    }
    """

    common_styles = """
    h1 {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #a18cd1; }
        to { text-shadow: 0 0 20px #fbc2eb; }
    }
    .tip, .quote {
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        color: #ffe3ff;
        margin-top: 1rem;
    }
    .login-header {
        font-size: 2.7rem;
        text-align: center;
        font-weight: bold;
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-subheader {
        text-align: center;
        font-style: italic;
        font-size: 1.2rem;
        margin-top: -10px;
        color: #fce3ff;
    }
    .sidebar-content {
        font-size: 1rem;
        color: #ffe3ff;
        padding-bottom: 8px;
        border-bottom: 1px dashed #fff;
        margin-bottom: 10px;
        font-style: italic;
    }
    .badge {
        font-size: 14px;
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, #a18cd1, #fbc2eb);
        color: white;
        margin-bottom: 1rem;
        text-align: center;
        word-break: break-word;
    }
    .logout-button button {
        background: linear-gradient(90deg, #ff758c, #ff7eb3);
        color: white;
        border: none;
        font-size: 16px;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 20px;
        width: 100%;
    }
    .logout-button button:hover {
        box-shadow: 0 4px 15px rgba(255, 150, 200, 0.5);
        transform: scale(1.02);
    }
    """

    theme_css = dark_styles if theme == "dark" else light_styles
    st.markdown(f"<style>{theme_css + common_styles}</style>", unsafe_allow_html=True)

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
