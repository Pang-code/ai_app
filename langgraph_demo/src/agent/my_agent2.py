# 本地私有化部署的大模型
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm
from agent.tools.tool_demo6 import runnable_tool
from agent.tools.tool_demo_arg2 import calculate3



# 构建ReAct智能体状态图
my_agent2 = create_react_agent(
    llm,
    tools=[calculate3,runnable_tool],
    prompt="你是一个智能助手,尽可能的调用工具回答用户的问题"
)


# 马上有一个小品需要演出，给我日文的报幕词
