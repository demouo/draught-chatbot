# draught-chatbot
llm-chatbot based on streamlit and LLM APIs

## Requirements

- streamlit
- zhipuai
- qianfan
- volcengine-python-sdk[ark]

```zsh
pip install streamlit zhipuai qianfan 'volcengine-python-sdk[ark]' 
```

## Configuration

- ~~前往 [model_config.py](src/draught_chatbot/config/model_config.py) 补充 API_KEY~~
- add API_KEY in web

## Start

```zsh
cd src
streamlit run web_app.py
```