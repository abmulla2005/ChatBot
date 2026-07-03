# RUN COMMAND:
# streamlit run streamlit_frontend_database.py

import uuid
import streamlit as st
from openai import (
    RateLimitError,
    AuthenticationError,
    APIConnectionError,
    APITimeoutError,
    APIError,
)

from langchain_core.messages import HumanMessage
from langgraph_database_backend import chatbot, retrieve_all_threads


# =====================================================
# Utility Functions
# =====================================================

def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    return state.values.get("messages", [])


# =====================================================
# Session State
# =====================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])


# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("🤖 LangGraph Chatbot")

if st.sidebar.button("➕ New Chat"):
    reset_chat()

st.sidebar.divider()

st.sidebar.subheader("My Conversations")

for thread_id in reversed(st.session_state["chat_threads"]):

    if st.sidebar.button(str(thread_id), use_container_width=True):

        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)

        history = []

        for msg in messages:

            role = "user" if isinstance(msg, HumanMessage) else "assistant"

            history.append(
                {
                    "role": role,
                    "content": msg.content,
                }
            )

        st.session_state["message_history"] = history


# =====================================================
# Chat History
# =====================================================

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =====================================================
# User Input
# =====================================================

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        },
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }

    # ==============================================
    # AI Response
    # ==============================================

    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                ai_message = st.write_stream(

                    message_chunk.content

                    for message_chunk, metadata in chatbot.stream(

                        {
                            "messages": [
                                HumanMessage(content=user_input)
                            ]
                        },

                        config=CONFIG,

                        stream_mode="messages",

                    )
                )

            st.session_state["message_history"].append(
                {
                    "role": "assistant",
                    "content": ai_message,
                }
            )

        except RateLimitError:

            st.error(
                "🚦 Model is currently busy.\n\nPlease wait a few seconds and try again."
            )

        except AuthenticationError:

            st.error(
                "❌ Invalid OpenRouter API Key."
            )

        except APIConnectionError:

            st.error(
                "🌐 Unable to connect to OpenRouter."
            )

        except APITimeoutError:

            st.error(
                "⌛ Request timed out."
            )

        except APIError as e:

            st.error(f"API Error:\n\n{e}")

        except Exception as e:

            st.error(f"Unexpected Error:\n\n{e}")
