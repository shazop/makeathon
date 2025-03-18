import streamlit as st
import os
import mysql.connector
from db import get_db_connection

st.set_page_config(page_title="My Reports", layout="wide")

# ✅ Ensure User is Logged In
if "role" not in st.session_state or st.session_state["role"] != "student":
    st.error("❌ Access Denied. Please log in as a student.")
    st.stop()

st.title("📜 My Reported Issues")

# 🔘 Button to Report a New Issue
path_dashboard = os.path.relpath("pages/Student_Dashboard.py")  # ✅ Correct linking
st.write(f"🔗 Debug Path: {path_dashboard}")  # Debugging path (remove after testing)

if st.button("📝 Report a New Issue"):
    st.switch_page(path_dashboard)  # ✅ Uses correct navigation

st.page_link(path_dashboard)  # ✅ Clickable page link for navigation

st.divider()

# ✅ Fetch and Display User Reports
conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT * FROM reports WHERE student_username = %s", (st.session_state["username"],))
reports = cursor.fetchall()

cursor.close()
conn.close()

if not reports:
    st.info("ℹ No reports found. Submit an issue from the Student Dashboard.")
else:
    for report in reports:
        st.subheader(f"📌 {report['category']} ({report['priority']})")
        st.text(f"📝 Description: {report['description']}")
        st.text(f"📌 Status: {report['status']}")
        st.text(f"📩 Reported by: {report['student_username']}")

        if report["image"]:
            st.image(report["image"], caption="📷 Uploaded Image", use_column_width=True)

        if report["video"]:
            st.video(report["video"])
