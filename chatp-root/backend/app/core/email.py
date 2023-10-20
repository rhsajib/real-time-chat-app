from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib  
from app.core.security import settings

SENDER_EMAIL = settings.SENDER_EMAIL
EMAIL_PASSWORD = settings.EMAIL_PASSWORD

def send_signup_email(recipient_email, activation_link):
    subject = "Activate Your Account"
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject

    email_content = f"""
    Hi,

    Thank you for signing up on Your Website! To activate your account, please click the following link:

    {activation_link}

    If you didn't sign up for Your Website, please disregard this email.

    Best regards,
    Your Website Team
    """
    message.attach(MIMEText(email_content, "plain"))
    email_text = message.as_string()

    try:
        smtp_server = "smtp.gmail.com"  # Update with your email service provider's SMTP server
        smtp_port = 587  # Update with the SMTP port

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)  # Update with your email password
        server.sendmail(SENDER_EMAIL, recipient_email, email_text)
        server.quit()

    except Exception as e:
        # Handle email sending errors
        print(f"Email sending error: {e}")
    
