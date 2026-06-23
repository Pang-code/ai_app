# 自定义工具节点
# from agent.env_utils import ZHIPU_API_KEY
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

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
}

chart_mcp_server_config = {
    'url': 'https://mcp.api-inference.modelscope.net/0e9816d0af3647/sse',
    'transport': 'sse',
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



class BasicToolsNode:
    """
    异步工具节点，用于并发执行AIMessage中请求的工具调用

    功能:
    1. 接收工具列表并建立名称索引
    2. 并发执行消息中的工具调用请求
    3. 自动处理同步/异步工具适配
    """
    def __init__(self, tools: list):
        """初始化工具节点
        Args:
            tools: 工具列表，每个工具需包含name属性
        """
        self.tools_by_name = {tool.name:tool for tool in tools} # 所有工具名字

    async def __call__(self, state: Dict[str, Any], **kwargs) -> Dict[str, List[ToolMessage]]:
        """异步调用入口
        Args:
            inputs: 输入字典，需包含"messages"字段
        Returns:
            包含ToolMessage列表的字典
        Raises:
            ValueError: 当输入无效时抛出
        """
        # 1. 输入验证
        if not (messages := state.get("messages")):
            raise ValueError("输入数据中未找到消息内容")  # 改进后的中文错误提示
        message: AIMessage = messages[-1]  # 取最新消息: AIMessage

        # 2. 并发执行工具调用
        outputs = await self._execute_tool_calls(message.tool_calls)
        return {"messages": outputs}

    async def _execute_tool_calls(self, tool_calls: List[Dict]) -> List[ToolMessage]:
        """执行实际工具调用
        Args:
            tool_calls: 工具调用请求列表
        Returns:
            ToolMessage结果列表
        """

        async def _invoke_tool(tool_call: Dict) -> ToolMessage:
            """执行单个工具调用
            Args:
                tool_call: 工具调用请求字典，需包含name/args/id字段
            Returns:
                封装的ToolMessage
            Raises:
                KeyError: 工具未注册时抛出
                RuntimeError: 工具调用失败时抛出
            """
            try:
                # 3. 异步调用工具
                tool = self.tools_by_name.get(tool_call["name"])
                if not tool:
                    raise KeyError(f"未注册的工具: {tool_call['name']}")

                if hasattr(tool, 'ainvoke'):  # 优先使用异步方法
                    tool_result = await tool.ainvoke(tool_call["args"])
                else:  # 同步工具通过线程池转异步
                    loop = asyncio.get_running_loop()
                    tool_result = await loop.run_in_executor(
                        None,  # 使用默认线程池
                        tool.invoke,  # 同步调用方法
                        tool_call["args"]  # 参数
                    )
                # 4. 构造ToolMessage
                return ToolMessage(
                content=json.dumps(tool_result, ensure_ascii=False),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
            except Exception as e:
                raise RuntimeError(f"工具调用失败: {tool_call['name']}") from e

        try:
            # 5. 并发执行所有工具调用
            # '''
            # asyncio.gather() 是 Python 异步编程中用于并发调度多个协程的核心函数，其核心行为包括：
            # 并发执行: 所有传入的协程会被同时调度到事件循环中，通过非阻塞 I/O 实现并行处理。
            # 结果收集: 按输入顺序返回所有协程的结果（或异常），与任务完成顺序无关。
            # 异常处理: 默认情况下，任一任务失败会立即取消其他任务并抛出异常；若设置 return_exceptions=True，则异常会作为结果
            # '''
            return await asyncio.gather(*[_invoke_tool(tool_call) for tool_call in tool_calls])
        except Exception as e:
            raise RuntimeError("并发执行工具时发生错误") from e

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
        return {"messages": [ await llm_with_tools.ainvoke(state["messages"])]}

    builder.add_node('chatbot', chatbot)

    tool_node = BasicToolsNode(tools)
    builder.add_node('tools', tool_node)

    builder.add_conditional_edges(
        "chatbot",
        route_tools_func,
        {"tools": "tools", END: END}
    )

    builder.add_edge(start_key='tools', end_key='chatbot')
    builder.add_edge(START, end_key='chatbot')
    graph = builder.compile()
    return graph


agent=asyncio.run(create_graph())

# 图工厂函数，LangGraph 将自动调用它来创建图
# def agent():
#     return asyncio.run(create_graph())