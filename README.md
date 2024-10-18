# Draught-chatbot
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

- ~~goto [model_config.py](src/draught_chatbot/config/model_config.py) and add API_KEY~~
- goto [model_config.py](src/draught_chatbot/config/model_config.py) and add selected model
- add API_KEY in web

## Start

```zsh
cd src
streamlit run web_app.py
```

## TODO

- [x] add API_KEY in web
- [x] add history
- [x] config optional model