import streamlit as st
import mysql.connector
from db import get_db_connection

st.set_page_config(page_title="Incharge Dashboard", layout="wide")

# ✅ Hide Sidebar
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

# ✅ Ensure User is Logged In as Incharge
if "role" not in st.session_state or st.session_state["role"] != "incharge":
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

st.title("🛠️ Incharge Dashboard")

# ✅ Logout Button
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # Clears all session data
    st.success("✅ Logged out successfully!")
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

st.divider()

# ✅ Incharge Job Mapping
incharge_category_map = {
    "plumber": "Water & Sanitation",
    "electrician": "Electrical Issues",
    "network_admin": "Internet & Network",
    "security_officer": "Security Concerns",
    "maintenance_manager": "Faulty Infrastructure",
}

# ✅ Get the Incharge User's Assigned Category
incharge_username = st.session_state["username"]
assigned_category = incharge_category_map.get(incharge_username, None)

if not assigned_category:
    st.error("❌ You are not assigned to any issue category.")
    st.stop()

# ✅ Fetch Reports Assigned to This Incharge
st.header(f"📜 Reports for {assigned_category}")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM reports WHERE category = %s AND status = 'Informed'", (assigned_category,))
reports = cursor.fetchall()
cursor.close()
conn.close()

if not reports:
    st.info("ℹ No reports assigned to you yet.")
else:
    for report in reports:
        st.markdown(f"### 📌 {report['subcategory']} ({report['priority']})")

        # ✅ Status is **BOLD and LARGE**
        st.markdown(
            f"<p style='font-size:28px; font-weight:bold; color:white;'>📝 Status: {report['status']}</p>",
            unsafe_allow_html=True
        )

        # ✅ Reported By **Bigger and Bolder**
        st.markdown(
            f"<p style='font-size:22px; font-weight:bold; color:white;'>📩 Reported by: {report['student_username']}</p>",
            unsafe_allow_html=True
        )

        st.markdown(f"**🔹 Description:** _{report['description']}_")

        # ✅ Show Uploaded Image/Video
        if report["image"]:
            st.image(report["image"], caption="📷 Uploaded Image", use_column_width=True)

        if report["video"]:
            st.video(report["video"])

st.divider()
st.button("🔴 Logout", on_click=logout)  # Logout at the bottom
