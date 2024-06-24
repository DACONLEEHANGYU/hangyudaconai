import streamlit as st




# # 버튼을 렌더링하는 함수
# def render_html_button(text, page_number, pdf_path, key):
#     st.markdown(f"""
#         <button onclick="handleButtonClick({page_number}, '{pdf_path}', '{key}')">
#             {text}
#         </button>
#     """, unsafe_allow_html=True)


# st.markdown("""
#     <script>
#         function handleButtonClick(page_number, pdf_path, key) {
#             // Streamlit에 클릭 이벤트 전달
#             const buttonEvent = new CustomEvent('button-click', {
#                 detail: { page_number, pdf_path, key }
#             });
#             window.dispatchEvent(buttonEvent);
#         }

#         window.addEventListener('button-click', function(event) {
#             const { page_number, pdf_path, key } = event.detail;
#             const element = document.getElementById(key);
#             if (element) {
#                 element.click();
#             }
#         });
#     </script>
# """, unsafe_allow_html=True)


# def print_messages(messages_container, responses):    

#     if(responses == ""):
#         print("utils > responses: ", responses)

#     if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
#         for chat_message in st.session_state["messages"]:
#             with messages_container:
#                  messages_container.chat_message(chat_message["role"]).write(chat_message["content"])

#     if responses and 'context' in responses:
#         rag_boxes = messages_container.columns(len(responses['context']))
#         for idx, context in enumerate(responses['context']):
#             with rag_boxes[idx]:
#                 page_number = context.metadata.get("page", 1)
#                 pdf_path = context.metadata.get("data_code", "")
#                 key = f"source_button_{idx}"
                
#                 render_html_button(context.metadata['source'][:12], page_number, pdf_path, key)
            
#                 st.markdown(f"{context.page_content[:20]}...")                 
                 
# def update_pdf(page_number, pdf_path,messages_container, responses):    
#     print("update_pdf 함수 호출")
#     st.session_state.current_page = page_number
#     st.session_state.current_pdf = pdf_path
#     st.session_state.pdf_code = pdf_path
#     print(f"st.session_state.pdf_code : {st.session_state.current_page}")
#     print(f"st.session_state.pdf_code : {st.session_state.pdf_code}")

#     print_messages(messages_container, responses)
#     # create_source_buttons(response)



def print_messages(messages_container, responses):    

    if(responses == ""):
        print("utils > responses: ", responses)

    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
        for chat_message in st.session_state["messages"]:
            with messages_container:
                 messages_container.chat_message(chat_message["role"]).write(chat_message["content"])
                                  
                #  messages_container.chat_message(chat_message["role"]).write("hello")
            # 컴포넌트 형태로 출처 출력 가능

                 #messages_container.chat_message(chat_message["role"]).write("hello")

# def print_messages():
#   if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
#     for chat_message in st.session_state["messages"]:
#       st.chat_message(chat_message["role"]).write(chat_message["content"])