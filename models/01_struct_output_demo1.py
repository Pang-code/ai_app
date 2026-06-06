from init_llm import deepseek_llm

# 返回自然语言的结果
# resp=deepseek_llm.invoke("你是谁？")
# print(resp)

# 需要结构化的 todo 官方推荐的结构化输出
from pydantic import BaseModel, Field


class Movie(BaseModel):
    title: str = Field(description="电影名称")
    director: str = Field(description="导演")
    year: int = Field(description="上映年份")
    rating: float = Field(description="评分（10分制）")


model_with_structure = deepseek_llm.with_structured_output(Movie)
# 调用模型并获取结构化输出
resp: Movie = model_with_structure.invoke("给我介绍下电影《星际穿越》")

print(type(resp))
print(resp)
