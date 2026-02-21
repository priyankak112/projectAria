from langgraph.graph import StateGraph, END
from schemas.state import AgentState
from agents.classifier_agent import classifier_agent
from agents.rag_agent import rag_agent
from agents.tool_router import tool_router
from agents.it_agent import it_agent
from agents.human_agent import human_agent


def route_from_classifier(state: AgentState) -> str:
   
    print("🔀 Routing from classifier...")
    
    if state.confidence_score is None or state.confidence_score < 0.5:
        print(f"⚠️ Low confidence ({state.confidence_score}), escalating to human")
        return "human_agent"
    
    # Priority 2: Route based on classified intent
    if state.intent == "knowledge":
        print("📚 Routing to RAG Agent")
        return "rag_agent"
    
    elif state.intent == "complaint":
        print("🎫 Routing to IT Agent")
        return "it_agent"
    
    elif state.intent == "escalation":
        print("🚨 Routing to Human Agent")
        return "human_agent"
    
    else:
        print(f"Unknown intent '{state.intent}'")
        return "human_agent"



def build_graph():
        
    graph = StateGraph(AgentState)

    # Add nodes (only actual agents, not tool_router)
    graph.add_node("classifier", classifier_agent)
    graph.add_node("rag_agent", rag_agent)
    graph.add_node("it_agent", it_agent)
    graph.add_node("human_agent", human_agent)

    # Set entry point
    graph.set_entry_point("classifier")

    graph.add_conditional_edges(
        "classifier",
        route_from_classifier,
        {
            "rag_agent": "rag_agent",
            "it_agent": "it_agent",
            "human_agent": "human_agent"
        }
    )

    # All agents lead to END
    graph.add_edge("rag_agent", END)
    graph.add_edge("it_agent", END)
    graph.add_edge("human_agent", END)

    print("✅ Graph built successfully")
    return graph.compile()
