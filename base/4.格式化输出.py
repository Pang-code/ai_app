
from pydantic import BaseModel, Field

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
