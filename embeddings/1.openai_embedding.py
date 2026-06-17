from openai import OpenAI

from env_utils import (
DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL,
    DOUBAO_API_KEY, DOUBAO_BASE_URL,
)
# Doubao-embedding（基础文本向量化）
# 输入：仅纯文本，中英双语
# 向量维度：默认 2048，可降维 1024/512
# 上下文长度：4K tokens
# 定位：性价比通用款，绝大多数知识库、文本检索、相似度匹配首选，速度快、成本更低
# 对应固定版本：doubao-embedding-text-240515（24 年 5 月迭代基线版本）
# 2. Doubao-embedding-large（高精度大文本嵌入）
# 输入：仅纯文本
# 向量维度：最高 4096 维，可降维 2048/1024/512
# 上下文长度：4K tokens
# 定位：精度更强，长文本、复杂语义、精细匹配、问答召回效果更好；价格、耗时高于基础版
# 对应固定版本：doubao-embedding-large-text-250515（升级迭代版本）
# 3. Doubao-embedding-vision（多模态图文嵌入）

# doubao_llm = OpenAI(
#     api_key=DOUBAO_API_KEY,
#     base_url=DOUBAO_BASE_URL
#
# )
#
#
# embedding = doubao_llm.embeddings.create(
#
#     model="ep-doubao-embedding-large-text-240915",
#     dimensions=512,  # 降维维度
#     input="这是一个测试"
# )
#
#
#
# print(embedding)



from openai import OpenAI

client = OpenAI(
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY
)
resp = client.embeddings.create(
    model="text-embedding-v4", # Qwen3-Embedding
    dimensions=512,  # 降维维度
    input="需要向量化的文本"
)

print(len(resp.data[0].embedding))
print(resp.data[0].embedding)