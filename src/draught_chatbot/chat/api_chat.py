# api_chat.py

#### zhipu
from zhipuai import ZhipuAI
from ..config.model_config import ZHIPU_API_KEY
zhipu_client = ZhipuAI(api_key=ZHIPU_API_KEY)    

#### qianfan 
import os
import qianfan
# 通过环境变量初始化认证信息
# 方式一：【推荐】使用安全认证AK/SK鉴权
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk，如何获取请查看https://cloud.baidu.com/doc/Reference/s/9jwvz2egb
# os.environ["QIANFAN_ACCESS_KEY"] = "your_iam_ak"
# os.environ["QIANFAN_SECRET_KEY"] = "your_iam_sk"

# 方式二：【不推荐】使用应用AK/SK鉴权
# 替换下列示例中参数，将应用API_Key、应用Secret key值替换为真实值
# 已经在model-config填写了环境变量，直接使用即可
qianfan_client = qianfan.ChatCompletion()

#### doubao
from volcenginesdkarkruntime import Ark
from ..config.model_config import DOUBAO_MODEL_DICT
doubao_client = Ark(api_key=os.environ.get("ARK_API_KEY"))

# adapter
def api_chat(type, model, temperature, messages, stream):
    if type == "zhipu":
        resp = zhipu_client.chat.completions.create(model=model,temperature=temperature,messages=messages,stream=stream)
        if stream:
            for chunk in resp:
                yield chunk.choices[0].delta.content
        else:
            return resp.choices[0].content
    elif type == "doubao":
        resp = doubao_client.chat.completions.create(model=DOUBAO_MODEL_DICT[model],temperature=temperature,messages=messages,stream=stream)
        if stream:
            for chunk in resp:
                yield chunk.choices[0].delta.content
        else:
            return resp.choices[0].content
    elif type == "qianfan":
        # TODO 长度问题会有报错
        # qianfan messages 必须奇数长度  但是选历史的时候很难处理啊。 
        # 还是用长度割吧方便 而且不要原地修改
        # qianfan 不支持 system， 所以把system 拼接到 messages[1]（user）
        messages_copy = messages.copy()
        
        if len(messages_copy) & 1:
            messages_copy.pop(1)
        sys_msg = messages_copy[0]["content"]
        messages_copy[1]["content"] = sys_msg + "\n" + messages_copy[1]["content"]
        messages_copy = messages_copy[1:]
         
        resp = qianfan_client.do(model=model, messages=messages_copy, stream=stream, temperature=temperature)
        if stream:
            for chunk in resp:
                yield chunk["body"]["result"]
        else:
            return resp["body"]["result"]
    else:
        raise ValueError(f"不支持的模型类型: {type}")