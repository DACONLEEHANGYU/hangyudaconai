import uuid

import streamlit as st


def create_source_card(context, rag_box, show_pdf, source_length=15, content_length=30):
  with rag_box:
    page_number = context.metadata.get('page', 1)
    pdf_path = context.metadata.get('data_code', "")
    source = context.metadata.get('source', "")

    st.button(
      f"{context.metadata['source'][:source_length]}",
      on_click=show_pdf,
      args=(page_number, pdf_path, source),
      help=context.metadata['source'],
      key=str(uuid.uuid1())
    )
    st.markdown(f"{' '.join(context.page_content.split())[:35]}...")


def create_source_boxes(container, contexts, show_pdf):
  rag_boxes = container.columns(len(contexts))
  for idx, context in enumerate(contexts):
    create_source_card(context, rag_boxes[idx], show_pdf)

# def create_source_boxes(container, contexts, show_pdf):
#   # 최대 4개의 박스만 생성
#   max_boxes = 4
#   num_boxes = min(len(contexts), max_boxes)
#   rag_boxes = container.columns(num_boxes)
#   for idx in range(num_boxes):
#     create_source_card(contexts[idx], rag_boxes[idx], show_pdf)


def print_messages(messages_container, show_pdf):
  if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
    with messages_container:
      for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message['message']["role"]).write(chat_message['message']["content"])
        if 'context' in chat_message:
          create_source_boxes(messages_container, chat_message['context'], show_pdf)


def print_messages_basic():
  for chat_message in st.session_state["messages"]:
    print(chat_message)
    if isinstance(chat_message, dict):
      st.chat_message(chat_message['role']).write(chat_message['content'])
    else:
      st.chat_message(chat_message.role).write(chat_message.content)


def init_css():
  # CSS 스타일 정의
  st.markdown(
    """
      <style>
      .rag_button {
        border: 0px;
      }
      .container {
          border: 1px solid #4CAF50;
          border-radius: 10px;
          width: 150px;
      }
      .title {
          font-weight: bold;
          font-size: 1.25rem;
      }
      .content {
          font-size: 0.875rem;
      }
      </style>
      """,
    unsafe_allow_html=True
  )


def create_rag_card(rag_context):
  init_css()
  st.markdown(
    f"""
      <button class="rag_button" onclick="handleClick()">
        <div class="container">
            <div class="title">{rag_context.metadata['source'][:15]}</div>
            <div class="content">{rag_context.page_content[:40]}</div>
        </div>
      </button>
      <script>
      function handleClick() {{
          console.log({rag_context.metadata['source'][:15]});
      }}
      </script>
    """,
    unsafe_allow_html=True
  )