from langchain_google_genai import ChatGoogleGenerativeAI
from rag.vector_store import load_vector_store
from schemas.state import AgentState
from llm_config import llm


def rag_agent(state: AgentState) -> AgentState:
    print("Inside RAG agent")
    vectordb = load_vector_store()
    docs = vectordb.similarity_search(state.user_query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the employee question using ONLY the context below.

Context:
{context}

Question:
{state.user_query}
"""
    answer = llm.invoke(prompt).content
    state.response = answer
    return state
