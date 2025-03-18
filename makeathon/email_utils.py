import smtplib
from email.mime.text import MIMEText

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "shazgamin@gmail.com"  # Change this
SENDER_PASSWORD = "777eN49tnsc777"  # Use App Password, NOT your real password
DEPARTMENT_OFFICER_EMAIL = "shazopyt@gmail.com"

# ✅ Send Email
def send_email(category, subcategory, priority, description):
    subject = f"New Issue Reported - {category} ({priority})"
    body = f"""
    A new issue has been reported.

    **Category:** {category}
    **Subcategory:** {subcategory}
    **Priority:** {priority}
    **Description:** {description}

    Please take necessary action.

    Regards,
    SBMS System
    """

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = DEPARTMENT_OFFICER_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, DEPARTMENT_OFFICER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
