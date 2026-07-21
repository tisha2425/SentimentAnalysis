import streamlit as st
from ml_model import predict_sentiment
from ai_model import generate_ai_response
from chatbot import chatbot_response
from email_utils import send_email
import random
import time
import os
import pandas as pd

# ================================
# SIDEBAR CHATBOT
# ================================

st.sidebar.markdown("---")

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if st.sidebar.button("💬 Chat with Assistant"):
    st.session_state.chat_open = not st.session_state.chat_open

if st.session_state.clear_input:
    st.session_state.sidebar_chat_input = ""
    st.session_state.clear_input = False

if st.session_state.chat_open:

    st.sidebar.markdown("### 💬 Assistant")

    for msg in st.session_state.chat_messages:

        role = "You" if msg["role"] == "user" else "AI"

        st.sidebar.markdown(
            f"**{role}:** {msg['content']}"
        )

    user_input = st.sidebar.text_input(
        "Ask a question",
        key="sidebar_chat_input"
    )

    if st.sidebar.button("Send"):

        if user_input.strip():

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            ai_response = chatbot_response(user_input)

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

            st.session_state.clear_input = True

            st.rerun()
