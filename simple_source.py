import os
import bs4
import re
import streamlit as st
import urllib.request
from streamlit_pdf_viewer import pdf_viewer
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_upstage import UpstageEmbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import RemoteRunnable
import chromadb
from chromadb.config import Settings
from chromadb import Client
from PyPDF2 import PdfReader,PdfWriter
import requests
import tempfile
import fitz

from utils import print_messages

# ChromaDB 연결
client = chromadb.HttpClient(host=os.getenv("RND_SERVER"), port=8780, settings=Settings(allow_reset=True))
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
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = "./pdf_store/dpdf.pdf"
if "current_page" not in st.session_state:
    st.session_state.current_page = 1
if "pdf_code" not in st.session_state:
    st.session_state.pdf_code = ""

# PDF 뷰어 컴포넌트를 위한 키를 생성
if "pdf_viewer_key" not in st.session_state:
    st.session_state.pdf_viewer_key = 0    
     


load_dotenv()
st.title("Dflex GPT")

col1, col3 = st.columns([4, 2.5])

select_collection_name = "dacon11" 

if "messages" not in st.session_state:
     st.session_state["messages"] = []




@st.cache_resource
def get_splitter():
        return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

@st.cache_resource
def get_embedding():
        model = "solar-embedding-1-large"
        return UpstageEmbeddings(api_key=os.getenv('UPSTAGE_API_KEY'), model=model)

@st.cache_resource
def get_vector_store():
       
        return Chroma(client=client, collection_name=select_collection_name, embedding_function=get_embedding())

@st.cache_resource
def get_retriever(k=4):
        return get_vector_store().as_retriever(search_type="similarity", search_kwargs={"k": k})

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
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

@st.cache_resource
def get_model():
        return ChatUpstage(api_key=os.getenv('UPSTAGE_API_KEY'))

if "selected_pdf_path" not in st.session_state:
    st.session_state.selected_pdf_path = "./pdf_store/dpdf.pdf"

@st.cache_resource
def get_chain():

         qa_chain = create_stuff_documents_chain(get_model(), get_prompt())
         return create_retrieval_chain(get_retriever(), qa_chain)

options = ["카테고리", "표준화", "데이콘휴가", "지식재산권", "데이터기반행정", "관리지침", "빅데이터", "ICT", "의료데이터", "자치법규" ]

def update_prompt(prompt):
    global options  # 전역 변수 사용
    if prompt == "/":
        st.session_state["suggestion_box"] = st.selectbox("옵션을 선택하세요:", options, label_visibility="hidden", key="suggestion_box")
    else:
        if "suggestion_box" in st.session_state:
            del st.session_state["suggestion_box"]


def update_pdf(page_number, pdf_path):    
    print(f"update_pdf 함수 호출, path : {pdf_path}, page_number : {page_number}")
    
    st.session_state.current_page = page_number
    st.session_state.current_pdf = pdf_path
    st.session_state.pdf_code = pdf_path

    print_messages(messages, response)    
    create_source_buttons(response)

def create_source_buttons(response):
    if response and 'context' in response:
        rag_boxes = messages.columns(len(response['context']))
        for idx, context in enumerate(response['context']):
            with rag_boxes[idx]:
                page_number = context.metadata.get("page", 1)
                pdf_path = context.metadata.get("data_code", "")
                
                if st.button(f"{context.metadata['source'][:12]}", key=f"source_button_{idx}",
                             on_click=update_pdf, args=(page_number, pdf_path)):
                    pass
            
                st.markdown(f"{context.page_content[:20]}...")    


# 선택된 pdf
select_pdf = './pdf_store/dpdf.pdf'
result_pdf =''

pdf_page = 1
pdf_name =''

with col1:
    with st.container(border=True):
        messages = st.container(height=640)

    input_container = st.container()
    with input_container:
          prompt = st.chat_input("메시지를 입력해 주세요.", on_submit=update_prompt, args=(None,))
   
    if prompt:        
        print_messages(messages, "")
        messages.chat_message("user").write(f"{prompt}")      
        chain = get_chain()
        st.session_state["messages"].append({"role": "user", "content":prompt})


        response = chain.invoke({"input": prompt})

        msg = response
        answer = response['answer']
       
        metadata = msg['context'][0].metadata

        pdf_page = metadata["page"]
        pdf_name = metadata["source"]                
        st.session_state.pdf_code = metadata["data_code"]

        messages.chat_message("assistant").write(response['answer'])        
        create_source_buttons(response)

        st.session_state["messages"].append({"role": "assistant", "content": answer})

  

with col3:    
    with st.container(border=True):     

        pdf_name_container = st.container() 
        with pdf_name_container:
              col1, col2 = st.columns([1, 3])
              with col1:
                st.image("free-icon-pdf.png", width=40, clamp=False) 
              with col2:
                # st.write(pdf_name)        
                st.markdown(
                    f"""
                <div style="
                    white-space: nowrap;
                     overflow: hidden;
                     text-overflow: ellipsis;
                    max-width: 100%;
                        ">
                  {pdf_name}
                </div>
                    """,
                    unsafe_allow_html=True)

        # rnd -> pdf    
        pdf_url = "./pdf_store/dpdf.pdf"        
  

        pdf_main_container = st.container()
        with pdf_main_container:
                
                # rnd 서버 연결
                if(st.session_state.pdf_code != ""):
                   
                    pdf_url = f"http://{os.getenv('RND_SERVER')}/dflex/{st.session_state.pdf_code}"
                    with urllib.request.urlopen(pdf_url) as pdf_file:
                        pdf_viewer(pdf_file.read(),pages_to_render=[pdf_page], height=630, width=700)
                            
                else:
                   
                    pass
                    pdf_viewer(pdf_url, height=630, width=700)                
                      