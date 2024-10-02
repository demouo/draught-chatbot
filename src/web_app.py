# web_app.py
import os
import streamlit as st
import time
from draught_chatbot.config.prompt_config import DEFAULT_SYS_PRONMPT
from draught_chatbot.chat.api_chat import api_chat
from draught_chatbot.chat.search_chat import search_chat
from draught_chatbot.config.model_config import SUPPORT_MODEL_DICT
from draught_chatbot.tool.tojson import load_to_jsonlist
from draught_chatbot.config.web_config import PASSWORD
from draught_chatbot.config.web_config import NOT_SUPPORT_WEB_PREVIEW, OUR_FILE_ID
import json
from draught_chatbot.config.model_config import SUPPORT_MODEL_DICT, APIKEY_CONFIG_PATH 

# 检查会话状态中是否有登录状态，如果没有，初始化为 False
if 'log_in' not in st.session_state:
    st.session_state.log_in = False

if st.session_state.log_in == False:        
    # 欢迎
    st.write("欢迎使用 Draught Chatbot  🚀 ")
    user_name = st.text_input("请输入用户名", value="default")
    # 在侧边栏添加输入邀请码的部分
    invitation_code = st.text_input("请输入邀请码", type="password")
    log_in_btn = st.button("登录")
    if log_in_btn:
        # 验证邀请码
        if invitation_code in PASSWORD:
            st.session_state.log_in = True
            st.session_state.user_name = user_name
            st.rerun()
        else:
            st.error("无效的邀请码，请重新输入")
else:
    # Streamlit页面配置
    st.set_page_config(page_title="Draught Chatbot", page_icon="🤖")

    # 页面标题
    st.title("Draught Chatbot")

    # 初始化系统提示
    if "sys_instruction_prompt" not in st.session_state:
        st.session_state.sys_instruction_prompt = ""

    # 侧边栏 - 图片
    logo_path = '../assets/logo_sheep.png'
    st.sidebar.image(logo_path, use_column_width=True)

    # 侧边栏 - 声明
    st.sidebar.subheader("Dev by @Draught")

    # 侧边栏 - 切换按钮
    page = st.sidebar.selectbox("Select Page", ["对话", "搜索", "文件上传", "对话复现", "KEY管理"], index=0)

    # 侧边栏 - 选择 type
    sys_prompt_options = DEFAULT_SYS_PRONMPT.keys()
    selected_sys_prompt = st.sidebar.selectbox("Select Default SYS Prompt", sys_prompt_options)
    if selected_sys_prompt:
        # 根据选择的 type 更新 model 选项
        st.session_state.sys_instruction_prompt = DEFAULT_SYS_PRONMPT[selected_sys_prompt]

    # 侧边栏 - 输入系统提示
    st.session_state.sys_instruction_prompt = st.sidebar.text_area(
        "Enter System Instruction Prompt",
        value=st.session_state.sys_instruction_prompt,
        height=100
    )

    # 侧边栏 - 选择 type
    type_options = SUPPORT_MODEL_DICT.keys()
    selected_type = st.sidebar.selectbox("Select Type", type_options)

    # 根据选择的 type 更新 model 选项
    model_options = SUPPORT_MODEL_DICT[selected_type]

    # 侧边栏 - 选择 model
    selected_model = st.sidebar.selectbox("Select Model", model_options)

    # 侧边栏 - 选择温度
    temperature = st.sidebar.slider("Select Temperature", min_value=0.0, max_value=1.0, value=0.95)

    # 全局 - 用户配置
    if "apikey_config" not in st.session_state:
        user_name = st.session_state.user_name 
        with open(APIKEY_CONFIG_PATH, "r", encoding='utf-8') as fp:
            apikeys = json.load(fp)
        curr_user_apikeys = apikeys.get(user_name, {})
        st.session_state.apikey_config = curr_user_apikeys

    if page == "KEY管理":
        def save():
            st.session_state.apikey_config = curr_user_apikeys
            apikeys[st.session_state.user_name] = curr_user_apikeys
            with open(APIKEY_CONFIG_PATH, "w", encoding='utf-8') as fp:
                json.dump(apikeys, fp, indent=4, ensure_ascii=False)

        st.header("KEY管理")
        
        with open(APIKEY_CONFIG_PATH, "r", encoding='utf-8') as fp:
            apikeys = json.load(fp)
            
        curr_user_apikeys = apikeys.get(st.session_state.user_name, {})
        st.session_state.apikey_config = curr_user_apikeys
        
        zhipu_apikey = curr_user_apikeys.get("ZHIPU_APIKEY", "")
        zhipu_apikey_input = st.text_input("ZHIPU_APIKEY", value=zhipu_apikey,type="password")
        if zhipu_apikey_input:
            st.success("ZHIPU_APIKEY已保存")
            curr_user_apikeys["ZHIPU_APIKEY"] = zhipu_apikey_input
            save()
        
        qianfan_ak = curr_user_apikeys.get(f"QIANFAN_AK", "")
        qianfan_sk = curr_user_apikeys.get(f"QIANFAN_SK", "")
        qianfan_ak_input = st.text_input("QIANFAN_AK", value=qianfan_ak,type="password")
        qianfan_sk_input = st.text_input("QIANFAN_SK", value=qianfan_sk,type="password")
        if qianfan_ak_input and qianfan_sk_input:
            st.success("QIANFAN_APIKEY已保存")
            curr_user_apikeys[f"QIANFAN_AK"] = qianfan_ak_input
            curr_user_apikeys[f"QIANFAN_SK"] = qianfan_sk_input
            save()
        
        doubao_ark = curr_user_apikeys.get(f"ARK_APIKEY", "")
        doubao_ark_input = st.text_input("DOUBAO_ARK_APIKEY", value=doubao_ark,type="password")
        if doubao_ark_input:
            curr_user_apikeys[f"ARK_APIKEY"] = doubao_ark_input
            doubao_models = SUPPORT_MODEL_DICT['doubao'] 
            doubao_model = st.selectbox("Select Doubao Model", doubao_models)
            if doubao_model:
                doubao_model_key = curr_user_apikeys.get(f"doubao.{doubao_model}", "")
                doubao_model_key_input = st.text_input(doubao_model + "_KEY", value=doubao_model_key,type="password")
                if doubao_model_key_input:
                    st.success(f"DOUBAO_{doubao_model}_KEY已保存")
                    curr_user_apikeys[f"doubao.{doubao_model}"] = doubao_model_key_input
                    save()
                    
    # 文件上传页面
    elif page == "文件上传":
        if not st.session_state.apikey_config:
            st.warning("检测到未配置APIKEY，请先到\"Page - KEY管理\"配置APIKEY")
        st.header("文件上传")
        uploaded_file = st.file_uploader("上传文件", type=["txt", "pdf", "docx", "xlsx", "json", "jsonl"])
        x = []
        if uploaded_file is not None:
            st.write("文件已上传:", uploaded_file.name)
            try:
                fp = load_to_jsonlist(uploaded_file)
                x = fp[0].keys()
                # show_content = "字段：" + str(list(fp[0].keys())) + "\n长度："+str(len(fp))+"\n单个预览：\n" + str(fp[0])
                show_content = f"长度：{(len(fp))}\n字段：{(list(fp[0].keys()))}\n单个预览：\n{(fp[0])}"
                st.text_area("文件内容", show_content, height=200)
                
                content_field = st.sidebar.selectbox("Select Content Field", x)
                y = [i for i in x if i != content_field]
                target_field = st.sidebar.selectbox("Select Target Field", y)
                st.warning("< - 请前往侧边栏选择对话字段") 
                batch_button = st.button("Batch chat")
                if "batch_chat_end" not in st.session_state:
                    st.session_state.batch_chat_end = False
                save_dict = {"file": uploaded_file.name, "content_field": content_field, "type": selected_type, "model": selected_model, "temperature": temperature,
                            "sys_instruction_prompt": st.session_state.sys_instruction_prompt, 
                            }
                if batch_button:
                    ans = []
                    for j in range(len(fp)):
                        try:
                            i = fp[j]
                            prompt = str(i[content_field])
                            st.write(j+1)
                            # 显示用户消息
                            with st.chat_message("user"):
                                st.write(prompt)
                            messages = [{"role": "system", "content": st.session_state.sys_instruction_prompt}]
                            messages.append({"role": "user", "content": prompt})
                            # 调用 API 获取响应，使用用户选择的 type 和 model
                            response = api_chat(type=selected_type, model=selected_model, temperature=temperature, messages=messages, stream=True, apikey_config=st.session_state.apikey_config) 
                    
                            # 处理流式响应
                            assistant_response_parts = []
                            with st.chat_message("assistant"):  
                                container = st.empty()
                                for chunk in response:
                                    new_text = chunk
                                    assistant_response_parts.append(new_text)
                                    output = "".join(assistant_response_parts)
                                    container.markdown(output, unsafe_allow_html=True)
                                    time.sleep(0.05)
                            st.write("\n")
                            ans.append({"input": prompt, "output": output})
                        except Exception as e:
                            st.error(j+1)
                            continue
                    st.markdown("`[END]` All Chats are Done!")
                    st.session_state.batch_chat_end = True
                    save_dict[OUR_FILE_ID] = ans
            except:
                save_dict[OUR_FILE_ID] = ans
                st.download_button("Download", json.dumps(save_dict, indent=4, ensure_ascii=False), file_name=uploaded_file.name+".json")
            if st.session_state.batch_chat_end:
                st.download_button("Download", json.dumps(save_dict, indent=4, ensure_ascii=False), file_name=uploaded_file.name+".json")
    elif page == "对话复现":
        st.header("对话复现")
        uploaded_file = st.file_uploader("上传文件", type=["json", "jsonl"])
        if uploaded_file is not None:
            st.write("文件已上传:", uploaded_file.name)
            fp = load_to_jsonlist(uploaded_file)
            if fp is None or len(fp) == 0:
                st.error("文件为空")
            elif "input"not in fp[0] or "output" not in fp[0]:
                st.error("非妈生格式, 请前往文件对话下载准确的格式或自制含有字段{input,output}的字典")
            else:
                for j in range(len(fp)):
                    i = fp[j]
                    prompt = str(i["input"])
                    st.write(j+1)
                    # 输入
                    with st.chat_message("user"):
                        st.write(prompt)
                    # 输出
                    with st.chat_message("assistant"):  
                        container = st.empty()
                        output = i['output']
                        container.markdown(output, unsafe_allow_html=True)
                    st.write("\n")
                st.markdown("`[END]` All Chats are Done!")
    elif page == "搜索":
        if not st.session_state.apikey_config:
            st.warning("检测到未配置APIKEY，请先到\"Page - KEY管理\"配置APIKEY")
        st.header("搜索")
        # 初始化聊天历史
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_instruction_prompt}]
        else:
            # 更新系统指令
            st.session_state.messages[0] = {"role": "system", "content": st.session_state.sys_instruction_prompt}

        # 用户选择历史消息的数量
        history_length = st.sidebar.slider("Select Number of History", min_value=0, max_value=10, value=3)

        # 添加清除历史按钮
        clear_history_button = st.sidebar.button("Clear Chats", type="primary")

        # 当用户点击清除历史按钮时，显示确认弹框
        if clear_history_button:
            st.sidebar.info("Cleared all history.")
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_instruction_prompt}]

        # 显示聊天历史 (从第二个元素开始，因为第一个元素是系统指令)
        chat_container = st.container()  # 创建一个容器用于显示聊天历史
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # 用户输入
        if prompt := st.chat_input("开始全网搜索"):
            # 显示用户消息
            with st.chat_message("user"):
                st.write(prompt)
            
            # 根据用户选择的历史长度来截取历史消息
            history_messages = []
            if history_length > 0: 
                history_messages += st.session_state.messages[-history_length:]
            if len(history_messages) == 0 or history_messages[0]["role"] != "system":
                history_messages = [st.session_state.messages[0]] + history_messages
            messages = history_messages + [{"role": "user", "content": prompt}]

            # 调用 API 获取响应，使用用户选择的 type 和 model
            apikeys = search_chat(type=selected_type, model=selected_model, messages=messages) 
            
            with st.chat_message("assistant"):  
                # 提取搜索意图
                search_intent = apikeys['choices'][0]['message']['tool_calls'][0]['search_intent'][0]

                # 提取搜索结果
                search_results = apikeys['choices'][0]['message']['tool_calls'][1]['search_result']

                # 打印搜索意图信息
                st.markdown("### 搜索意图")
                st.markdown(f"**类别**：{search_intent.get('category', '')}")
                st.markdown(f"**意图**：{search_intent.get('intent', '')}")
                st.markdown(f"**关键词**：{search_intent.get('keywords', '')}")
                st.markdown(f"**查询**：{search_intent.get('query', '')}")
                st.markdown("\n")

                # 打印搜索结"果信息
                st.markdown("\n### 搜索结果：")
                for i in range(len(search_results)):
                    result = search_results[i]
                    st.markdown(f"#### 网页{i+1}")
                    st.markdown(f"**标题**：{result.get('title', '')}")
                    st.markdown(f"**媒体**：{result.get('media', '')}")
                    link = result.get('link', '')
                    st.markdown(f"**链接**：{link}")
                    
                    with st.expander("点击预览网页"):
                        # 使用 iframe 嵌入网页预览
                        if link and not any(not_support_web in link for not_support_web in NOT_SUPPORT_WEB_PREVIEW):
                            st.markdown(f"**网页预览**：")
                            # st.components.v1.iframe(link, width=800, height=600, scrolling=True)
                            # 在占位符中加载网页
                            # 使用 HTML 的 iframe 标签来禁用自动播放等功能
                            iframe_html = f"""
                                <iframe src="{link}" width="1080" height="900" frameborder="0" 
                                        style="border:0" allowfullscreen sandbox="allow-scripts allow-same-origin"></iframe>
                            """
                            st.markdown(iframe_html, unsafe_allow_html=True)
                        else:
                            st.warning("暂不支持预览")
                    st.markdown(f"**内容**：{result.get('content', '')}\n")
    else:
        if not st.session_state.apikey_config:
            st.warning("检测到未配置APIKEY，请先到\"Page - KEY管理\"配置APIKEY")
        # 对话
        # 初始化聊天历史
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_instruction_prompt}]
        else:
            # 更新系统指令
            st.session_state.messages[0] = {"role": "system", "content": st.session_state.sys_instruction_prompt}

        # 用户选择历史消息的数量
        history_length = st.sidebar.slider("Select Number of History", min_value=0, max_value=10, value=3)

        # 添加清除历史按钮
        clear_history_button = st.sidebar.button("Clear Chats", type="primary")

        # 当用户点击清除历史按钮时，显示确认弹框
        if clear_history_button:
            st.sidebar.info("Cleared all history.")
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_instruction_prompt}]

        # 显示聊天历史 (从第二个元素开始，因为第一个元素是系统指令)
        chat_container = st.container()  # 创建一个容器用于显示聊天历史
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # 用户输入
        if prompt := st.chat_input("欢迎向我提问🙋"):
            # 显示用户消息
            with st.chat_message("user"):
                st.write(prompt)
            
            # 添加中断按钮
            stop_button = st.button('stop', key='stop_button')

            # 根据用户选择的历史长度来截取历史消息
            history_messages = []
            if history_length > 0: 
                history_messages += st.session_state.messages[-history_length:]
                if len(history_messages) == 0 or history_messages[0]["role"] != "system":
                    history_messages = [st.session_state.messages[0]] + history_messages
            messages = history_messages + [{"role": "user", "content": prompt}]

            # 调用 API 获取响应，使用用户选择的 type 和 model
            response = api_chat(type=selected_type, model=selected_model, temperature=temperature, messages=messages, stream=True, apikey_config=st.session_state.apikey_config) 
            
            # 处理流式响应
            assistant_response_parts = []
            with st.chat_message("assistant"):  
                container = st.empty()
                for chunk in response:
                    new_text = chunk
                    assistant_response_parts.append(new_text)
                    container.markdown("".join(assistant_response_parts), unsafe_allow_html=True)
                    if stop_button:  # 检查是否点击了中断按钮
                        break
                    time.sleep(0.05)
                
                # 显示完整的响应
                container.markdown("".join(assistant_response_parts), unsafe_allow_html=True)
                # 对话历史
                final_response = "".join(assistant_response_parts).strip()
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                

