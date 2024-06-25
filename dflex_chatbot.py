import os
import urllib.request
import uuid

import chromadb
import streamlit as st
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.retrievers import EnsembleRetriever


from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import ChatUpstage
from langchain_upstage import UpstageEmbeddings
from streamlit_pdf_viewer import pdf_viewer

from retriever.multi_retriever import MultiRetriever
from qa_utils import print_messages, create_source_boxes

if 'sbstate' not in st.session_state:
    st.session_state.sbstate = 'collapsed'

st.set_page_config(layout="wide", page_title="DaconInfinityGPT", page_icon="🔗", initial_sidebar_state=st.session_state.sbstate)

st.markdown(
  """
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap');
  .st-emotion-cache-1wwcybw{
   # 사이드바 x 버튼
    color: white;
  }
  .st-emotion-cache-7ym5gk{
    background-color: #d4e6f5;    
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
    background-color: #161616 !important;
    # box-shadow: 5px 5px 2px #d1c5b6;
    font-weight: bold;
    border: none;
  }
  .st-emotion-cache-qeahdt h1{
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
    border: 1px solid;
    border-radius: 10px;
    gap: 0.5rem;
  }
  .st-emotion-cache-1anz8uz{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    border: 1px solid;
    border-radius: 10px;
    gap: 0.5rem;
  }
  .st-emotion-cache-12hhi06{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    border: 1px solid;
    border-radius: 10px;
    gap: 0.5rem;
  }
  .st-emotion-cache-phzz4j{
    width: 208.938px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    border: 1px solid;
    border-radius: 10px;
    gap: 0.5rem;
  }
  .st-emotion-cache-6o6feu{
    background-image: url('./pdf_store/dacon_logo.jpg');
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
  .st-emotion-cache-asc41u h1{
    color: #3777c5;
    font-size: 20px;
    padding: 0 0 10px 5px;
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


with st.sidebar:
  st.title("DB 카테고리 선택")
  st.checkbox("지식재산권",value=True, key="DSET_AI_01_check")
  st.checkbox("표준화",value=True, key="DSET_AI_02_check")
  st.checkbox("의료데이터",value=True, key="DSET_AI_03_check")
  st.checkbox("데이터기반행정",value=True, key="DSET_AI_05_check")
  st.checkbox("관리지침",value=True, key="DSET_AI_06_check")
  st.checkbox("데이터 3법 개정안",value=True, key="DSET_AI_07_check")
  st.checkbox("자치법규",value=True, key="DSET_AI_08_check")
  st.checkbox("ICT",value=True, key="DSET_AI_09_check")
  st.checkbox("빅데이터",value=True, key="DSET_AI_10_check")

# 초기 세션 상태 설정
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []
if "default_pdf" not in st.session_state:
  st.session_state.default_pdf = "./pdf_store/dpdf.pdf"

# 초기상태에서 이미지를 보여주기 위한 변수
if "show_initial_image" not in st.session_state:
    st.session_state.show_initial_image = True     

# PDF 뷰어 컴포넌트를 위한 키를 생성
if "pdf_viewer_key" not in st.session_state:
  st.session_state.pdf_viewer_key = 0

if "collection_name" not in st.session_state:
     st.session_state.collection_name = "dacon11" 


load_dotenv()
st.title("Dflex GPT")

chat_column, pdf_column = st.columns([5, 3])

select_collection_name = "dacon11"

if "messages" not in st.session_state:
  st.session_state['messages'] = []

if "current" not in st.session_state:
  st.session_state['current'] = {}


def get_selected_collections():
    selected_collections = []
    if st.session_state["DSET_AI_01_check"]:
        selected_collections.append("DSET_AI_01")
    if st.session_state["DSET_AI_02_check"]:
        selected_collections.append("DSET_AI_02")
    if st.session_state["DSET_AI_03_check"]:
        selected_collections.append("DSET_AI_03")
    if st.session_state["DSET_AI_05_check"]:
        selected_collections.append("DSET_AI_05")
    if st.session_state["DSET_AI_06_check"]:
        selected_collections.append("DSET_AI_06")
    if st.session_state["DSET_AI_07_check"]:
         selected_collections.append("DSET_AI_07")
    if st.session_state["DSET_AI_08_check"]:
          selected_collections.append("DSET_AI_08")
    if st.session_state["DSET_AI_09_check"]:
          selected_collections.append("DSET_AI_09")
    if st.session_state["DSET_AI_10_check"]:
          selected_collections.append("DSET_AI_10")                                                 
    return selected_collections if selected_collections else ["dacon11"]



@st.cache_resource
def get_splitter():
  return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


@st.cache_resource
def get_embedding():
  model = "solar-embedding-1-large"
  return UpstageEmbeddings(api_key=os.getenv('UPSTAGE_API_KEY'), model=model)



def get_vector_store(collection_name):
  client = chromadb.HttpClient(host=os.getenv('RND_SERVER'), port=8780, settings=Settings(allow_reset=True))
  # print(client.heartbeat())
  # print(f"collection_name: {collection_name}")

  return Chroma(client=client, collection_name=collection_name, embedding_function=get_embedding())


def get_retriever(k=4):
    selected_collections = get_selected_collections()
    
    if len(selected_collections) == 1:
        return get_vector_store(selected_collections[0]).as_retriever(search_type='similarity_score_threshold', search_kwargs={'k': k, "score_threshold" : 0.1})
    else:
        retrievers = [
            get_vector_store(collection).as_retriever(search_type='similarity_score_threshold', search_kwargs={'k': k, "score_threshold" : 0.1})
            for collection in selected_collections
        ]
        print(f"retrievers: {len(retrievers)}")
        weights = [1.0 / len(retrievers)] * len(retrievers)
        return EnsembleRetriever(retrievers=retrievers, weights=weights)      

def get_vector_stores():
  return [get_vector_store(collection) for collection in get_selected_collections()]

def get_multi_retriever():
  return MultiRetriever(vector_stores=get_vector_stores())


# @st.cache_resource
# def get_prompt():
#   system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you "
#     "don't know. Use three sentences maximum and keep the "
#     "answer concise. If you cannot find the answer in the provided context, say 'I don't know.'"
#     "\n\n"
#     "{context}"
#   )
#   return ChatPromptTemplate.from_messages(
#     [
#       ('system', system_prompt),
#       ('human', '{input}'),
#     ]
#   )

@st.cache_resource
def get_prompt():
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Your responses should be based solely on the provided context. "
        "If the necessary information is not present in the context, "
        "or if the context is empty, always respond with 'I don't have enough information to answer that question.' "
        "When you do have relevant information in the context, use it to answer "
        "the question concisely, using no more than three sentences. "
        "Be direct and to the point in your responses.\n\n"
        "Context: {context}\n\n"
        "Question: {input}\n\n"
        "Answer: "
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


if 'selected_pdf_path' not in st.session_state:
  st.session_state.selected_pdf_path = "./pdf_store/dpdf.pdf"


def get_chain():
  retriever = get_multi_retriever()  
  qa_chain = create_stuff_documents_chain(get_model(), get_prompt())
  return create_retrieval_chain(retriever, qa_chain)


def update_pdf(page_number, code, source):
  print(f"update_pdf 함수 호출, path : {code}, page_number : {page_number}, source: {source}")
  st.session_state['current']['page'] = page_number
  st.session_state['current']['source'] = source
  st.session_state['current']['code'] = code

def update_category():
    global select_collection_name
    selected_option = st.session_state["suggestion_box"]
    
    if selected_option == "카테고리":
        select_collection_name = "dacon11"
    elif selected_option == "지식재산권":
        select_collection_name = "DSET_AI_01"
    elif selected_option == "표준화":
        select_collection_name = "DSET_AI_02"
    elif selected_option == "의료데이터":    
         select_collection_name = "DSET_AI_03"    
    elif selected_option == "데이터기반행정":
         select_collection_name = "DSET_AI_05"      
    elif selected_option == "관리지침":
        select_collection_name = "DSET_AI_06"
    elif selected_option == "데이터 3법 개정안":
        select_collection_name = "DSET_AI_07"
    elif selected_option == "자치법규":
        select_collection_name = "DSET_AI_08"
    elif selected_option == "ICT":
        select_collection_name = "DSET_AI_09"
    elif selected_option == "빅데이터":
        select_collection_name = "DSET_AI_10"                                           

    # 다른 카테고리에 대한 처리도 추가
       
    st.session_state.collection_name = select_collection_name
    # 벡터 스토어 재생성
    st.session_state.vector_store = get_vector_store(select_collection_name)


chain = get_chain()

options = ["전체", "지식재산권", "표준화", "의료데이터", "데이터기반행정", "관리지침", "데이터 3법 개정안", "자치법규", "ICT", "빅데이터" ]

with chat_column:  
  message_container = st.container(height=770)
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
          pdf_viewer(pdf_file.read(), pages_to_render=[st.session_state['current']['page']], height=730, width=700, key=str(uuid.uuid1()))
      else:
        pdf_viewer(st.session_state.default_pdf, height=730, width=700)