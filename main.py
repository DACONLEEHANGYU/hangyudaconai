import streamlit as st
from utils import print_messages
from langchain_core.messages import ChatMessage


llm = RemoteRunnable(LANGSERVE_ENDPOINT)

st.set_page_config(page_title="DaconInfinityGPT", page_icon="🔗")
st.title("DaconInfinityGPT")

if "messages" not in st.session_state:
  st.session_state["messages"] = []

# 이전 대화기록 출력
print_messages()

if user_input := st.chat_input("메시지를 입력해 주세요."):
  st.chat_message("user").write(f"{user_input}")
  st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

  with st.chat_message("assistant"):
    msg = f"당신이 입력한 내용은 {user_input}"
    st.write(msg)
    st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))
