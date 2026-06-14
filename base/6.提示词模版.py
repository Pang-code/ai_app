from langchain_core.prompts import PromptTemplate

from my_llm import qwen_llm

# 多个提示词组成一个模板
# template_str = (
#     "帮我生成一个简短的，关于{topic}的报幕词。"
#     "要求：1、内容搞笑一点；"
#     "2、输出的内容采用{language}。"
# )
# # 传入完整字符串构建模板
# prompt = PromptTemplate.from_template(template_str)

# result = prompt.format(topic="校园运动会", language="东北方言")
# print(result)



# 单个提示词模板
# 定义提示词模板
prompt_template = PromptTemplate.from_template("帮我生成一个简短的，关于{topic}的介绍")

# 调用模板，传入参数
# prompt = prompt_template.invoke({"topic": "相声"})

# 打印生成的提示词
# print(prompt)




chain = prompt_template | qwen_llm

resp = chain.invoke({"topic": "相声"})
print(resp)
