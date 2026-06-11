from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain.chat_models import init_chat_model

from env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, OPENAI_API_KEY, OPENAI_BASE_URL, ANTHROPIC_API_KEY, \
    ANTHROPIC_BASE_URL, DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, ZHIPUAI_API_KEY, ZHIPUAI_BASE_URL



rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  #表示每秒最多发送 0.1 次请求，也就是每 10 秒 1 次请求，严格控制平均速率。
    check_every_n_seconds=0.1, # 限流器每 100 毫秒检查一次是否允许发送请求，确保限流的响应及时性。
    max_bucket_size=10,        #令牌桶的最大容量，允许一次性发送最多 10 个请求的 “突发流量”，应对短时间内的并发需求
)


tongyi_llm = init_chat_model(
    model="qwen3.7-max",
    model_provider="openai",
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,
)



for i in range(3):
    response = tongyi_llm.invoke("你好，介绍一下自己")

