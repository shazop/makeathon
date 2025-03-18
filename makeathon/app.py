import streamlit as st
import os
from db import authenticate_user, initialize_database

st.set_page_config(page_title="SBMS Login", layout="centered")

# ✅ Initialize Database
initialize_database()

# ✅ Ensure session variables exist
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# ✅ Compute Correct Paths Using `os.path.relpath()`
admin_dashboard_path = os.path.relpath("pages/Admin_Dashboard.py")
student_dashboard_path = os.path.relpath("pages/Student_Dashboard.py")

# ✅ Redirect logged-in users dynamically
if st.session_state["role"] == "admin":
    st.switch_page(admin_dashboard_path)
elif st.session_state["role"] == "student":
    st.switch_page(student_dashboard_path)

# ✅ Login UI
st.title("🏫 Smart Building Management System")

username = st.text_input("👤 Username")
password = st.text_input("🔒 Password", type="password")

if st.button("🔑 Login"):
    user = authenticate_user(username, password)
    
    if user:
        st.session_state["username"] = user["username"]
        st.session_state["role"] = user["role"]

        if user["role"] == "admin":
            st.success("✅ Login Successful! Redirecting to Admin Dashboard...")
            st.switch_page(admin_dashboard_path)
        elif user["role"] == "student":
            st.success("✅ Login Successful! Redirecting to Student Dashboard...")
            st.switch_page(student_dashboard_path)
    else:
        st.error("❌ Invalid credentials. Please try again.")
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)