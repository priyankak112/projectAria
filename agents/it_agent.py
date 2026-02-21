from datetime import datetime
from dotenv import load_dotenv
from schemas.state import AgentState
from mcp_clients.gmail_client import GmailMCPClient
from mcp_clients.db_mcpclient import DatabaseMCPClient
import os
import uuid

load_dotenv()

IT_SUPPORT_EMAIL = os.getenv("IT_SUPPORT_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


def it_agent(state: AgentState) -> AgentState:
      
    print(" Executing IT Agent for complaint handling... ")

    user_query = state.user_query or ""
    if not user_query or user_query.strip() == "":
        print("⚠️ WARNING: Empty user query detected.")
        state.response = "⚠️ No query to process."
        state.escalation_sent = False
        state.last_agent = "it_agent"
        return state
    
    user_query = state.user_query
    user_id = state.user_id or "anonymous"
    ticket_id = f"IT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    timestamp = datetime.now().isoformat()
    
    # Create email body
    email_body = f"""
🎫 IT SUPPORT TICKET CREATED

Ticket ID: {ticket_id}
User ID: {user_id}
Submission Time: {timestamp}

Issue Description:
{user_query}
Please acknowledge receipt and provide resolution timeline.
"""
    
    # Step 1: Send email to IT support
    gmail_client = GmailMCPClient(
        sender_email=SENDER_EMAIL,
        app_password=GMAIL_APP_PASSWORD
    )
    
    email_result = gmail_client.send_email(
        to=IT_SUPPORT_EMAIL,
        subject=f" [{ticket_id}] IT Support Ticket",
        body=email_body
    )
    
    # Step 2: Log complaint to database
    db_client = DatabaseMCPClient(connection_string=DB_CONNECTION_STRING)
    
    complaint_record = {
        "complaint_id": ticket_id,
        "user_id": user_id,
        "user_query": user_query,
        "created_at": timestamp
    }
    
    db_result = db_client.insert_complaint(
        table="complaints",
        record=complaint_record
    )
    
    # Step 3: Update state
    state.response = (
        f"🎫 IT ticket created successfully: {ticket_id}\n"
        f"📧 Your issue has been sent to the IT support team.\n"
        f"⏱️ You can expect a response within 24 hours."
    )
    state.it_ticket_id = ticket_id
    state.it_ticket_status = "OPEN"
    state.escalation_sent = email_result["success"]
    state.escalation_details = {
        "email": email_result,
        "database": db_result,
        "ticket_id": ticket_id,
        "timestamp": timestamp
    }
    state.last_agent = "it_agent"
    
    print(f" Complaint {ticket_id} created: Email sent + DB recorded")
    
    return state