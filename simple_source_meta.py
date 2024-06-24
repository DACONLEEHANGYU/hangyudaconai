import os

import bs4
import streamlit as st
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import RemoteRunnable

from utils import print_messages

load_dotenv()

st.set_page_config(page_title="DaconInfinityGPT", page_icon="🔗")
st.title("DaconInfinityGPT, What is Task Decomposition?")

if "messages" not in st.session_state:
  st.session_state["messages"] = []

document_url="https://lilianweng.github.io/posts/2023-06-23-agent/"
@st.cache_resource
def get_docs(url):
  # 1. Load, chunk and index the contents of the blog to create a retriever.
  loader = WebBaseLoader(
    web_paths=(url,),
    bs_kwargs=dict(
      parse_only=bs4.SoupStrainer(
        class_=("post-content", "post-title", "post-header")
      )
    ),
  )
  return loader.load()

@st.cache_resource
def get_splitter():
  return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

@st.cache_resource
def get_split_docs():
  return get_splitter().split_documents(get_docs(document_url))

@st.cache_resource
def get_embedding():
  model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
  gpt4all_kwargs = {'allow_download': 'True'}
  return GPT4AllEmbeddings(model_name=model_name, gpt4all_kwargs=gpt4all_kwargs)

@st.cache_resource
def get_vector_store():
  return Chroma.from_documents(documents=get_split_docs(), embedding=get_embedding())

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
  return RemoteRunnable(os.getenv('LANGSERVE_ENDPOINT'))

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

@st.cache_resource
def get_chain():
  qa_chain = create_stuff_documents_chain(get_model(), get_prompt())
  return create_retrieval_chain(get_retriever(), qa_chain)


# 이전 대화기록 출력
print_messages()

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

if user_input := st.chat_input("메시지를 입력해 주세요."):
  st.chat_message("user").write(f"{user_input}")
  st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

  response = get_chain().invoke({"input": user_input})
  with st.chat_message("assistant"):
    msg = response

    st.write(msg['answer'])
    rag_boxes = st.columns(len(msg['context']))
    for idx, context in enumerate(msg['context']):
      with rag_boxes[idx]:
        st.markdown(
          f"""
            <button class="rag_button" onclick="handleClick()">
              <div class="container">
                  <div class="title">{document_url[:12]}</div>
                  <div class="content">{context.page_content[:40]}</div>
              </div>
            </button>
            <script>
            function handleClick() {{
                console.log({document_url});
            }}
            </script>
          """,
          unsafe_allow_html=True
        )
    st.session_state["messages"].append(ChatMessage(role="assistant", content=msg['answer']))
