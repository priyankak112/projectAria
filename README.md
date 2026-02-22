# 🚀 Project ARIA – Adaptive Routing Intelligence Assistant

Project ARIA is a **production-ready, multi-agent AI chatbot system** designed for enterprise environments.  
It intelligently routes employee queries to specialized agents using **intent classification**, **RAG**, and **agent orchestration**, with full **ticketing, escalation, and notification support**.

✅ Deployed on **AWS Cloud EC2**  
✅ Dockerized & scalable  

## 🧠 What is Project ARIA?

Project ARIA (Adaptive Routing Intelligence Assistant) is an **intelligent multi-agent system** that:
- Understands user intent
- Routes queries to the correct specialized agent
- Uses **Retrieval-Augmented Generation (RAG)** for grounded answers
- Escalates low-confidence responses automatically
- Tracks tickets and notifies stakeholders via email

---

## ✨ Key Features

- 🧭 **Smart Intent Classification** – Automatically routes queries to specialized agents  
- 📚 **RAG-Powered Responses** – Uses vector search for knowledge-grounded answers  
- 🤖 **Multi-Agent Orchestration** – LangGraph-based state machine routing  
- 📊 **Confidence Scoring** – Low-confidence responses trigger escalation  
- 🎫 **Ticket Tracking System** – Persistent ticket & escalation storage  
- 📈 **Analytics Dashboard** – Insights into query patterns and agent usage  
- ✉️ **Email Notifications** – Automated Gmail alerts to stakeholders  
- 🧹 **Clean UX** – Auto-clearing input with Streamlit callbacks  

---

## 🏗️ System Architecture

```text
User
 ↓
Streamlit UI
 ↓
Intent Classification (Gemini)
 ↓
LangGraph Orchestrator
 ├── Knowledge Agent (RAG + ChromaDB)
 ├── IT Agent (SQLite via MCP,Gmail via custom MCP)
 ├── Escalation Agent(Gmail via MCP,sqlite via custom MCP)
 ↓
Response + Ticket Tracking
⭐ If you found this project interesting, feel free to star the repo and connect!
