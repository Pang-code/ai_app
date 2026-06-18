# 本地私有化部署的大模型
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm



# 补全前面函数
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"城市： {city}，今天天气晴朗 ，气温35摄氏度!"


# 构建ReAct智能体状态图
graph = create_react_agent(
    llm,
    tools=[get_weather],
    prompt="你是一个智能助手"
)


# 启动方式1
# 单轮调用示例
# res = graph.invoke({"messages": [("user", "深圳今天天气怎么样？")]})
# print(res["messages"][-1].content)

# 启动方式2
# langgraph dev

