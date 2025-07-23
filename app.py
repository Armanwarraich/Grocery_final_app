import streamlit as st
from datetime import datetime
from components.auth_components import render_auth_section
from components.product_manager import render_products_tab, render_add_item_tab, render_recycle_bin_tab
from components.insights_ui import render_insights_tab, render_alerts_tab
from utils.database import get_user_products
from utils.helpers import get_status_counts, apply_theme
from config.theme import setup_page_config, get_daily_content

# Page config
setup_page_config()

# Initialize session state
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

def main():
    apply_theme(st.session_state["theme"])
    
    # Authentication check
    if not st.session_state.get("user_email"):
        render_auth_section()
        return
    
    render_dashboard()

def render_dashboard():
    # Header with logout
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🔓 Log Out", use_container_width=True):
            st.session_state["user_email"] = None
            st.rerun()
    
    # Title and subtitle
    st.markdown("<h1>🛍 Smart AI Grocery Expiry Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<div class='login-subheader'>Track today, save tomorrow. Make AI your pantry pal. 🧠</div>", unsafe_allow_html=True)
    
    # Get user products and metrics
    products = get_user_products(st.session_state["user_email"])
    expired, soon, fresh = get_status_counts(products)
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("⏳ Expired Items", expired)
    c2.metric("⚡ Expiring Soon (3d)", soon)
    c3.metric("🌱 Fresh Items", fresh)
    
    # Daily content
    get_daily_content()
    
    # Sidebar
    render_sidebar(products, expired, soon, fresh)
    
    # Main tabs
    render_main_tabs(products)

def render_sidebar(products, expired, soon, fresh):
    with st.sidebar:
        st.markdown(f"<div class='badge'>👤 Logged in as:<br>{st.session_state['user_email']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='sidebar-content'>❗ Expired Items: <b>{expired}</b></div>
        <div class='sidebar-content'>⚡ Expiring Soon: <b>{soon}</b></div>
        <div class='sidebar-content'>🌱 Fresh Items: <b>{fresh}</b></div>
        """, unsafe_allow_html=True)
        
        # Theme selector
        theme_choice = st.radio("🌙☀ Theme:", ["dark", "light"], 
                               index=0 if st.session_state["theme"] == "dark" else 1)
        if theme_choice != st.session_state["theme"]:
            st.session_state["theme"] = theme_choice
            st.rerun()

def render_main_tabs(products):
    tabs = st.tabs(["📋 Products", "➕ Add Item", "📊 Insights", "⚡ Alerts", "♻ Recycle Bin"])
    
    with tabs[0]:
        render_products_tab(products)
    with tabs[1]:
        render_add_item_tab()
    with tabs[2]:
        render_insights_tab(products)
    with tabs[3]:
        render_alerts_tab(products)
    with tabs[4]:
        render_recycle_bin_tab()

if __name__ == "__main__":
    main()
