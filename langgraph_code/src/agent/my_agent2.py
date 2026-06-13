from langchain.agents import create_agent
from agent.init_llm import deepseek_llm
from agent.tools.tool_demo2 import web_search
from agent.tools.tool_demo3 import MySearchTool

my_search=MySearchTool()  #

# 创建智能体实例
agent = create_agent(
    # "qwen3.7-max",
    deepseek_llm,
    # tools=[web_search, MySearchTool],
    tools=[ MySearchTool],
    system_prompt="你是一个智能助手。尽可能的调用工具回答用户的问题"
)