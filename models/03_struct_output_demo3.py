from init_llm import deepseek_llm

# 返回自然语言的结果
# resp=deepseek_llm.invoke("你是谁？")
# print(resp)

# 需要结构化的 todo json结构化输出


# 使用 JSON Schema（最灵活，跨语言友好）
json_schema = {
    "title": "MovieInfo",  # 当前工具的名称
    "description": "包含电影标题、上映年份、导演和评分的电影对象",
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "电影标题"},
        "year": {"type": "integer", "description": "上映年份"},
        "director": {"type": "string", "description": "导演"},
        "rating": {"type": "number", "description": "评分（10分制）"}
    },
    "required": ["title", "year", "director", "rating"]
}

model_with_structure = deepseek_llm.with_structured_output(json_schema)
# 调用模型并获取结构化输出
resp: json_schema = model_with_structure.invoke("给我介绍下电影《星际穿越》")

print(type(resp))
print(resp)
