from langchain_core.messages import HumanMessage
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, MessagesPlaceholder

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 1. 定义示例列表
examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]

# 2. 定义单个示例的对话模板
base_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

# 3. 创建少样本对话模板
few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=base_prompt,
)

# 4. 定义最终对话模板，包含系统提示、少样本示例和对话历史占位符
final_template = ChatPromptTemplate.from_messages([
    ("system", "你是智能机器人AI助手！"),
    few_shot_prompt,
    MessagesPlaceholder("msgs")  # 多轮对话历史占位符
])

# 5. 初始化模型
from my_llm import qwen_llm

# 6. 构建链并调用
chain = final_template | qwen_llm

# 传入用户问题（注意这里应该用msgs，而不是input）
response = chain.invoke({
    "msgs": [HumanMessage(content="2 🦜 9 的结果是多少？")]
})

print("模型回复：")
print(response.content)