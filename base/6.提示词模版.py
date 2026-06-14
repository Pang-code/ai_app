from langchain_core.prompts import PromptTemplate

from my_llm import qwen_llm

# 定义提示词模板
prompt_template = PromptTemplate.from_template("帮我生成一个简短的，关于{topic}的介绍")

# 调用模板，传入参数
# prompt = prompt_template.invoke({"topic": "相声"})

# 打印生成的提示词
# print(prompt)




chain = prompt_template | qwen_llm

resp = chain.invoke({"topic": "相声"})
print(resp)
