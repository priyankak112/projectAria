from schemas.state import AgentState
from llm_config import llm
import json


def tool_router(state: AgentState) -> str:

    print("Inside tool routerrr")
    # Priority 1: Check confidence score
    if state.confidence_score is None or state.confidence_score < 0.5:
        print(f"⚠️ Low confidence ({state.confidence_score}), escalating to human agent")
        return "human_agent"
    
    # Priority 2: Route based on classified intent
    if state.intent == "knowledge":
        print("📚 Routing to RAG Agent for knowledge retrieval")
        return "rag_agent"
    
    elif state.intent == "complaint":
        print("🎫 Routing to IT Agent for complaint/ticketing")
        return "it_agent"
    
    elif state.intent == "escalation":
        print("🚨 Routing to Human Agent for escalation")
        return "human_agent"
    
    else:
        # Fallback: unknown intent escalates to human
        print(f"❓ Unknown intent '{state.intent}', escalating to human")
        return "human_agent"