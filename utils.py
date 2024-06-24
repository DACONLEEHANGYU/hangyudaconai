import streamlit as st


def print_messages(messages_container, responses):    

    if(responses == ""):
        print("utils > responses: ", responses)

    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
        for chat_message in st.session_state["messages"]:
            with messages_container:
                 messages_container.chat_message(chat_message["role"]).write(chat_message["content"])
                                  
 