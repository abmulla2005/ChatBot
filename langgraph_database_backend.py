from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from openai import (
    RateLimitError,
    AuthenticationError,
    APIConnectionError,
    APITimeoutError,
    APIError,
)

import sqlite3
import os
import time

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------
load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY3")

if not api_key:
    raise ValueError("OPEN_ROUTER_API_KEY3 is missing in .env")

# ----------------------------------------------------
# LLM
# ----------------------------------------------------
llm = ChatOpenAI(
    model="liquid/lfm-2.5-embedding-350m:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.7,
    streaming=True,
)

# ----------------------------------------------------
# LangGraph State
# ----------------------------------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ----------------------------------------------------
# Safe LLM Invoke
# ----------------------------------------------------
def invoke_with_retry(messages, retries=3):

    for attempt in range(retries):

        try:
            return llm.invoke(messages)

        except RateLimitError:

            if attempt == retries - 1:
                raise Exception(
                    "🚦 OpenRouter Free Model is busy.\n\n"
                    "Please wait 20-30 seconds and try again."
                )

            wait = 2 ** attempt
            print(f"Rate Limited... Retrying in {wait}s")
            time.sleep(wait)

        except AuthenticationError:
            raise Exception(
                "❌ Invalid OpenRouter API Key.\n"
                "Check OPEN_ROUTER_API_KEY3 in your .env file."
            )

        except APIConnectionError:
            raise Exception(
                "🌐 Unable to connect to OpenRouter.\n"
                "Check your internet connection."
            )

        except APITimeoutError:

            if attempt == retries - 1:
                raise Exception("⌛ Request timed out.")

            time.sleep(2)

        except APIError as e:
            raise Exception(f"OpenRouter API Error:\n{e}")

        except Exception as e:
            raise Exception(f"Unexpected Error:\n{e}")


# ----------------------------------------------------
# Chat Node
# ----------------------------------------------------
def chat_node(state: ChatState):

    messages = state["messages"]

    response = invoke_with_retry(messages)

    return {
        "messages": [response]
    }


# ----------------------------------------------------
# SQLite Checkpointer
# ----------------------------------------------------
conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(conn=conn)

# ----------------------------------------------------
# Graph
# ----------------------------------------------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# ----------------------------------------------------
# Retrieve Conversation Threads
# ----------------------------------------------------
def retrieve_all_threads():

    threads = set()

    for checkpoint in checkpointer.list(None):

        thread_id = checkpoint.config["configurable"]["thread_id"]

        threads.add(thread_id)

    return list(threads)
