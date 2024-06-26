import streamlit as st


def init_css():
  st.markdown(
  """
  <style>
  [data-testid="stHeader"]{
    /* 기본 헤더 삭제 */
     display: none;
  }  
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap');

  [data-testid="stCheckbox"] span{
    background-color: #2d6ed3;
    border: black
  }
  [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] [data-testid="column"]{
    border: 1px solid #b1b0bb;
    border-radius: 10px;
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
    padding-left: 35px;
    margin-bottom: 30px;    
  }
  [data-testid="stSidebarHeader"]{  
    padding: 5px 13px 0px 0px;
  }
  [data-testid="baseButton-secondary"]{
    /* 출처 버튼 hover */
    background-color: #e5f1ff;
    color: #e5f1ff;
  }  
  [data-testid="baseButton-secondary"]:hover{
     /* 출처 버튼 hover */
     border-color: #8EB4E3;
     color: #8EB4E3;
  }
  [data-testid="baseButton-secondary"]:active{  
     /* 출처 버튼 active */
     border-color: #8EB4E3;
     background-color: #aeaeef;
     color: #8EB4E3;      
  }
  [data-testid="baseButton-secondary"]:focus:not(:active){
    border-color: #8EB4E3;     
    color: #8EB4E3;
  }
  [data-testid="stChatInput"] div{
    /* input box */ 
    border-color: #f0f2f5 !important
  }
  [data-testid="stChatInput"] div:active{
    /* input box 액티브 상태 */ 
    border-color: #8EB4E3 !important;
  }
  [data-testid="stChatInputSubmitButton"]:hover{
    background-color: #8EB4E3;
  }
  #dflex-chat{  
    /* 타이틀 */
    color: #3777c5;
    font-size: 23px;
    padding: 13px 0 0px 2px;    
  }
  [data-testid="stSidebarContent"]{
    background-color : #011223e3
    /*background-color: #c3c2c24f;*/
  }
  [data-testid="stWidgetLabel"] [data-testid="stMarkdownContainer"] p{
    /* 사이드바 텍스트 */
    color: white;
  }
  [data-testid="stAlert"]{
    display: none;
  }
  [data-testid="stSidebarCollapseButton"]{
    color: white;
  }
  [data-testid="stVerticalBlockBorderWrapper"]{
    border-color: #c7baba;
    border-radius: 10px;
  }  
  [data-testid="StyledFullScreenButton"]{
     visibility: hidden;
  }
  [data-testid="stChatInputTextArea"]{
    background-color: #e4e4e7;
  } 
  [data-testid="chatAvatarIcon-assistant"]{
    background-color: #201c51;
  }
  [data-testid="stChatMessage"]:nth-child(1), 
  [data-testid="stChatMessage"]:nth-child(3n+1) {
    background-color: #efefef; !important;
  }
  [data-testid="stChatMessage"]:nth-child(3n+2) {
    background-color: #dbdceb;
    padding-right: 30px;
  }
  .noto-sans-kr-<uniquifier> {
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
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
  [data-testid="stMarkdownContainer"] p{
    word-break: break-all;
    color: black;
  }
  [data-testid="stMarkdownContainer"]{
    font-family: "Noto Sans KR", sans-serif;
    padding-left: 5px;
  }
  [data-testid="stAppViewBlockContainer"]{
    /* 전체 화면 패딩 */
    padding: 0 6rem 0 6rem;
  }
  [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"]{
    /* 박스 쉐도우 */
  }  
  /*.st-emotion-cache-r421ms{
    background-color: white;
    box-shadow: 5px 5px 2px #d1c5b6;
  }*/
  [data-testid="baseButton-secondary"] {
    /* 버튼 패딩 */
    padding: 0;
  }
  p{
    font-family: "Noto Sans KR", sans-serif;
  }
</style>
  """,
  unsafe_allow_html=True,
)