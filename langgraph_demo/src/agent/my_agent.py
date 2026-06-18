# 本地私有化部署的大模型
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm
from agent.tools.tool_demo_arg2 import calculate3



# 构建ReAct智能体状态图
my_agent = create_react_agent(
    llm,
    tools=[calculate3],
    prompt="你是一个智能助手,尽可能的调用工具回答用户的问题"
)


# 启动方式1
# 单轮调用示例
# res = graph.invoke({"messages": [("user", "深圳今天天气怎么样？")]})
# print(res["messages"][-1].content)

# 启动方式2
# langgraph dev  帮我计算一下(1+4)*2

