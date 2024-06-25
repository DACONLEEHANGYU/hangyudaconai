import uuid

import streamlit as st


def create_source_card(context, rag_box, show_pdf, source_length=15, content_length=30):
  with rag_box:
    page_number = context.metadata.get('page', 1)
    pdf_path = context.metadata.get('data_code', "")
    source = context.metadata.get('source', "")
    score = context.metadata.get('score', 0.0)
    st.button(
      f"{context.metadata['source'][:16]}...",
      use_container_width=True,
      on_click=show_pdf,
      args=(page_number, pdf_path, source),
      help=context.metadata['source'],
      key=str(uuid.uuid1()
      )
    )
    st.markdown(f"{' '.join(context.page_content.split())[:30]}...")
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


def init_css():
  st.markdown(
  """
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap');
  .st-emotion-cache-1wwcybw{
   # 사이드바 x 버튼
    color: white;
  }
  .st-emotion-cache-12w0qpk{
    width: calc(25% - 1rem);
    flex: 1 1 calc(25% - 1rem);
    border: 1px solid #b1b0bb;
    border-radius: 10px;
  }
  .st-emotion-cache-7ym5gk{
    background-color: #d4e6f5;    
  }
  [data-testid="stCheckbox"] span{
    background-color: black;
  }
  [data-testid="stSidebarContent"] h1{  
    /* 사이드바 타이틀 */
    font-family:  "Noto Sans KR", sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    border: 1px solid black;
    background: white;
    border-radius: 20px;
    padding: 5px;
    padding-left: 20px;
    margin-bottom: 30px;    
  }
  [data-testid="stSidebarHeader"]{
    padding: 5px 13px 0px 0px;
  }
  #dflex-gpt{  
    /* 타이틀 */
    color: #3777c5;
    font-size: 23px;
    padding: 10px 0 0px 2px;    
  }
  .st-emotion-cache-nunl0c{
    # 사이드바 접었을 때 출처카드 
    width: 200.312px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0.5rem;
    border: 1px solid #e5dcdc;
    border-radius: 9px;
  }  
  .st-emotion-cache-j6qv4b p{
    color: black;
  }
  .st-emotion-cache-j6qv4b{
    # 사이드바 텍스트
    font-family: "Noto Sans KR", sans-serif;
    color: aliceblue;
  }
  .st-at{
    #background-color: #161616 !important;
    # box-shadow: 5px 5px 2px #d1c5b6;
    font-weight: bold;
    border: none;
  }

  .st-emotion-cache-y4bq5x{
    background-color: #5b7cfd00 !important
  }
  .st-emotion-cache-1gv3huu{
    background-color: #eef0f9 !important;
  } 
  .st-emotion-cache-lip6wq{
    border: 2px solid #e5dcdc;
    border-radius: 10px;
  }
  .st-emotion-cache-ouq56e{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0.5rem;
  }
  .st-emotion-cache-1anz8uz{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0.5rem;
  }
  .st-emotion-cache-12hhi06{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;  
    gap: 0.5rem;
  }
  .st-emotion-cache-phzz4j{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0.5rem;
  }
  .st-emotion-cache-6o6feu{
    background-image: url("./pdf_store/dacon_logo.jpg");
    background-color: white;
    border: 1px solid #e5dcdc;
  }
 
  .st-emotion-cache-bome3c{
    # content 영역 
    border: 1px solid #77758d94;
  }
  .st-emotion-cache-vt4dha{
    border: 2px solid #e5dcdc;
    border-radius: 10px;
    gap: 0.5rem;
  }
  .st-emotion-cache-7ym5gk:hover{
    border-color: rgb(78 127 243);
    color: rgb(78 127 243);
  }
  .st-emotion-cache-7ym5gk:focus:not(:active){
    border-color: rgb(78 127 243);
    color: rgb(78 127 243);
  }
  .st-emotion-cache-7ym5gk:active{
    border-color: rgb(78 127 243);
    background-color: #99cdf9;
  }
  .st-bt{
    background-color: white;
  }
  .st-emotion-cache-1kv1lyy{
    align-items: flex-end;
  }
  [data-testid="StyledFullScreenButton"]{
     visibility: hidden;
  }
  [data-testid="stChatInputTextArea"]{
    background-color: #f2f2f5;
  }
  .noto-sans-kr-<uniquifier> {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  }
  .st-emotion-cache-1h6yrjv{
    background-color: #f3f3f3;    
}
  .st-emotion-cache-r421ms < .st-emotion-cache-1wmy9hl {
    background-color: #F0F0F0; /* 원하는 배경색 hex 코드 */
  }
  .st-emotion-cache-s1k4sy{
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  .reportview-container .markdown-text-container {
    font-family: monospace;    
  }
  .sidebar .sidebar-content {
    background-image: linear-gradient(#ececfb, #f5f5f5)
    color: white;
  }
  .Widget>label {
    color: white;
    font-family: monospace;
  }
  [class^="st-b"]  {
    color: white;
    font-family: monospace;
  }
  .st-emotion-cache-1c7y2kd{
    background-color: #d6d7ef;
  }
  .st-emotion-cache-4oy321{
    background-color: #ebe9f5;
  }
  .st-emotion-cache-bho8sy{
    background-color: #201c51;
  }
  .st-emotion-cache-4oy321 .st-emotion-cache-1flajlm{
  color: black;
  }
  .st-emotion-cache-1flajlm{
    font-family: "Noto Sans KR", sans-serif;
  }
  .st-emotion-cache-1ch8vux:hover{
    background-color: #8EB4E3;
    color: #8EB4E3;
  }
  .st-bb {
    font-family: "Noto Sans KR", sans-serif;
    background-color: transparent;
    # height: 50px;
    # line-height: 35px;    
  }
  .st-emotion-cache-vdokb0{
    font-family: "Noto Sans KR", sans-serif;
    padding-left: 10px;
  }  
  .st-emotion-cache-1jicfl2{    
    padding-right: 6rem;
    padding-left: 6rem;
    padding-top: 0;
    height: 910px;
  }
  .st-emotion-cache-r421ms{
    background-color: white;
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  .st-emotion-cache-1yiq2ps{    
    # padding-right: 200px;
    # padding-left: 200px;
    # background : #8EB4E3;
  }
  .st-emotion-cache-19z6gzv{    
    background: #201c51;
  }
  .st-emotion-cache-wnrclc{
    width: 50px;    
    flex: none;
  }
  .st-emotion-cache-1c7y2kd p{
    color: black;
  }
  .st-emotion-cache-ml2xh6{
  line-height: 3.5;
  }
  .st-bb{
    font-weight: 400;
  }
  .st-c1{
    # background-color: white !important;
  }
  .st-emotion-cache-vdokb0 p{
    font-weight: 400;
    padding-right: 30px;
  }
  p{
    font-family: "Noto Sans KR", sans-serif;
  }
  .st-c2{    
    border-right-color: #8EB4E3 !important;
  }
  .st-c3{
    border-left-color: #8EB4E3 !important;
  }
  .st-emotion-cache-ue6h4q{
  display: none;
  }
  .st-c4{
    border-right-color: #8EB4E3 !important;
  }
  .st-c5{
    border-top-color: #8EB4E3 !important;
    border-bottom-color: #8EB4E3 !important;
  }
  .st-c6{
    border-bottom-color: #8EB4E3 !important;
  }
  .st-at {
    background-color: white;
    #box-shadow: 5px 5px 2px #d1c5b6;
    font-weight: bold;
  }
  .st-di{
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  .st-db{
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  [class^="st-b"]{
    color:#5a6d85;
    font-family: "Noto Sans KR", sans-serif;
  }
  .st-emotion-cache-5wnhd9{
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  textarea {
    background-color: #f2f2f5;
  }
  .st-emotion-cache-81d6d7{
    box-shadow: 5px 5px 2px #d1c5b6;
  }
  footer {
    font-family: monospace;
  }
  .reportview-container .main footer, .reportview-container .main footer a {    
  }
  header .decoration {
    background-image: none;    
  }
  .st-emotion-cache-12fmjuu{
  display: none;
  }
  
  </style>
  """,
  unsafe_allow_html=True,
)



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