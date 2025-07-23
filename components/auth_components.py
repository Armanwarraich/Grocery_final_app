import streamlit as st
from utils.auth_utils import login_user, register_user, assess_password_strength

def render_auth_section():
    st.markdown("<div class='login-header'>🌟 Smart Expiry Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subheader'>Organize your pantry with AI – Smart, Fast, Magical! 🪄</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.get("show_login", True):
            render_login_form()
        else:
            render_signup_form()
    
    with col2:
        toggle_text = "Sign Up" if st.session_state.get("show_login", True) else "Sign In"
        if st.button(f"🔁 Switch to {toggle_text}", use_container_width=True):
            st.session_state["show_login"] = not st.session_state.get("show_login", True)
            st.rerun()

def render_login_form():
    with st.form("login_form"):
        st.markdown("<h3 style='text-align:center;'>👤 Sign In</h3>", unsafe_allow_html=True)
        email = st.text_input("Email:", key="login_email")
        password = st.text_input("Password:", type="password", key="login_pw")
        
        if st.form_submit_button("🚀 Sign In"):
            if email and password:
                if login_user(email, password):
                    st.session_state["user_email"] = email
                    st.success(f"✅ Welcome back, {email}!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect email or password.")
            else:
                st.error("❌ Please fill in all fields.")

def render_signup_form():
    with st.form("signup_form"):
        st.markdown("<h3 style='text-align:center;'>📝 Create an Account</h3>", unsafe_allow_html=True)
        email = st.text_input("Email:", key="register_email")
        password = st.text_input("Password:", type="password", key="register_pw")
        
        if password:
            strength = assess_password_strength(password)
            st.markdown(f"<div class='sidebar-content'>🔐 Password Strength: <i>{strength}</i></div>", unsafe_allow_html=True)
        
        if st.form_submit_button("🌟 Sign Up Now"):
            if email and password:
                if assess_password_strength(password) == "Strong ✅":
                    if register_user(email, password):
                        st.success("🎉 Registration successful! You can now sign in.")
                        st.session_state["show_login"] = True
                        st.rerun()
                    else:
                        st.error("❌ Email already registered.")
                else:
                    st.warning("⚠ Please use a stronger password.")
            else:
                st.error("❌ Please fill in all fields.")
