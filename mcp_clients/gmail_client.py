from typing import Optional
from schemas.state import AgentState
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


class GmailMCPClient:
    """LangGraph-compliant Gmail MCP client"""
    
    def __init__(self, sender_email: Optional[str] = None, app_password: Optional[str] = None):
        self.sender_email = sender_email or SENDER_EMAIL
        self.app_password = app_password or GMAIL_APP_PASSWORD
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        
    ) -> dict:
        """Returns status dict for state updates"""
        
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
            server.quit()

            return {
                "success": True,
                "message": f"📧 Email sent to {to}",
                "email_to": to,
                
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Email failed: {str(e)}",
                "error": str(e)
            }