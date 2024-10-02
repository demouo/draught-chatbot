# model_config.py
import os

# support models 
SUPPORT_MODEL_DICT = {
    "zhipu": ["GLM-4-plus","GLM-4-0520","GLM-4-flashX","GLM-4-flash", "glm-4",],
    "doubao": ["Doubao-pro-32k", ],
    "qianfan": ["ERNIE-Speed-128K", "ERNIE-Speed-8K", "ERNIE Speed-AppBuilder", "ERNIE-Lite-8K", "ERNIE-Lite-8K-0922", "ERNIE-Tiny-8K", "Yi-34B-Chat",],
    "zhipu-search": ["web-search-pro", ],
}

# api key 

APIKEY_CONFIG_PATH = "./draught_chatbot/config/apikey_config.json"
