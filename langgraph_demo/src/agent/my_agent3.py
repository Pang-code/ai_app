# 动态提示词模版   通过configurable 传输给智能体
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm
from agent.tools.tool_demo6 import runnable_tool
from agent.tools.tool_demo_arg2 import calculate3
# from agent.tools.tool_demo7 import MySearchTool
from langchain_core.messages import AnyMessage,BaseMessage
# from langgraph.prebuilt import AgentState
from langchain_core.runnables import RunnableConfig

from typing import Sequence, TypedDict
class AgentState(TypedDict):
    """智能体状态类型定义"""

    # # from langgraph.prebuilt import AgentState找不到这个方法了
    messages: Sequence[BaseMessage]


# 提示词模板的函数：由用户传入内容，组成一个动态的系统提示词
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config['configurable'].get('user_name', 'zs')
    print(f"用户名：{user_name}")
    system_message = f'你是一个智能助手，当前用户的名字是：{user_name}'
    return [{'role': 'system', 'content': system_message}]+state["messages"]

# 构建ReAct智能体状态图
my_agent3 = create_react_agent(
    llm,
    tools=[calculate3, runnable_tool],
    prompt=prompt
)


# 马上有一个小品需要演出，给我日文的报幕词

