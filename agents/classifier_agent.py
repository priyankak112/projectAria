from langchain_google_genai import ChatGoogleGenerativeAI
from schemas.state import AgentState
from dotenv import load_dotenv
from llm_config import llm
import json


def classifier_agent(state: AgentState) -> AgentState:
        
    prompt = f"""
You are an intent classification agent for a corporate assistant.

Classify the user's request into exactly ONE of the following categories:

1. "knowledge"
   - The user is asking for information from company documents
   - Examples: policies, leave, holidays, handbook, rules

2. "complaint"
   - The user is reporting an issue or requesting operational help
   - Examples: IT issues, salary problems, access issues, requests

3. "escalation"
   - The user is angry, dissatisfied, or explicitly wants human involvement
   - Examples: complaints about people, managers, serious concerns, legal or HR escalation

Return ONLY a valid JSON object in this format:
{{
  "topic": "<one_of_knowledge_complaint_escalation>",
  "confidence": <float_0_to_1>
}}

Topic confidence scale:
- 0.9-1.0: Very clear intent
- 0.7-0.9: Clear intent with minor ambiguity
- 0.5-0.7: Ambiguous, could fit multiple categories
- Below 0.5: Very unclear, recommend escalation
-Do not include explanations, markdown, or extra text.
- Output raw JSON only.
User query:
{state.user_query}
"""
    
    try:
        result = llm.invoke(prompt).content.strip()
        classification = json.loads(result)
        print("result from LLM:", classification)
        intent = classification.get("topic", "escalation")
        confidence = float(classification.get("confidence", 0.5))
        
        # Ensure confidence is within bounds
        confidence = max(0.0, min(1.0, confidence))
        
        print(f"✅ Classified intent: {intent}")
        print(f"📊 Confidence score: {confidence:.2f}")
        
        # Update state
        state.intent = intent
        state.classified_category = intent
        state.confidence_score = confidence
        
        return state
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        state.intent = "escalation"
        state.classified_category = "escalation"
        state.confidence_score = 0.0
        state.error = f"Classification failed - Invalid JSON: {str(e)}"
        return state
    
    except Exception as e:
        print(f"❌ Unexpected classifier error: {e}")
        state.intent = "escalation"
        state.classified_category = "escalation"
        state.confidence_score = 0.0
        state.error = f"Classifier error: {str(e)}"
        return state