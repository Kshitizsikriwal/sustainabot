import streamlit as st
import requests
import time

st.set_page_config(
    page_title="SustainaBot",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm SustainaBot. How can I help you with sustainability today? 🌱"}
    ]

def load_css():
    bg = "#121212"
    text = "#EAEAEA"
    user_bg = "#2E7D32"   # green
    bot_bg = "#2C2C2C"    # dark grey

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg};
            color: {text};
            font-family: "Segoe UI", "Roboto", sans-serif;
        }}
        .title {{
            text-align: center;
            font-weight: 600;
            font-size: 24px;
            margin-bottom: 12px;
        }}
        .chat-bubble {{
            padding: 12px 16px;
            border-radius: 16px;
            margin: 6px 0;
            max-width: 75%;
            line-height: 1.5;
            font-size: 15px;
        }}
        .user-bubble {{
            background-color: {user_bg};
            color: white;
            margin-left: auto;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
        }}
        .bot-bubble {{
            background-color: {bot_bg};
            color: {text};
            margin-right: auto;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 13px;
            opacity: 0.7;
        }}
    </style>
    """, unsafe_allow_html=True)

load_css()

with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared. How can I help you now? 🌱"}
        ]
        st.rerun()

    if st.button("⬇️ Download Chat", use_container_width=True):
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("Save Chat", chat_text, file_name="sustainabot_chat.txt")

    st.markdown("---")
    st.caption("🌱 Built with ❤️ by **Kshitiz Sikriwal**")


st.markdown('<div class="title">💬 SustainaBot</div>', unsafe_allow_html=True)

chat_box = st.container()

# Render chat history
with chat_box:
    for i, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        content = msg["content"]
        bubble_class = "user-bubble" if role == "user" else "bot-bubble"

        st.markdown(f'<div class="chat-bubble {bubble_class}">{content}</div>', unsafe_allow_html=True)

        # Add copy button only for assistant messages

if user_input := st.chat_input("Ask me anything about sustainability..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble user-bubble">{user_input}</div>', unsafe_allow_html=True)

    # Placeholder for bot response
    placeholder = st.empty()
    loader = st.empty()

    # Loader animation
    spinner_chars = ["/", "-", "\\", "|"]
    for i in range(8):  
        loader.markdown(f'<div class="chat-bubble bot-bubble">Thinking {spinner_chars[i % 4]}</div>', unsafe_allow_html=True)
        time.sleep(0.15)

    # API call
    try:
        response = requests.post(API_URL, json={"question": user_input})
        response.raise_for_status()
        bot_reply = response.json().get("answer", "⚠️ No answer received.")
    except Exception as e:
        bot_reply = f"⚠️ Request failed: {str(e)}"

    loader.empty()

    # Typing animation
    typed = ""
    for char in bot_reply:
        typed += char
        placeholder.markdown(f'<div class="chat-bubble bot-bubble">{typed}▌</div>', unsafe_allow_html=True)
        time.sleep(0.012)

    placeholder.markdown(f'<div class="chat-bubble bot-bubble">{typed}</div>', unsafe_allow_html=True)

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": typed})

st.markdown('<div class="footer">© 2025 SustainaBot | Made by Kshitiz Sikriwal</div>', unsafe_allow_html=True)
