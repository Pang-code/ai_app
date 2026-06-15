from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        '你是一个乐于助人的助手。尽你所能回答所有问题。提供的聊天历史包含与你对话用户的信息。'
    ),
    MessagesPlaceholder(variable_name='chat_history', optional=True),

    ('human', '{input}'),
    # MessagesPlaceholder(variable_name='agent_scratchpad', optional=True),
])
from my_llm import qwen_llm

# 6. 构建链并调用
chain = prompt | qwen_llm





from langchain_core.chat_history import InMemoryChatMessageHistory

# 全局会话存储容器
# store = {}  # key: session_id(str), value: InMemoryChatMessageHistory 对象

def get_session_history(session_id: str):
    """从关系型数据库的历史消息列表中 返回当前会话 的所有历史消息"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string='sqlite:///chat_history.db',# 可以是任何关系型数据库
    )


# 3、创建带历史记录功能的处理链
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history',
)



# 第一次对话
# # 调用带会话记忆的对话链
# resp = chain_with_message_history.invoke(
#     {"input": "你好，我名字叫：pcw"},
#     config={"configurable": {"session_id": "user2"}}
# )
# print("模型回复1：")
# print(resp)



# 第二次对话
# 调用带会话记忆的对话链
resp = chain_with_message_history.invoke(
    {"input": "你好，我叫什么名字？"},
    config={"configurable": {"session_id": "user2"}}
)
print("模型回复2：")
print(resp)