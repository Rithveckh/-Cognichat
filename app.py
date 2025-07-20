import streamlit as st
from langchain_groq.chat_models import ChatGroq
import os

# Load Groq API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq chat model
chat = ChatGroq(
    model="mistral-saba-24b",
    api_key=groq_api_key,
    temperature=0.5,
)

# Page config
st.set_page_config(page_title="🧠 Cognichat", page_icon="🤖")

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #121212;
    color: white;
}
.chat-message {
    padding: 1rem;
    margin-bottom: 0.5rem;
    border-radius: 10px;
    line-height: 1.5;
}
.user-message {
    background-color: #2c2c2e;
    text-align: right;
    color: #ffffff;
    margin-left: 20%;
}
.bot-message {
    background-color: #1f2937;
    text-align: left;
    color: #d1d5db;
    margin-right: 20%;
}
.title {
    font-size: 2.2rem;
    font-weight: 600;
    color: #00ffff;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🧠 Cognichat</div>', unsafe_allow_html=True)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_content" not in st.session_state:
    st.session_state.file_content = None

if "awaiting_file_query" not in st.session_state:
    st.session_state.awaiting_file_query = False

# Sidebar
with st.sidebar:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.file_content = None
        st.session_state.awaiting_file_query = False
        st.rerun()

    chat_text = "\n\n".join([
        f"You: {m['content']}" if m["role"] == "user" else f"Cognichat: {m['content']}"
        for m in st.session_state.messages
    ])
    st.download_button(
        label="📥 Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
    )

    st.markdown("---")

    memory_toggle = st.toggle("🧠 Enable Chat Memory", value=True)
    if not memory_toggle:
        st.session_state.messages = st.session_state.messages[-1:]

    st.markdown("---")

    # File Upload Section
    st.markdown("### 📎 Upload File")
    uploaded_file = st.file_uploader("Upload a .txt or .pdf", type=["txt", "pdf"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        try:
            file_text = file_bytes.decode("utf-8")
        except:
            file_text = file_bytes[:1000].decode("utf-8", errors="ignore")
        st.session_state.file_content = file_text
        st.session_state.awaiting_file_query = True
        st.success("📁 File uploaded! Now ask a question based on it.")

    st.markdown("---")
    st.markdown("### 📊 Chat Stats")
    st.write(f"🗨️ Messages: {len(st.session_state.messages)}")
    st.write(f"📝 Total Words: {sum(len(m['content'].split()) for m in st.session_state.messages)}")

# Display all messages
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    emoji = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(f"<div class='chat-message {role_class}'>{emoji} {msg['content']}</div>", unsafe_allow_html=True)

# Chat input
query = st.chat_input("Type your message...", key="chat_input_box")

# Handle input
if query:
    # If a file was uploaded and awaiting user prompt
    if st.session_state.awaiting_file_query and st.session_state.file_content:
        full_prompt = f"Analyze the following uploaded file content and answer this question:\n\n{st.session_state.file_content[:1000]}...\n\nUser question: {query}"
        st.session_state.awaiting_file_query = False
        st.session_state.file_content = None
    else:
        full_prompt = query

    # Append user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Get bot response
    with st.spinner("🤖 Cognichat is typing..."):
        response = chat.invoke([{"role": "user", "content": full_prompt}])

    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.rerun()
