from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough

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


def summarize_messages(current_input):
    """剪辑和摘要上下文，历史记录"""
    # 1. 从入参中提取会话ID
    session_id = current_input['config']["configurable"]["session_id"]
    if not session_id:
        raise ValueError("必须通过config参数提供session_id")

    # 2. 获取当前会话全部聊天记录
    chat_history = get_session_history(session_id)
    stored_messages = chat_history.messages
    if len(stored_messages) <= 2:
        return False
    # 取出最后2条最新消息，完整保留不做摘要
    last_two_messages = stored_messages[-2:]
    # 取出除最后2条以外的全部历史消息，用于执行摘要压缩
    messages_to_summarize = stored_messages[:-2]

    summarization_prompt = ChatPromptTemplate.from_messages([
        ("system", "请将以下对话历史压缩为一条保留关键信息的摘要消息。"),
        ("placeholder", "{chat_history}"),
        ("human", "请生成包含上述对话核心内容的摘要，保留重要事实和决策。")
    ])


    summarization_chain = summarization_prompt | qwen_llm
    summary_message = summarization_chain.invoke({'chat_history': messages_to_summarize})

    # 重建历史记录：摘要 + 最后2条原始消息
    chat_history.clear()
    chat_history.add_message(summary_message)
    for msg in last_two_messages:
        chat_history.add_message(msg)

    return True



# 最终的链
# 最终的链
# RunnablePassthrough 默认会将输入数据原样传递到下游，而 .assign() 方法允许在保留原始输入的同时，通过指定键值对（如 messages_xxx）追加新字段到输入字典中
final_chain = (RunnablePassthrough.assign(messages_summarized=summarize_messages) | chain_with_message_history)



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
resp = final_chain.invoke(
    {"input": "你好，我叫什么名字？", 'config':{"configurable": {"session_id": "user2"}}},
    config={"configurable": {"session_id": "user2"}}
)
print("模型回复2：")
print(resp)