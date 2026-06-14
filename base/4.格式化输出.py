from langchain_core.output_parsers import SimpleJsonOutputParser
from pydantic import BaseModel, Field

# 1.with_structured_output


class Movie(BaseModel):
    """电影详情。"""
    title: str = Field(description="电影标题")
    year: int = Field( description="电影发行年份")
    director: str = Field( description="电影导演")
    rating: float = Field( description="电影评分（满分10分）")


# 不是所有模型都支持结构化输出，例如：qwen  不支持  with_structured_output
from init_llm import deepseek_llm

model_with_structure = deepseek_llm.with_structured_output(Movie, include_raw=True) # 参数 include_raw 表示是否返回原始文本
# 调用模型并获取结构化输出
resp = model_with_structure.invoke("给我介绍下电影《星际穿越》")

print(type(resp))
print(resp)






import json
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 使用 Pydantic 定义数据模型，约束笑话的输出格式
class Joke(BaseModel):
    """笑话（搞笑段子）的结构类(数据模型类 PODO)"""
    setup: str = Field(description="笑话的开头部分")
    punchline: str = Field(description="笑话的包袱/笑点")
    rating: Optional[int] = Field(description="笑话的有趣程度评分，范围 1 到 10")

# 2. 初始化 LLM（这里用本地部署的vLLM服务作为示例）


# 3. 定义提示词模板
prompt_template = PromptTemplate.from_template("帮我生成一个关于 {topic} 的笑话。")

# 4. 为 LLM 绑定结构化输出格式
runnable = deepseek_llm.with_structured_output(Joke)

# 5. 构建链并调用
chain = prompt_template | runnable
resp = chain.invoke({"topic": "猫"})

# 6. 输出结果
print("结构化对象输出：")
print(resp)
print("\n字典格式输出：")
print(resp.__dict__)
print("\nJSON 格式输出：")
print(json.dumps(resp.__dict__))








# 2. SimpleJsonOutputParser 回答的问题还会衍生一个问题

prompt = ChatPromptTemplate.from_template("""
尽你所能回答用户的问题。

你必须始终输出一个包含"answer"和"followup_question"键的JSON对象。
其中"answer"代表：对用户问题的回答；
"followup_question"代表：用户可能提出的后续问题。

{question}
""")


# 3. 构建链式调用：提示词 → 大模型 → JSON解析器
chain = prompt | deepseek_llm | SimpleJsonOutputParser()

# 4. 执行调用
resp = chain.invoke({"question": "细胞的动力源是什么？"})
print(resp)