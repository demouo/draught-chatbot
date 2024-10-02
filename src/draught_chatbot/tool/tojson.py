import json
from ..config.web_config import OUR_FILE_ID
def jsonl_to_jsonlist(jsonl_file):
    ans = []
    for line in jsonl_file:
        
        try:
            line = line.decode("utf-8")
            # “” -> \"
            line = line.replace("\"", "“")
            # ' -> "
            line = line.replace("\'", "\"")
            
            # 替换非法转义字符
            line = line.replace('\xa0', ' ')
            
            print(line)
            print(str(line))
            ans.append(json.loads(line))
        except Exception as e:
            print(e)
            ans.append({})
    return ans 


import pandas as pd

def excel_to_jsonlist(excel_path):
    """
    将Excel文件中的数据转换成JSON列表格式。
    
    :param excel_path: Excel文件的路径
    :return: 包含Excel数据的JSON列表
    """
    try:
        # 使用pandas读取Excel文件
        df = pd.read_excel(excel_path)
        
        # 将DataFrame转换为JSON列表
        return df.to_dict(orient='records')

    except FileNotFoundError:
        print(f"文件未找到: {excel_path}")
    except PermissionError:
        print(f"无权访问文件: {excel_path}")
    except Exception as e:
        print(f"处理文件时发生错误: {e}")


# 因为下载文件有特殊的标识key知道是我们的下载文件，所以直接可以特化处理，方便文件进进出出
def json_to_jsonlist(upload_file):
    dic = json.load(upload_file)
    if OUR_FILE_ID in dic:
        dic = dic[OUR_FILE_ID]
    return dic

def load_to_jsonlist(upload_file):
    if upload_file.name.endswith(".jsonl"):
        return jsonl_to_jsonlist(upload_file)
    elif upload_file.name.endswith(".xlsx"):
        return excel_to_jsonlist(upload_file)
    elif upload_file.name.endswith(".json"):
        return json_to_jsonlist(upload_file)