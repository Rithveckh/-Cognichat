import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Make sure it's in your .env file.")
    st.stop()
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-pro")
st.set_page_config(page_title="🧠 Cognichat", page_icon="🤖")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Fira+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #121212;
    color: white;
}

.message-container {
    display: flex;
    flex-direction: column;
    padding-bottom: 2rem;
}

.message-pair {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-bottom: 1.5rem;
}

.user-bubble, .bot-bubble {
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 90%;
    word-wrap: break-word;
    white-space: pre-wrap;
    font-family: 'Fira Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.5;
}

.user-bubble {
    align-self: flex-end;
    background-color: #2e2e30;
    color: white;
    border: 1px solid #4a4a4a;
}

.bot-bubble {
    align-self: flex-start;
    background-color: #1c1c1f;
    color: #d1d5db;
    border: 1px solid #333;
}

.title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #00ffff;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🧠 Cognichat</div>', unsafe_allow_html=True)

# Session state
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
    st.download_button("📅 Download Chat", chat_text, "chat_history.txt")

    st.markdown("---")
    memory_toggle = st.toggle("🧠 Enable Chat Memory", value=True)
    if not memory_toggle:
        st.session_state.messages = st.session_state.messages[-1:]

    st.markdown("---")
    st.markdown("### 📌 Upload File")
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

# Render messages
st.markdown('<div class="message-container">', unsafe_allow_html=True)
i = 0
while i < len(st.session_state.messages):
    st.markdown('<div class="message-pair">', unsafe_allow_html=True)

    if st.session_state.messages[i]["role"] == "user":
        user_msg = st.session_state.messages[i]["content"]
        st.markdown(f"<div class='user-bubble'>🧍 {user_msg}</div>", unsafe_allow_html=True)
        i += 1

    if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "assistant":
        bot_msg = st.session_state.messages[i]["content"]
        st.markdown(f"<div class='bot-bubble'>🤖 {bot_msg}</div>", unsafe_allow_html=True)
        i += 1

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
query = st.chat_input("Type your message...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

# Stream bot response if needed
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_msg = st.session_state.messages[-1]["content"]

    if st.session_state.awaiting_file_query and st.session_state.file_content:
        full_prompt = (
            f"Analyze the following uploaded file content and answer this question:\n\n"
            f"{st.session_state.file_content[:1000]}...\n\nUser question: {user_msg}"
        )
        st.session_state.awaiting_file_query = False
        st.session_state.file_content = None
    else:
        full_prompt = user_msg

    typing_placeholder = st.empty()
    typing_placeholder.markdown('<div class="bot-bubble">🤖 Cognichat is typing...</div>', unsafe_allow_html=True)

    response_placeholder = st.empty()
    bot_response = ""
    try:
        stream = model.generate_content(full_prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                for char in chunk.text:
                    bot_response += char
                    response_placeholder.markdown(
                        f'<div class="bot-bubble">🤖 {bot_response}</div>', unsafe_allow_html=True
                    )
                    time.sleep(0.005)
        typing_placeholder.empty()
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
    except Exception as e:
        typing_placeholder.empty()
        error_msg = f"❌ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

    st.rerun()