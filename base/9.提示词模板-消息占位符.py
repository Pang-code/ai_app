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