from datetime import datetime
from dotenv import load_dotenv
from schemas.state import AgentState
from mcp_clients.gmail_client import GmailMCPClient
from mcp_clients.db_mcpclient import DatabaseMCPClient
import os
import uuid

load_dotenv()

HUMAN_SUPPORT_EMAIL = os.getenv("HUMAN_SUPPORT_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


def human_agent(state: AgentState) -> AgentState:
       
    print("🚨 Executing Human Agent for escalation")
     # ✅ Guard check: Prevent execution if query is empty
    user_query = state.user_query or ""
    
    if not user_query or user_query.strip() == "":
        print("⚠️ WARNING: Empty user query detected. Skipping escalation.")
        state.response = "⚠️ No query to escalate. Please provide a valid complaint."
        state.escalation_sent = False
        state.last_agent = "human_agent"
        return state
    #if not empty
    user_query = state.user_query
    user_id = state.user_id or "anonymous"
    escalation_id = f"ESC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    timestamp = datetime.now().isoformat()
    
    # Create email body
    email_body = f"""
🚨 HUMAN ESCALATION REQUIRED

Escalation ID: {escalation_id}
User ID: {user_id}
Timestamp: {timestamp}

User Message:
{user_query}
Please address this escalation and update the system with resolution.
"""
    
    # Step 1: Initialize Gmail client and send email
    gmail_client = GmailMCPClient(
        sender_email=SENDER_EMAIL,
        app_password=GMAIL_APP_PASSWORD
    )
    
    email_result = gmail_client.send_email(
        to=HUMAN_SUPPORT_EMAIL,
        subject=f" [{escalation_id}] Human Escalation Required",
        body=email_body
    )
    
    # Step 2: Initialize Database client and create escalation record
    db_client = DatabaseMCPClient(connection_string=DB_CONNECTION_STRING)
    
    escalation_record = {
        "escalation_id": escalation_id,
        "user_id": user_id,
        "user_query": user_query,
        "created_at": timestamp
    }
    
    db_result = db_client.insert_escalation(
        table="escalations",
        record=escalation_record
    )
    
    # Step 3: Update state with both email and DB results
    state.response = (
        f"🚨 Escalation created successfully: {escalation_id}\n"
        f"⚠️ Your request has been escalated to a human support team.\n"
        f"📩 A human representative will contact you shortly.\n"
    )
    state.escalation_sent = email_result["success"]
    state.escalation_id = escalation_id
    state.escalation_details = {
        "email": email_result,
        "database": db_result,
        "escalation_id": escalation_id,
        "timestamp": timestamp
    }
    state.last_agent = "human_agent"
    
    # Log success/failure
    if email_result["success"] and db_result["success"]:
        print(f"✅ Escalation {escalation_id} created: Email sent + DB recorded")
    else:
        print(f"⚠️ Escalation {escalation_id}: Email={email_result['success']}, DB={db_result['success']}")
    
    return state