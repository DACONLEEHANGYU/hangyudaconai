import os
import urllib.request
import uuid

import chromadb
import streamlit as st
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from streamlit_pdf_viewer import pdf_viewer

from retriever.multi_retriever import MultiRetriever
from utils import print_messages, create_source_boxes

# ChromaDB 연결
client = chromadb.HttpClient(host="220.76.216.228", port=8780, settings=Settings(allow_reset=True))
print(client.heartbeat())

# Collection 조회 예제
collections = client.list_collections()

st.set_page_config(layout="wide", page_title="DaconInfinityGPT", page_icon="🔗")

st.markdown(
  """
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap');
  
  .noto-sans-kr-<uniquifier> {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  }
  .st-emotion-cache-r421ms < .st-emotion-cache-1wmy9hl {
    background-color: #F0F0F0; /* 원하는 배경색 hex 코드 */
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
    background-color: #434AFA;
  }
  .st-emotion-cache-4oy321{
    background-color: #FFBD45;
  }
  .st-emotion-cache-bho8sy{
    background-color: #201c51;
  }
  .st-emotion-cache-4oy321 .st-emotion-cache-1flajlm{
  color: white;
  }
  .st-emotion-cache-1flajlm{
    font-family: "Noto Sans KR", sans-serif;
  }
  .st-emotion-cache-1ch8vux:hover{
    background-color: #8EB4E3;
  }
  .st-bb {
    font-family: "Noto Sans KR", sans-serif;
    background-color: transparent;
    # height: 50px;
    # line-height: 35px;    
  }
  .st-emotion-cache-vdokb0{
    font-family: "Noto Sans KR", sans-serif;
  }
  .st-emotion-cache-asc41u h1{
    color: #8EB4E3;
    font-size: 35px;
    padding: 0 0 10px 5px;
  }
  .st-emotion-cache-1jicfl2{
    background-color: white;
    border-radius: 30px;    
    padding-right: 6rem;
    padding-left: 6rem;
    padding-top: 0;
    height: 850px;
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
    color: white;
  }
  .st-emotion-cache-ml2xh6{
  line-height: 3.5;
  }
  .st-bb{
    font-weight: 400;
  }
  .st-c1{
    background-color: white !important;
  }
  .st-emotion-cache-vdokb0 p{
    font-weight: 600;
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
    box-shadow: 5px 5px 2px #d1c5b6;
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

# 초기 세션 상태 설정
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []
if "default_pdf" not in st.session_state:
  st.session_state.default_pdf = "./pdf_store/dpdf.pdf"

# PDF 뷰어 컴포넌트를 위한 키를 생성
if "pdf_viewer_key" not in st.session_state:
  st.session_state.pdf_viewer_key = 0

load_dotenv()
st.title("Dflex GPT")

chat_column, pdf_column = st.columns([4, 2.5])

if "messages" not in st.session_state:
  st.session_state['messages'] = []

if "current" not in st.session_state:
  st.session_state['current'] = {}


@st.cache_resource
def get_splitter():
  return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


@st.cache_resource
def get_embedding():
  model = "solar-embedding-1-large"
  return UpstageEmbeddings(api_key=os.getenv('UPSTAGE_API_KEY'), model=model)


@st.cache_resource
def get_vector_store(select_collection_name = "dacon11"):
  return Chroma(client=client, collection_name=select_collection_name, embedding_function=get_embedding())

def get_selected_collections():
  return ['DSET_AI_01', 'DSET_AI_02', 'DSET_AI_03', 'DSET_AI_05', 'DSET_AI_06', 'DSET_AI_07', 'DSET_AI_08', 'DSET_AI_09', 'DSET_AI_10']
def get_vector_stores():
  return [get_vector_store(collection) for collection in get_selected_collections()]

def get_multi_retriever():
  return MultiRetriever(vector_stores=get_vector_stores())

@st.cache_resource
def get_retriever(k=4, search_type='similarity'):
  return get_vector_store().as_retriever(search_type=search_type, search_kwargs={'k': k})

@st.cache_resource
def get_prompt():
  system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
  )
  return ChatPromptTemplate.from_messages(
    [
      ('system', system_prompt),
      ('human', '{input}'),
    ]
  )


@st.cache_resource
def get_model():
  return ChatUpstage(api_key=os.getenv('UPSTAGE_API_KEY'))
  # return ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

@st.cache_resource
def get_chain():
  qa_chain = create_stuff_documents_chain(get_model(), get_prompt())
  return create_retrieval_chain(get_multi_retriever(), qa_chain)


if 'selected_pdf_path' not in st.session_state:
  st.session_state.selected_pdf_path = "./pdf_store/dpdf.pdf"


def update_pdf(page_number, code, source):
  print(f"update_pdf 함수 호출, path : {code}, page_number : {page_number}, source: {source}")
  st.session_state['current']['page'] = page_number
  st.session_state['current']['source'] = source
  st.session_state['current']['code'] = code

chain = get_chain()

with chat_column:
  with st.container(border=True):
    message_container = st.container(height=640)
    print_messages(message_container, show_pdf=update_pdf)

  with st.container():
    if prompt := st.chat_input("메시지를 입력해 주세요.", args=(None,)):
      message_container.chat_message("user").write(f"{prompt}")
      st.session_state["messages"].append({"message":{"role": "user", "content": prompt}})

      response = chain.invoke({'input': prompt})
      answer = response['answer']
      metadata = response['context'][0].metadata

      st.session_state['current']['page'] = metadata["page"]
      st.session_state['current']['source'] = metadata["source"]
      st.session_state['current']['code'] = metadata["data_code"]

      message_container.chat_message("assistant").write(answer)
      if 'context' in response:
        create_source_boxes(message_container, response['context'], update_pdf)

      st.session_state["messages"].append({
        "message":{
          "role": "assistant", "content": answer
        },
        "context": response['context']
      })

with pdf_column:
  with st.container(border=True) as pdf_name_container:
    with st.container():
      pdf_img_col, pdf_content_col = st.columns([1, 3])
      with pdf_img_col:
        st.image("free-icon-pdf.png", width=40, clamp=False)
      with pdf_content_col:
        st.markdown(
          f"""
            <div style="
                white-space: nowrap;
                 overflow: hidden;
                 text-overflow: ellipsis;
                max-width: 100%;
                    ">
              {st.session_state['current']['source'] if 'source' in st.session_state['current'] else ''}
            </div>
          """,
          unsafe_allow_html=True)

    # rnd -> pdf
    pdf_url = "./pdf_store/dpdf.pdf"

    pdf_main_container = st.empty()
    with pdf_main_container:
      # rnd 서버 연결
      if 'code' in st.session_state['current'] and st.session_state['current']['code'] != "":
        pdf_url = f"http://{os.getenv('RND_SERVER')}/dflex/{st.session_state['current']['code']}"
        with urllib.request.urlopen(pdf_url) as pdf_file:
          pdf_viewer(pdf_file.read(), pages_to_render=[st.session_state['current']['page']], height=630, width=700, key=str(uuid.uuid1()))
      else:
        pdf_viewer(st.session_state.default_pdf, height=630, width=700)