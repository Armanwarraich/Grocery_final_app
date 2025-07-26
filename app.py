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
    
    # Metrics with better styling for dark theme
    c1, c2, c3 = st.columns(3)
    
    # Use custom styled metrics that work better with themes
    with c1:
        st.markdown(f"""
            <div style='background: rgba(255, 107, 107, 0.9); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);'>
                <div style='font-size: 0.95rem; font-weight: 600; margin-bottom: 8px;'>⏳ Expired Items</div>
                <div style='font-size: 2.2rem; font-weight: bold;'>{expired}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
            <div style='background: rgba(255, 167, 38, 0.9); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(255, 167, 38, 0.3);'>
                <div style='font-size: 0.95rem; font-weight: 600; margin-bottom: 8px;'>⚡ Expiring Soon (3d)</div>
                <div style='font-size: 2.2rem; font-weight: bold;'>{soon}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
            <div style='background: rgba(102, 187, 106, 0.9); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        text-align: center;
                        box-shadow: 0 4px 15px rgba(102, 187, 106, 0.3);'>
                <div style='font-size: 0.95rem; font-weight: 600; margin-bottom: 8px;'>🌱 Fresh Items</div>
                <div style='font-size: 2.2rem; font-weight: bold;'>{fresh}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Daily content
    get_daily_content()
    
    # Sidebar
    render_sidebar(products, expired, soon, fresh)
    
    # Main tabs
    render_main_tabs(products)


def render_sidebar(products, expired, soon, fresh):
    with st.sidebar:
        # User info with bigger styling
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        margin-bottom: 25px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='font-size: 1.2rem; font-weight: 600; margin-bottom: 8px;'>👤 Logged in as:</div>
                <div style='font-size: 0.9rem; word-break: break-word;'>{st.session_state['user_email']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Stats boxes with bigger styling
        st.markdown(f"""
            <div style='margin-bottom: 20px;'>
                <div style='background: #ff6b6b; color: white; padding: 15px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 3px 10px rgba(255,107,107,0.3);'>
                    <div style='font-size: 1.1rem; font-weight: 600;'>❗ Expired Items</div>
                    <div style='font-size: 1.8rem; font-weight: bold; margin-top: 5px;'>{expired}</div>
                </div>
                <div style='background: #ffa726; color: white; padding: 15px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 3px 10px rgba(255,167,38,0.3);'>
                    <div style='font-size: 1.1rem; font-weight: 600;'>⚡ Expiring Soon</div>
                    <div style='font-size: 1.8rem; font-weight: bold; margin-top: 5px;'>{soon}</div>
                </div>
                <div style='background: #66bb6a; color: white; padding: 15px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 3px 10px rgba(102,187,106,0.3);'>
                    <div style='font-size: 1.1rem; font-weight: 600;'>🌱 Fresh Items</div>
                    <div style='font-size: 1.8rem; font-weight: bold; margin-top: 5px;'>{fresh}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Theme selector with bigger styling
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        color: white;
                        padding: 18px;
                        border-radius: 15px;
                        text-align: center;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;'>🌙☀ Theme</div>
            </div>
        """, unsafe_allow_html=True)
        
        theme_choice = st.radio("", ["🌙 Dark", "☀ Light"], 
                               index=0 if st.session_state["theme"] == "dark" else 1,
                               label_visibility="collapsed")
        
        # Update theme
        new_theme = "dark" if "Dark" in theme_choice else "light"
        if new_theme != st.session_state["theme"]:
            st.session_state["theme"] = new_theme
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