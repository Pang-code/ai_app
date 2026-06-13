from langchain.agents import create_agent
from agent.init_llm import deepseek_llm
from agent.tools.tool_demo2 import web_search

# 创建智能体实例
agent = create_agent(
    # "qwen3.7-max",
    deepseek_llm,
    tools=[web_search],
    system_prompt="你是一个智能助手。尽可能的调用工具回答用户的问题"
)