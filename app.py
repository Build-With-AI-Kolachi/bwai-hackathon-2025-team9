import streamlit as st

st.set_page_config(page_title="WhatsHelpAI", layout="centered")

st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        max-width: 70%;
        font-size: 16px;
        line-height: 1.5;
    }
    .user-msg {
        background-color: #dcf8c6;
        margin-left: auto;
        text-align: right;
    }
    .bot-msg {
        background-color: #fff;
        margin-right: auto;
        text-align: left;
        border: 1px solid #ececec;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        border: 1px solid #ececec;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 WhatsHelpAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="stChatMessage user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="stChatMessage bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_input("Type your message...", key="input", label_visibility="collapsed")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Replace this with your AI logic
    bot_response = f"Echo: {user_input}"
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.experimental_rerun()