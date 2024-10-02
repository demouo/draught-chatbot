import json
import requests
import uuid


api_key = "ZHIPU_API_KEY"

def search_chat(type, model, messages):
    msg = messages
    tool = model
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': api_key},
        timeout=300
    )
    
    return json.loads(resp.content.decode())
