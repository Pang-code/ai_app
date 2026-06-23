# 中断输入执行
# from agent.env_utils import ZHIPU_API_KEY
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
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
    # graph = builder.compile(interrupt_before=['tools']) # 加入中断,任何节点都会中断。这种只有在langchain develop模式下才会生效
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory, interrupt_before=['tools'])
    return graph


# agent = asyncio.run(create_graph())
async def run_graph():
    graph = await create_graph()
    # 配置参数，包含乘客ID和线程ID
    config = {
        "configurable": {
            # 检查点由session_id访问
            "thread_id": 'zs12311',
        }
    }

    def print_message(event, result):
        """格式化输出消息"""
        messages = event.get('messages')
        if messages:
            if isinstance(messages, list):
                message = messages[-1]  # 如果消息是列表，则取最后一个
            if message.__class__.__name__ == 'AIMessage':
                if message.content:
                    # print(result)
                    result = message.content  # 需要在展示的消息
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > 1500:
                msg_repr = msg_repr[:1500] + " ...（已截断）"  # 超过最大
            print(msg_repr)  # 输出消息的表示形式
        return result

    def get_answer(tool_message, user_answer):
        """让人介入，并且给一个问题的答案"""
        tool_name = tool_message.tool_calls[0]['name']
        answer = (
            f"人工强制终止了工具：{tool_name}的执行，拒绝的理由是：{user_answer}"
        )

        # 创建一个消息
        new_message = [
            ToolMessage(content=answer, tool_call_id=tool_message.tool_calls[0]["id"]),
            AIMessage(content=answer)
        ]

        # 把新人造的消息，添加到工作流的state中
        graph.update_state(  # 手动修改state
            config=config,
            values={'messages': new_message}
        )




    async def execute_graph(user_input: str) -> str:
        """ 执行工作流的函数 """
        result = ''  # AI助手的最后一条消息
        # for chunk in graph.astream(input=None, config, stream_mode='values'):

        if user_input.strip().lower() != 'y':  # 正常的用户提问
            current_state = graph.get_state(config)
            if current_state.next:  # 如果有下一步，则当前工作流处在中断中
                tools_script_message = current_state.values['messages'][-1]# 通过提供关于请求的更改/改变主意的指示来满足工具调用
                get_answer(tools_script_message, user_input)
                message = graph.get_state(config).values['messages'][-1]
                result = message.content
                return  result
            else:
                # 不是可等待对象（Awaitable），因此不能直接用于 await 表达式，必须通过
                async for chunk in graph.astream({'messages': ('user',user_input)}, config, stream_mode='values'):
                    result = print_message(chunk, result)
        else:  # 用户想继续工具的调用 输入y
            async for chunk in graph.astream(None, config, stream_mode='values'):
                result = print_message(chunk, result)

        current_state = graph.get_state(config)
        if current_state.next:  # 出现了工作流的中断
            ai_message = current_state.values['messages'][-1]
            tool_name = ai_message.tool_calls[0]['name']
            # ai_message.tool_calls[0]['args']
            result = f"AI助手马上根据你要求，执行{tool_name}工具。您是否批准继续执行？输入'y'继续；否则，请说明你的理由"


        return result


    # 执行工作流
    while True:
        user_input = input('用户: ')
        res = await execute_graph(user_input)
        print('AI: ', res)

if __name__ == '__main__':
    asyncio.run(run_graph())