# CHATGPT Clone
- install
``` 
python.exe -m pip install --upgrade pip
pip install streamlit
pip install langchain
pip install langserve[all] 
pip install python-dotenv
pip install notebook
pip install langchain_community
pip install langchain-openai
```
- config
  - create `.env`
  - config `LANGSERVE_ENDPOINT`
  ``` 
  LANGSERVE_ENDPOINT = "http://1.1.1.1:1111/example/" 
  ```