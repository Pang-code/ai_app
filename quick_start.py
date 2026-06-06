from langchain.agents import create_agent

from my_llm import deepseek_llm


def get_weather(city: str) -> str:
    # 模拟天气查询
    """获取给定城市的天气。"""
    return f"{city} 天气晴朗！"


# 创建Agent
agent = create_agent(
    model=deepseek_llm,
    tools=[get_weather],
    system_prompt="你是一个助手，你可以查询城市的天气。",
)

# 调用Agent
resp = agent.invoke(
    {"messages": [{"role": "user", "content": "查询深圳的天气"}]}
)

print(resp)
