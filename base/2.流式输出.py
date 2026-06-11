from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

from env_utils import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL,
)

# ==================== DeepSeek ====================
deepseek_llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_BASE_URL,
    model="deepseek-v4-pro",
    extra_body={"reasoning": {"enabled": True}},  # 启用推理
    stream_usage=True,
    temperature=None,
    max_tokens=None,
    timeout=None,
    reasoning_effort="low",
    max_retries=2,

)

stream_usage = True,
# 初始化变量，用于拼接完整的流式响应
full = None  # 类型标注：None | AIMessageChunk

# 1. 流式输出模型响应文本
for chunk in deepseek_llm.stream("你的问题"):
    full = chunk if full is None else full + chunk
    print(full.text)  # 逐次打印当前拼接后的文本



# 打印完整响应的结构化内容块
print(full.content_blocks)
# 示例输出：[{"type": "text", "text": "The sky is typically blue..."}]





# 2. 流式输出推理过程（适配含思维链的模型）
for chunk in deepseek_llm.stream("你的问题"):
    # print(type(chunk))
    # print(chunk)
    # # 过滤出类型为"reasoning"的推理步骤内容
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    # # 有推理步骤则打印，否则打印普通文本
    print(reasoning_steps if reasoning_steps else chunk.text)