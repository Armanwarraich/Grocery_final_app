import streamlit as st
from utils.auth_utils import login_user, register_user, assess_password_strength

def render_auth_section():
    # Vertical spacing
    st.markdown("<div style='height:6vh;'></div>", unsafe_allow_html=True)
    
    # App title
    st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1 style='color: #1a73e8; font-size: 2.5rem; margin-bottom: 8px; font-weight: 600;'>
                🛍️ Smart Expiry Tracker
            </h1>
            <p style='color: #5f6368; font-size: 1.1rem; margin: 0;'>
                Organize your pantry with AI
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the form (no white box)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # Tab buttons
        mode = st.session_state.get("auth_mode", "login")
        tab_col1, tab_col2 = st.columns([1, 1])
        with tab_col1:
            if st.button("Sign In", use_container_width=True, key="login_tab"):
                st.session_state["auth_mode"] = "login"
                st.rerun()
        with tab_col2:
            if st.button("Create Account", use_container_width=True, key="signup_tab"):
                st.session_state["auth_mode"] = "signup"
                st.rerun()

        st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)

        # Forms
        if mode == "login":
            render_login_form()
        else:
            render_signup_form()

def render_login_form():
    with st.form("login_form"):
        st.markdown("<h3 style='color: #202124; text-align: center; margin-bottom: 24px;'>Sign in to your account</h3>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("Sign In", use_container_width=True):
                if email and password:
                    if login_user(email, password):
                        st.session_state["user_email"] = email
                        st.success("✅ Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.error("❌ Please fill all fields")

def render_signup_form():
    with st.form("signup_form"):
        st.markdown("<h3 style='color: #202124; text-align: center; margin-bottom: 24px;'>Create your account</h3>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Create a password", type="password")
        
        if password:
            strength = assess_password_strength(password)
            st.markdown(f"<small style='color: #5f6368;'>🔐 Password strength: {strength}</small>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("Create Account", use_container_width=True):
                if email and password:
                    if "Strong" in assess_password_strength(password):
                        if register_user(email, password):
                            st.success("🎉 Account created!")
                            st.session_state["auth_mode"] = "login"
                            st.rerun()
                        else:
                            st.error("❌ Email already registered")
                    else:
                        st.warning("⚠️ Use a stronger password")
                else:
                    st.error("❌ Please fill all fields")
