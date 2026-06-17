import uuid
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个多模态AI助手，可以处理文本、音频和图像输入"),
        MessagesPlaceholder(variable_name="messages"),  # 代表：历史消息
    ]
)
from my_llm import qwen_llm

# 6. 构建链并调用
chain = prompt | qwen_llm


# 1. 基础LCEL对话链：提示词 + 多模态大模型

# 2. 会话历史工厂函数：按session_id读取SQLite存储的聊天记录
def get_session_history(session_id: str):
    """从关系型数据库的历史消息列表中 返回当前会话 的所有历史消息"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string='sqlite:///chat_history.db',
    )

# 3. 封装带自动持久化记忆的完整对话链
chain_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)

config = {"configurable": {"session_id": str(uuid.uuid4())}}


# 构造多模态用户消息（标准多模态格式）
user_msg = HumanMessage(content=[{'type': 'text', 'text': '什么是机器学习'}])
# 调用带SQL会话记忆的对话链
resp1 = chain_history.invoke({'messages': [user_msg]}, config=  config)

print(resp1.content)

