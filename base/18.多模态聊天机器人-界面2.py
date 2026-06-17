import uuid
import gradio as gr
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

# 系统提示词：多模态助手，支持文本/音频/图像
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个多模态AI助手，可以处理文本、音频和图像输入"),
    # 占位符，自动填充历史对话上下文
    MessagesPlaceholder(variable_name="messages"),
])
from my_llm import qwen_llm

# 6. 构建链并调用
chain = prompt | qwen_llm



def get_session_history(session_id: str):
    """根据session_id从sqlite读取/存储当前会话全部聊天记录"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string='sqlite:///chat_history.db',
    )

# 封装带持久化会话记忆的完整对话链
chain_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)


# 全局唯一会话ID，每个网页用户独立上下文
config = {"configurable": {"session_id": str(uuid.uuid4())}}

# 本地测试代码（注释状态）
# user_msg = HumanMessage(content=[{'type': 'text', 'text': '你知道机器学习是什么吗？'}])
# resp1 = chain_history.invoke({'messages': [user_msg]}, config)
# print(resp1.content)


def get_last_user_after_assistant(history):
    """反向遍历找到最后一个assistant的位置，并返回后面的所有user消息"""
    # 空对话直接返回None
    if not history:
        return None
    # 最后一条是AI回复，说明无待处理用户消息，返回None
    if history[-1]["role"] == "assistant":
        return None

    last_assistant_idx = -1
    # 倒序遍历对话，找到最后一条assistant下标
    for i in range(len(history) - 1, -1, -1):
        if history[i]["role"] == "assistant":
            last_assistant_idx = i
            break

    # 全程没找到assistant：首次对话，返回全部历史（全是用户消息）
    if last_assistant_idx == -1:
        return history
    else:
        # 截取最后一条AI回复之后的所有消息（本次用户提问内容）
        return history[last_assistant_idx+1:]


import base64


def transcribe_audio(audio_path):
    """使用Base64处理语音，封装为多模态模型可识别audio_url结构"""
    # 目前多模态大模型两种传参方案：
    # 1、base64 data-url字符串（本地文件，无外网依赖）；2、公网可访问url地址
    try:
        # 二进制只读打开本地音频文件
        with open(audio_path, 'rb') as audio_file:
            # 读取二进制音频，base64编码，转utf-8字符串
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

        # 组装多模态标准音频消息体
        audio_message = {
            "type": "audio_url",
            "audio_url": {
                # data协议base64音频资源
                "url": f"data:audio/wav;base64,{audio_data}",
                "duration": 30  # 音频时长（秒），辅助模型优化解析
            }
        }
        return audio_message
    except Exception as e:
        print(f"音频读取编码失败：{e}")
        return None


import io
import base64
from PIL import Image


def transcribe_image(image_path):
    """
    :param image_path: 图片本地路径
    :return: 多模态标准image_url字典（base64 DataURL格式）
    """
    # 打开图片
    with Image.open(image_path) as img:
        # 获取原始图片格式，无格式默认JPEG
        img_format = img.format if img.format else 'JPEG'

        # 内存缓冲区，无需落地临时文件
        buffered = io.BytesIO()
        # 按原始格式保存，PNG保留透明通道，不会强制转JPEG丢失透明度
        img.save(buffered, format=img_format)

    # 缓冲区二进制转base64字符串
    image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # 返回大模型兼容的多模态图片消息体
    return {
        "type": "image_url",
        "image_url": {
            # 自适应图片格式的data base64 url
            "url": f"data:image/{img_format.lower()};base64,{image_data}",
            "detail": 'low'  # 图片解析精度：low/auto/high，low降低算力消耗
        }
    }


def add_message(history, messages):
    """将用户输入的消息添加到聊天记录中"""
    # 循环处理所有上传/录音媒体文件（图片/wav/mp4）
    for m in messages['files']:
        print(m)
        history.append({'role': 'user', "content": {'path': m}})
    # 处理纯文本消息
    if messages["text"] is not None and messages["text"].strip():
        history.append({"role": "user", "content": messages["text"]})
    # 返回更新后的聊天记录 + 重置清空多模态输入框
    # return history, gr.MultimodalTextbox(value=None, interactive=False)
    return history, ''


def submit_messages(history):
    """提交用户输入的消息，生成机器人回复"""
    user_messages = get_last_user_after_assistant(history)
    print(user_messages)
    content = []

    for x in user_messages:
        # if isinstance(x['content'], str):  # 文字输入消息
        #     content.append({'type': 'text', 'text': x['content']})
        # elif isinstance(x['content'], list):  # 多媒体输入消息
        #     file_path = x['content'][0]  # 得到多媒体的文件路径
        #     if file_path.endswith('.wav'):  # 输入的是音频文件
        #         file_message = transcribe_audio(file_path)
        #     elif file_path.endswith(".jpg") or file_path.endswith(".png") or file_path.endswith(".jpeg"):
        #         file_message = transcribe_image(file_path)
        #     content.append(file_message)
        # if isinstance(x['content'], str):  # 文字输入消息
        #     content.append({'type': 'text', 'text': x['content']})
        if isinstance(x['content'], list):  # 多媒体输入消息
            cont = x['content'][0]  # 得到多媒体的文件路径
            if cont.get('type') == 'text':
                if cont['text'].strip():  # 忽略空字符串
                    content.append({'type': 'text', 'text': cont['text']})

            elif cont.get('type') == 'file' and cont.get('file'):
                file_data = cont.get('file')
                file_path = file_data.get('path', '') if isinstance(file_data, dict) else ''
                if not file_path:
                    continue
                file_message = None


                if file_path.endswith('.wav'):  # 输入的是音频文件
                    file_message = transcribe_audio(file_path)
                elif file_path.endswith(".jpg") or file_path.endswith(".png") or file_path.endswith(".jpeg"):
                    file_message = transcribe_image(file_path)

                if file_message:
                    content.append(file_message)

        else:
            pass
    # 1. 将收集好的多模态数组封装为LangChain人类消息对象
    if not content:
        print("警告：没有有效的消息内容")
        return history
    # 1. 将收集好的多模态数组封装为LangChain人类消息对象
    input_message = HumanMessage(content=content)

    # 2. 调用带SQLite持久化记忆的多模态对话链
    resp = chain_history.invoke({"messages": input_message}, config)

    # 3. 将模型返回的AI回复存入前端渲染用的history列表
    history.append({'role': 'assistant', 'content': resp.content})

    return  history

# Gradio网页布局启动
with gr.Blocks(title='多模态聊天机器人', theme=gr.themes.Soft()) as block:
    # 新版messages格式聊天窗口，高度500px
    # chatbot = gr.Chatbot( height=500, label='聊天机器人',bubble_full_width=Frue)
    chatbot = gr.Chatbot( height=500, label='聊天机器人')

    # 创建多模态输入框
    chat_input = gr.MultimodalTextbox(
        interactive=True,       # 可交互
        file_types=['image', '.wav', '.mp4'],
        file_count="multiple",  # 允许多文件上传
        placeholder="请输入信息或者上传文件...",  # 输入框提示文本
        show_label=False,       # 不显示标签
        sources=["microphone", "upload"],  # 支持麦克风录音 + 文件上传
    )

    chat_input.submit(
        add_message,
        inputs=[chatbot, chat_input],
        outputs=[chatbot, chat_input]
    ).then(
        submit_messages,
        [chatbot],
        [chatbot],
    ).then(  # 回复完成后重新激活输入框
        lambda: gr.MultimodalTextbox(interactive=True),  # 匿名函数重置输入框
        None,  # 无输入
        [chat_input]  # 输出到输入框
    )


if __name__ == '__main__':
    block.launch()