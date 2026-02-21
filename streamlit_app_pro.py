import streamlit as st
import uuid
from datetime import datetime
from graph import build_graph
from schemas.state import AgentState
import json
import pandas as pd

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="🤖 CorpAssist AI Pro",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'graph' not in st.session_state:
    st.session_state.graph = build_graph()
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
if 'current_ticket_id' not in st.session_state:
    st.session_state.current_ticket_id = None
if 'conversation_count' not in st.session_state:
    st.session_state.conversation_count = 0
if 'pending_input' not in st.session_state:
    st.session_state.pending_input = None

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
    <style>
            
    /* App Background */
    .stApp {
        background-color: #F5F7FA;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .escalation-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .knowledge-badge {
        background-color: #cce5ff;
        color: #1976d2;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    .complaint-badge {
        background-color: #ffcccc;
        color: #d32f2f;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    .escalation-badge {
        background-color: #ffe0b2;
        color: #f57c00;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("🎛️ CorpAssist AI Control Panel")
    
    # User Info
    with st.expander("👤 User Profile", expanded=False):
        st.text(f"User ID: {st.session_state.user_id}")
        st.text(f"Session Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.divider()
    
    # Session Stats
    with st.expander("📈 Session Statistics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Conversations", st.session_state.conversation_count)
            st.metric("Messages", len(st.session_state.messages))
        with col2:
            st.metric("Tickets", len(st.session_state.tickets))
            if st.session_state.current_ticket_id:
                    st.caption(f"**Latest Ticket:** {st.session_state.current_ticket_id}")
    
    st.divider()
    
    # Settings
    with st.expander("⚙️ Settings", expanded=False):
        st.markdown("### Chat Settings")
        show_details = st.checkbox("Show response details", value=True)
        show_confidence = st.checkbox("Show confidence scores", value=True)
        auto_scroll = st.checkbox("Auto-scroll to latest", value=True)
    
    st.divider()
    
    # Actions
    st.markdown("### Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.user_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.tickets = []
            st.session_state.conversation_count = 0
            st.rerun()
    
    st.divider()
    
    # Info
    st.info("""
    **CorpAssist AI** helps employees with:
    - 📚 Company knowledge retrieval
    - 🎫 IT ticket creation
    - 🚨 Human escalations
    """)

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Analytics", "🎫 Tickets", "❓ Help"])

# ============================================================================
# TAB 1: CHAT INTERFACE
# ============================================================================

with tab1:
    st.title("💬 Chat with CorpAssist AI")
    st.markdown("*Ask questions, report issues, or request assistance*")
    
    st.divider()
    
    # Chat display area
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.messages) == 0:
            st.info("👋 Welcome! Start a conversation by typing your message below.")
        else:
            for msg in st.session_state.messages:
                if msg['role'] == 'user':
                    st.markdown(f"""
                        <div class='chat-message user-message'>
                            <strong>👤 You:</strong> {msg['content']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    is_escalation = msg.get('escalation', False)
                    msg_class = 'escalation-message' if is_escalation else 'bot-message'
                    icon = "🚨" if is_escalation else "🤖"
                    
                    st.markdown(f"""
                        <div class='chat-message {msg_class}'>
                            <strong>{icon} CorpAssist:</strong>
                            <div style='margin-top: 0.5rem;'>{msg['content']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Show metadata
                    if msg.get('metadata'):
                        meta = msg['metadata']
                        cols = st.columns(4)
                        
                        if meta.get('intent'):
                            intent = meta['intent']
                            if intent == 'knowledge':
                                cols[0].markdown(f"<span class='knowledge-badge'>📚 Knowledge</span>", unsafe_allow_html=True)
                            elif intent == 'complaint':
                                cols[0].markdown(f"<span class='complaint-badge'>🎫 Complaint</span>", unsafe_allow_html=True)
                            elif intent == 'escalation':
                                cols[0].markdown(f"<span class='escalation-badge'>🚨 Escalation</span>", unsafe_allow_html=True)
                        
                        if meta.get('confidence') and show_confidence:
                            confidence = meta['confidence'] * 100
                            cols[1].metric("Confidence", f"{confidence:.0f}%")
                        
                        if meta.get('ticket_id'):
                            cols[2].code(meta['ticket_id'], language='text')
                        
                        if meta.get('agent'):
                            cols[3].caption(f"**Agent:** {meta['agent']}")
    
    st.divider()
    
    # Input area with callback
    def handle_send():
        user_input = st.session_state.chat_input
        if not user_input or not user_input.strip():
            return
        
        st.session_state.pending_input = user_input
        st.session_state.chat_input = ""
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.text_input(
            label="Message",
            key="chat_input",
            placeholder="Type your question or issue...",
            label_visibility="collapsed",
            on_change=handle_send
        )
    
    with col2:
        st.button("📤 Send", use_container_width=True, on_click=handle_send)
    
    # Process pending input if any
    if st.session_state.pending_input:
        user_input = st.session_state.pending_input
        st.session_state.pending_input = None
        
        st.session_state.conversation_count += 1
        
        state = AgentState(
            user_id=st.session_state.user_id,
            user_query=user_input
        )
        
        with st.spinner("⏳ Processing..."):
            try:
                result = st.session_state.graph.invoke(state)
                
                bot_response = result.get("response", "Sorry, something went wrong.")
                
                metadata = {
                    'intent': result.get('intent'),
                    'confidence': result.get('confidence_score'),
                    'agent': result.get('last_agent')
                }
                ticket_id = None
                ticket_type = None
                
                # Check for IT complaint ticket
                if result.get('it_ticket_id'):
                    ticket_id = result.get('it_ticket_id')
                    ticket_type = 'complaint'
                # Check for escalation ticket
                elif result.get('escalation_id'):
                    ticket_id = result.get('escalation_id')
                    ticket_type = 'escalation'
                # Fallback to generic ticket_id
                elif result.get('ticket_id'):
                    ticket_id = result.get('ticket_id')
                    ticket_type = 'ticket'

                if ticket_id:
                    metadata['ticket_id'] = ticket_id
                    st.session_state.current_ticket_id = ticket_id
                    st.session_state.tickets.append({
                        'id': ticket_id,
                        'query': user_input,
                        'timestamp': datetime.now(),
                        'status': 'OPEN',
                        'type': ticket_type
                    })
                
                # Add both user and bot messages together after processing
                st.session_state.messages.append({
                    'role': 'user',
                    'content': user_input
                })
                
                st.session_state.messages.append({
                    'role': 'bot',
                    'content': bot_response,
                    'metadata': metadata,
                    'escalation': result.get('escalation_sent', False)
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 2: ANALYTICS
# ============================================================================

with tab2:
    st.title("📊 Conversation Analytics")
    
    if len(st.session_state.messages) == 0:
        st.info("No messages yet. Start a conversation to see analytics.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Messages", len(st.session_state.messages))
        with col2:
            user_msgs = sum(1 for m in st.session_state.messages if m['role'] == 'user')
            st.metric("User Messages", user_msgs)
        with col3:
            bot_msgs = sum(1 for m in st.session_state.messages if m['role'] == 'bot')
            st.metric("Bot Responses", bot_msgs)
        with col4:
            st.metric("Conversations", st.session_state.conversation_count)
        
        st.divider()
        
        # Intent distribution
        intents = {}
        for msg in st.session_state.messages:
            if msg.get('metadata') and msg['metadata'].get('intent'):
                intent = msg['metadata']['intent']
                intents[intent] = intents.get(intent, 0) + 1
        
        if intents:
            st.subheader("Intent Distribution")
            intent_df = pd.DataFrame(list(intents.items()), columns=['Intent', 'Count'])
            st.bar_chart(intent_df.set_index('Intent'))
        
        # Confidence scores
        confidences = [msg['metadata']['confidence'] for msg in st.session_state.messages 
                      if msg.get('metadata') and msg['metadata'].get('confidence')]
        
        if confidences:
            st.subheader("Average Confidence Score")
            avg_confidence = sum(confidences) / len(confidences)
            st.metric("Average Confidence", f"{avg_confidence*100:.1f}%")

# ============================================================================
# TAB 3: TICKETS
# ============================================================================

with tab3:
    st.title("🎫 Support Tickets")
    
    if len(st.session_state.tickets) == 0:
        st.info("No tickets created yet.")
    else:
        st.subheader(f"Active Tickets ({len(st.session_state.tickets)})")
        
        for ticket in st.session_state.tickets:
            ticket_type = ticket.get('type', 'ticket')
            type_icon = "🚨" if ticket_type == 'escalation' else "🎫"
            type_label = "ESCALATION" if ticket_type == 'escalation' else "COMPLAINT"
            
            with st.expander(f"{type_icon} {type_label} - {ticket['id']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"**Issue:** {ticket['query']}")
                with col2:
                    st.caption(f"**Created:** {ticket['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.caption(f"**Status:** {ticket['status']}")
                st.caption(f"**Type:** {type_label}")

# ============================================================================
# TAB 4: HELP
# ============================================================================

with tab4:
    st.title("❓ Help & Documentation")
    
    st.markdown("""
    ### How to use CorpAssist AI
    
    📚 Knowledge Queries
    Ask about company policies, handbook information, or general knowledge.
    - "What's the leave policy?"
    - "Tell me about company benefits"
    - "What are the working hours?"
    
    #### 🎫 Complaints & Issues
    Report problems or request operational help.
    - "My laptop is not working"
    - "I can't access the VPN"
    - "Request for printer access"
    
    #### 🚨 Escalations
    For serious concerns or when you need human attention.
    - "I need to speak with HR about something sensitive"
    - "This is urgent and needs immediate attention"
    
    ### Features
    - ✅ Multi-agent intelligent routing
    - ✅ Knowledge retrieval from company docs
    - ✅ Automatic ticket creation
    - ✅ Human escalation support
    - ✅ Conversation history tracking
    
    ### System Architecture
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Agents:**
        - 🤖 Classifier Agent
        - 📚 RAG Agent
        - 🎫 IT Agent
        - 🚨 Human Agent
        """)
    with col2:
        st.markdown("""
        **Architecture:**
        - LangGraph workflow
        - ChromaDB vector store
        - Gemini LLM
        - SQLite database
        """)
