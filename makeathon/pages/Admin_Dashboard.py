import streamlit as st
import mysql.connector
from db import get_db_connection

st.set_page_config(page_title="Admin Dashboard", layout="wide")

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

# ✅ Ensure User is Logged In (Redirect to Login Page if Session is Lost)
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

st.title("🛠️ Admin Dashboard")

# ✅ Logout Button
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # Clears all session data
    st.success("✅ Logged out successfully!")
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

st.divider()

# ✅ Show Reports
st.header("📜 Reported Issues")

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM reports")
reports = cursor.fetchall()
cursor.close()
conn.close()

if not reports:
    st.info("ℹ No reports available.")
else:
    for report in reports:
        st.markdown(f"### 📌 {report['category']} ({report['priority']})")

        # ✅ Make status **BOLD and LARGER**
        st.markdown(
            f"<p style='font-size:28px; font-weight:bold; color:white;'>📝 Status: {report['status']}</p>",
            unsafe_allow_html=True
        )

        # ✅ Make "Reported by" **Bigger, Bolder, and White**
        st.markdown(
            f"<p style='font-size:22px; font-weight:bold; color:white;'>📩 Reported by: {report['student_username']}</p>",
            unsafe_allow_html=True
        )

        st.markdown(f"**🔹 Description:** _{report['description']}_")

        # ✅ Show Uploaded Image/Video
        if report["image"]:
            st.image(report["image"], caption="📷 Uploaded Image", use_container_width =True)

        if report["video"]:
            st.video(report["video"])

        # ✅ Admin Status Update
        new_status = st.selectbox(
            f"🔄 Update Status for Report #{report['id']}",
            ["Pending", "In Progress", "Resolved"],
            index=["Pending", "In Progress", "Resolved"].index(report["status"])
        )

        if st.button(f"✅ Update Report #{report['id']}"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reports SET status = %s WHERE id = %s",
                (new_status, report["id"])
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"✅ Report #{report['id']} status updated to {new_status}!")
            st.rerun()

st.divider()
st.button("🔴 Logout", on_click=logout)  # Logout at the bottom
