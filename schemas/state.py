from pydantic import BaseModel
from typing import Optional

class AgentState(BaseModel):
    """Minimal LangGraph state for CORAI project"""
    
    # === REQUIRED ===
    user_query: str
    user_id: str
    
    # === CORE ROUTING ===
    intent: Optional[str] = None
    response: Optional[str] = None
    last_agent: Optional[str] = None
    
    # === ESCALATION ===
    escalation_sent: Optional[bool] = False
    escalation_id: Optional[str] = None
    escalation_details: Optional[dict] = None
    
    # === RAG PIPELINE ===
    rag_context: Optional[str] = None
    rag_results: Optional[list] = None
    
    # === CLASSIFICATION ===
    classified_category: Optional[str] = None
    confidence_score: Optional[float] = None
    
    # === IT TICKETING ===
    it_ticket_id: Optional[str] = None
    it_ticket_status: Optional[str] = None  # "OPEN", "IN_PROGRESS", "RESOLVED"
    # === TOOL EXECUTION ===
    tool_calls: Optional[list] = None
    tool_results: Optional[dict] = None
    
    # === ERROR HANDLING ===
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True