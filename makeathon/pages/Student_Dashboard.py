import streamlit as st
import mysql.connector
from db import get_db_connection

st.set_page_config(page_title="Student Dashboard", layout="wide")

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
if "role" not in st.session_state or st.session_state["role"] != "student":
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

st.title("📌 Student Dashboard")

# ✅ Logout Button
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # Clears all session data
    st.success("✅ Logged out successfully!")
    st.switch_page("app.py")  # 🔄 Redirect to Login Page

# ✅ Toggle between "Report an Issue" & "View My Reports"
if "show_reports" not in st.session_state:
    st.session_state["show_reports"] = False  # Default: Show issue reporting

if st.session_state["show_reports"]:
    if st.button("📝 Report a New Issue"):
        st.session_state["show_reports"] = False  # Switch back to reporting mode
        st.rerun()
else:
    if st.button("📜 View My Reports"):
        st.session_state["show_reports"] = True  # Show reports after clicking
        st.rerun()

st.divider()  # UI Separator

# ✅ **Show Reports if `show_reports` is True**
if st.session_state["show_reports"]:
    st.header("📜 My Reported Issues")

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
            st.markdown(f"### 📌 {report['category']} ({report['priority']})")
            
            # ✅ Make status **BOLD and LARGER**
            st.markdown(
                f"<p style='font-size:28px; font-weight:bold; color:white;'>📝 Status: {report['status']}</p>",
                unsafe_allow_html=True
            )

            st.markdown(f"**📩 Reported by:** `{report['student_username']}`")
            st.markdown(f"**🔹 Description:** _{report['description']}_")

            if report["image"]:
                st.image(report["image"], caption="📷 Uploaded Image", use_column_width=True)

            if report["video"]:
                st.video(report["video"])

    st.divider()
    st.button("🔴 Logout", on_click=logout)
    st.stop()  # Prevents UI from rendering both sections

# ✅ **Show Issue Reporting Form (Only when "View My Reports" is NOT selected)**
st.header("📝 Report an Issue")

categories = {
    "Faulty Infrastructure": ["Broken chairs", "Damaged classrooms", "Elevator malfunctions"],
    "Electrical Issues": ["Power failures", "Non-functional lights", "AC/heater problems"],
    "Water & Sanitation": ["Leaking pipes", "Unclean washrooms", "Poor drainage"],
    "Internet & Network": ["Slow WiFi", "Network downtime"],
    "Security Concerns": ["Malfunctioning CCTV", "Unauthorized access", "Broken locks"],
}

category = st.selectbox("📂 Select Issue Category", list(categories.keys()))
subcategory = st.selectbox("📂 Select Subcategory", categories[category])
priority = st.selectbox("⚡ Select Priority", ["Critical", "High", "Medium", "Low"])
description = st.text_area("📝 Describe the Issue")
uploaded_image = st.file_uploader("📷 Upload Image (Optional)", type=["png", "jpg", "jpeg"])
uploaded_video = st.file_uploader("🎥 Upload Video (Optional)", type=["mp4"])

if st.button("📩 Submit Report"):
    conn = get_db_connection()
    cursor = conn.cursor()

    image_data = uploaded_image.read() if uploaded_image else None
    video_data = uploaded_video.read() if uploaded_video else None

    try:
        cursor.execute("""
            INSERT INTO reports (category, subcategory, priority, description, status, image, video, student_username)
            VALUES (%s, %s, %s, %s, 'Pending', %s, %s, %s)
        """, (category, subcategory, priority, description, image_data, video_data, st.session_state["username"]))

        conn.commit()
        st.success("✅ Report Submitted Successfully!")

        # ✅ Auto-switch to report tracking after submission
        st.session_state["show_reports"] = True
        st.rerun()

    except mysql.connector.Error as err:
        st.error(f"❌ Error submitting report: {err}")

    finally:
        cursor.close()
        conn.close()

st.divider()
st.button("🔴 Logout", on_click=logout)  # Logout at the bottom
