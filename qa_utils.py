import uuid
import re

import streamlit as st

def process_string(input_string):
  # 공백을 한 칸으로 만드는 작업
  input_string = re.sub(r'\s+', ' ', input_string).strip()
  
  # 결과를 저장할 변수
  content = []
  
  # 문자열을 순회하며 각각의 문자를 분류
  for char in input_string:
      if re.match(r'[가-힣]', char):
          content.append(char)
      elif re.match(r'[a-zA-Z]', char):
          content.append(char)
      elif re.match(r'[0-9]', char):
          content.append(char)

  
  return ' '.join(content)


def extract_string(text):
  # 한글, 알파벳, 숫자를 포함하는 정규 표현식 패턴
  pattern = re.compile(r'[가-힣a-zA-Z0-9]+')
  # 패턴에 매칭되는 모든 문자열을 리스트로 반환하고, 이를 합쳐서 하나의 문자열로 반환
  result = ' '.join(pattern.findall(text))
  return result

def create_source_card(context, rag_box, show_pdf, source_length=15, content_length=30):
  with rag_box:
    page_number = context.metadata.get('page', 1)
    pdf_path = context.metadata.get('data_code', "")
    source = context.metadata.get('source', "")
    score = context.metadata.get('score', 0.0)
    st.button(
      f"{context.metadata['source'][:15]}",
      use_container_width=True,
      on_click=show_pdf,
      args=(page_number, pdf_path, source),
      help=context.metadata['source'],
      key=str(uuid.uuid1()
      )
    )
    st.markdown(f"{extract_string(context.page_content)[:50]}...")
    if len(extract_string(context.page_content)[:50]) < 50:
      print(context.page_content) 
    st.markdown(f"유사도 : :blue-background[{round(score,3)}]")


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


def create_rag_card(rag_context):
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


