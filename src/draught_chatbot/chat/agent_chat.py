from zhipuai import ZhipuAI
from ..config.model_config import ZHIPU_API_KEY

client = ZhipuAI(api_key=ZHIPU_API_KEY) # 请填写您自己的APIKey

def search_chat():
    response = client.chat.completions.create(
        model="glm-4-alltools",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content":[
                    {
                        "type":"text",
                        "text":"帮我查询2018年至2024年，每年五一假期全国旅游出行数据，并绘制成柱状图展示数据趋势。"
                    }
                ]
            }
        ],
        stream=True,
        tools=[
        {
            "type": "function",
            "function": {
                "name": "get_tourist_data_by_year",
                "description": "用于查询每一年的全国出行数据，输入年份范围(from_year,to_year)，返回对应的出行数据，包括总出行人次、分交通方式的人次等。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "description": "交通方式，默认为by_all，火车=by_train，飞机=by_plane，自驾=by_car",
                            "type": "string"
                        },
                        "from_year": {
                            "description": "开始年份，格式为yyyy",
                            "type": "string"
                        },
                        "to_year": {
                            "description": "结束年份，格式为yyyy",
                            "type": "string"
                        }
                    },
                    "required": ["from_year","to_year"]
                }
            }
        },
        {
            "type": "code_interpreter"
        }
        ]
    )

    for chunk in response:
        print(chunk)