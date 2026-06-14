from langchain_core.prompts import ChatPromptTemplate


# 变量占位符


# 1. 定义对话式提示词模板
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个幽默的电视台主持人！"),
    ("user", "帮我生成一个简短的，关于{topic}的报幕词。")
])

# 2. 测试模板渲染
# print("渲染后的提示词：")
# print(prompt_template.invoke({"topic": "相声"}))

# 3. 初始化模型（这里用本地部署的vLLM服务作为示例）
from my_llm import qwen_llm


# 4. 构建链并调用
chain = prompt_template | qwen_llm
response = chain.invoke({"topic": "相声"})
print("\n模型输出：")
print(response)