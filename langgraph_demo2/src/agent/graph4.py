# 官方
# from agent.env_utils import ZHIPU_API_KEY
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.env_utils import DASHSCOPE_API_KEY
from agent.init_llm import qwen_llm as llm

# 外网上公开 MCP 服务端的连接配置
# zhipuai_mcp_server_config = {
#     'url': 'https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization',
#     'transport': 'sse',
# }


# 阿里百炼 MCP 服务配置（示例）
dashscope_mcp_server_config = {
    'url': 'https://mcp.dashscope.aliyuncs.com/sse',  # 替换为实际URL
    'transport': 'sse',
    'headers': {
        'Authorization': f'Bearer {DASHSCOPE_API_KEY}'
    }
}

my12306_mcp_server_config = {
    'url': 'https://mcp.api-inference.modelscope.net/1f6b76f83f2d49/sse',
    'transport': 'sse',
    'headers': {
        'Accept': 'application/json, text/event-stream',
    },
}

chart_mcp_server_config = {
    'url': 'https://mcp.api-inference.modelscope.net/0e9816d0af3647/sse',
    'transport': 'sse',
    'headers': {
        'Accept': 'application/json, text/event-stream',
    },
}

fetch_mcp_server_config = {
    'url': 'https://mcp-.api-inference.modelscope.net/sse',
    'transport': 'sse',
}

# MCP的客户端
mcp_client = MultiServerMCPClient(
    {
        'chart_mcp': chart_mcp_server_config,
        'my12306_mcp': my12306_mcp_server_config,
        # 'zhipuai_mcp': zhipuai_mcp_server_config,
        # 'dashscope_mcp': dashscope_mcp_server_config,
    }
)
import asyncio


class State(MessagesState):
    pass


def route_tools_func(state: State):
    """
    动态路由函数，如果从大模型输出后的AIMessage，中包含有工具调用的请求(指令)，
    就进入到tools节点，否则则结束
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


async def create_graph():
    tools = await mcp_client.get_tools()

    builder = StateGraph(State)

    llm_with_tools = llm.bind_tools(tools)

    async def chatbot(state: State):
        return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

    builder.add_node('chatbot', chatbot)

    # tool_node = BasicToolsNode(tools)
    tool_node = ToolNode(tools, handle_tool_errors=True)
    builder.add_node('tools', tool_node)

    builder.add_conditional_edges(
        "chatbot",
        tools_condition,
        {"tools": "tools", END: END}
    )

    builder.add_edge(start_key='tools', end_key='chatbot')
    builder.add_edge(START, end_key='chatbot')
    graph = builder.compile()
    return graph


agent = asyncio.run(create_graph())

# 图工厂函数，LangGraph 将自动调用它来创建图
# def agent():
#     return asyncio.run(create_graph())


# 帮我生成2025年，每个月销售数据，数据是随机的。
# 明天中午12点到1点有哪些从深圳去广州的高铁