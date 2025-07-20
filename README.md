# 🧠 Cognichat – The AI-Powered File + Chat Assistant

![Built With](https://img.shields.io/badge/Built%20With-Langchain%20%7C%20Streamlit%20%7C%20Groq-orange?style=for-the-badge)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cognichat-ai.streamlit.app)

**Cognichat** is a sleek, lightweight AI chatbot built with **Streamlit**, powered by **Groq’s ultra-fast models**, and enhanced with **Langchain** for context handling. You can chat naturally or upload `.txt` or `.pdf` files — and then ask smart questions about them.

---

## 🚀 Live Demo

👉 [Try Cognichat Now](https://cognichat-ai.streamlit.app)

---

## ✨ Features

- 💬 Chat with an LLM powered by Groq
- 📎 Upload `.txt` or `.pdf` files and ask questions about the content
- 🧠 Optional memory toggle (retain or reset history)
- 📥 Download your chat history
- 🧹 Clear chat with a single click
- 🎨 Beautiful dark UI with custom fonts and layout

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **AI Model:** [Groq API](https://groq.com/)
- **Language Wrapping:** Langchain
- **Environment Variables:** Python `dotenv`
- **PDF/Text Parsing:** Python native decoding / `pypdf`

---

## 📦 Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cognichat.git
cd cognichat
```

---
2. Create Virtual Environment
```bash
python -m venv venv
```
Then activate it:
```bash
source venv/bin/activate
On Windows: venv\Scripts\activate
```
3. Install Dependencies
  Install packages directly:
```bash
pip install streamlit langchain langchain-community langchain-groq groq python-dotenv pypdf
```
Or using the requirements file:
```bash
pip install -r requirements.txt
```
---
4. Add Your API Key
Create a .env file in the root directory and add: GROQ_API_KEY=your_groq_api_key_here
---
5. Run the App
```bash
streamlit run app.py
```
Or:
```bash
python -m streamlit run app.py
```
---

☁️ Deploy on Streamlit Cloud
  1.Push your code to GitHub
  2.Go to https://share.streamlit.io
  3.Connect your GitHub repo and select app.py as the entry file
  4.Under App Settings → Secrets, add: GROQ_API_KEY = "your_groq_api_key_here"
  5.Customize your app's subdomain under App URL
  6.Click Deploy 🚀
