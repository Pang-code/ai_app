from init_llm import deepseek_llm

# 返回自然语言的结果
# resp=deepseek_llm.invoke("你是谁？")
# print(resp)

# 需要结构化的 todo TypedDict的结构化输出

from typing_extensions import TypedDict, Annotated,List
# from typing import TypedDict, List, Annotated


# 使用TypedDict定义嵌套结构
class Actor(TypedDict):
    name: Annotated[str, "演员姓名"]
    role: Annotated[str, "饰演的角色"]

class Movie(TypedDict):
    title: Annotated[str, "电影的正式名称，例如《盗梦空间》"]
    year: Annotated[int, "电影的公映年份，使用四位数字表示"]
    director: Annotated[str, "电影导演的全名"]
    rating: Annotated[float, "电影在10分制下的评分，可包含一位小数"]
    cast: Annotated[List[Actor], "演员列表"]  # 嵌套列表定义



model_with_structure = deepseek_llm.with_structured_output(Movie)
# 调用模型并获取结构化输出
resp: Movie = model_with_structure.invoke("给我介绍下电影《星际穿越》")

print(type(resp))
print(resp)
