import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langserve import RemoteRunnable
from langchain_core.messages import ChatMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from utils import print_messages

load_dotenv()

st.set_page_config(page_title="DaconInfinityGPT", page_icon="🔗")
st.title("DaconInfinityGPT")

if "store" not in st.session_state:
  st.session_state["store"] = {}

if "messages" not in st.session_state:
  st.session_state["messages"] = []


def filter_messages(messages, k=10):
  return messages[-k:]


def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in st.session_state["store"]:
    st.session_state["store"][session_id] = ChatMessageHistory()
  return st.session_state["store"][session_id]


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
def get_runnable_message_history():
  return RunnableWithMessageHistory(
    get_chain(),
    get_session_history,
    input_messages_key="messages",
  )


@st.cache_resource
def get_model():
  return RemoteRunnable(os.getenv('LANGSERVE_ENDPOINT'))


@st.cache_resource
def get_chain():
  chain = (
      RunnablePassthrough.assign(messages=lambda x: filter_messages(x["messages"]))
      | get_prompt()
      | get_model()
  )
  return chain

# Using "with" notation
with st.sidebar:
  chat_id = st.text_input("session id를 입력하세요.")
  if st.button("bind"):
    st.session_state["messages"] = []
    if "chat_id" in st.session_state:
      get_session_history(st.session_state["chat_id"]).clear()
    st.session_state["chat_id"] = chat_id

if "chat_id" in st.session_state:
  # 이전 대화기록 출력
  print_messages()

  if user_input := st.chat_input("메시지를 입력해 주세요."):
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))


    response = get_runnable_message_history().invoke({"messages": [HumanMessage(content=user_input)]}, config={"configurable": {"session_id": st.session_state["chat_id"]}})
    print(get_session_history(st.session_state["chat_id"]))
    print('-'*10)
    with st.chat_message("assistant"):
      msg = response.content

      st.write(msg)
      st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
