from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# 1. 定义带多轮对话占位符的模板
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个电视台高端访谈节目的主持人！"),
    MessagesPlaceholder("msgs")  # 多轮对话历史的占位符
])

# 2. 渲染模板，传入对话历史
rendered_prompt = prompt_template.invoke({
    "msgs": [HumanMessage(content="你好，主持人！")]
})

print("渲染后的对话消息：")
print(rendered_prompt)

# 3. 初始化模型并构建链
from my_llm import qwen_llm



chain = prompt_template | qwen_llm

# 4. 调用链，传入多轮对话
response = chain.invoke({
    "msgs": [
        HumanMessage(content="你好，主持人！")
    ]
})

print("\n模型回复：")
print(response.content)







"""
还有作用是就是消息可以作为历史聊天作为上下文

这将生成一个包含两个消息的列表，第一个是系统消息，第二个是我们传入的HumanMessage。后面的消息就是我 和Al 大模型对话过程中的历史消息。这对于将消息列表插入到特定位置非常有用。

prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        '你是一个智能助手，尽可能的调用工具回答用户的问题'
    ),
    MessagesPlaceholder(
        variable_name='chat_history',
        optional=True
    ),
    ('human', '{input}'),
    MessagesPlaceholder(
        variable_name='agent_scratchpad',
        optional=True
    ),
])

"""
