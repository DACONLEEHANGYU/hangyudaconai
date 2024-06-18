import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import ChatMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langserve import RemoteRunnable

from utils import print_messages

load_dotenv()

st.set_page_config(page_title="DaconInfinityGPT", page_icon="🔗")
st.title("DaconInfinityGPT")

if "messages" not in st.session_state:
  st.session_state["messages"] = []


@st.cache_resource
def get_prompt():
  return ChatPromptTemplate.from_messages(
    [
      (
        "system",
        "You are a helpful assistant. Answer all questions to the best of your ability.",
      ),
      MessagesPlaceholder(variable_name="messages"),
    ]
  )


@st.cache_resource
def get_model():
  return RemoteRunnable(os.getenv('LANGSERVE_ENDPOINT'))


@st.cache_resource
def get_chain():
  chain = (
      get_prompt()
      | get_model()
  )
  return chain

# 이전 대화기록 출력
print_messages()

if user_input := st.chat_input("메시지를 입력해 주세요."):
  st.chat_message("user").write(f"{user_input}")
  st.session_state["messages"].append(ChatMessage(role="user", content=user_input))


  response = get_chain().invoke({"messages": [HumanMessage(content=user_input)]})
  with st.chat_message("assistant"):
    msg = response.content

    st.write(msg)
    st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
