# 自定义工具节点
# from agent.env_utils import ZHIPU_API_KEY
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.types import interrupt, Command

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

        tool_name = message.tool_calls[0]['name'] if message.tool_calls else None
        # if tool_name == 'get-tickets' or tool_name == 'webSearchSogou':
        if tool_name == 'get-tickets':
            response = interrupt(
                f"AI大模型尝试调用工具 `{tool_name}`, \n"
                "请审核并选择: 批准（y）或直接给我工具执行的答案。"
            )
            # 根据人工响应类型处理
            if response["answer"] == "y":
                pass  # 直接使用原参数继续执行
            else:
                return {"messages": [ToolMessage(
                    content=f"人工终止了该工具的调用，给出的理由或者答案是:{response['answer']}",
                    name=tool_name,
                    tool_call_id=message.tool_calls[0]['id'],
                )]}



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
    # graph = builder.compile()

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


# agent=asyncio.run(create_graph())

# 图工厂函数，LangGraph 将自动调用它来创建图
# def agent():
#     return asyncio.run(create_graph())



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

    # def get_answer(tool_message, user_answer):
    #     """让人介入，并且给一个问题的答案"""
    #     tool_name = tool_message.tool_calls[0]['name']
    #     answer = (
    #         f"人工强制终止了工具：{tool_name}的执行，拒绝的理由是：{user_answer}"
    #     )
    #
    #     # 创建一个消息
    #     new_message = [
    #         ToolMessage(content=answer, tool_call_id=tool_message.tool_calls[0]["id"]),
    #         AIMessage(content=answer)
    #     ]
    #
    #     # 把新人造的消息，添加到工作流的state中
    #     graph.update_state(  # 手动修改state
    #         config=config,
    #         values={'messages': new_message}
    #     )




    async def execute_graph(user_input: str) -> str:
        """ 执行工作流的函数 """
        result = ''  # AI助手的最后一条消息
        # for chunk in graph.astream(input=None, config, stream_mode='values'):

        # if user_input.strip().lower() != 'y':  # 正常的用户提问
        #     current_state = graph.get_state(config)
        #     if current_state.next:  # 如果有下一步，则当前工作流处在中断中
        #         tools_script_message = current_state.values['messages'][-1]# 通过提供关于请求的更改/改变主意的指示来满足工具调用
        #         get_answer(tools_script_message, user_input)
        #         message = graph.get_state(config).values['messages'][-1]
        #         result = message.content
        #         return  result
        #     else:
        #         # 不是可等待对象（Awaitable），因此不能直接用于 await 表达式，必须通过
        #         async for chunk in graph.astream({'messages': ('user',user_input)}, config, stream_mode='values'):
        #             result = print_message(chunk, result)
        # else:  # 用户想继续工具的调用 输入y
        #     async for chunk in graph.astream(None, config, stream_mode='values'):
        #         result = print_message(chunk, result)
        current_state = graph.get_state(config)
        if current_state.next:  # 出现了工作流的中断
            human_command = Command(resume={'answer': user_input})
            async for chunk in graph.astream(human_command, config, stream_mode='values'):
                result = print_message(chunk, result)
            return result
        else:
            async for chunk in graph.astream({'messages': ('user', user_input)}, config, stream_mode='values'):
                result = print_message(chunk, result)
                # if chunk.get('__interrupt__', None):
                #     # result = f"AI助手马上根据你要求，执行{chunk['__interrupt__']['tool_name']}工具。您是否批准继续执行"
                #     print(chunk['__interrupt__'])


        current_state = graph.get_state(config)
        if current_state.next:  # 出现了工作流的中断
            # result = f"AI助手马上根据你要求，执行{tool_name}工具。您是否批准继续执行？输入'y'继续；否则，请说明你的理由"
            result = current_state.interrupts[0].value

        return result


    # 执行工作流
    while True:
        user_input = input('用户: ')
        res = await execute_graph(user_input)
        print('AI: ', res)

if __name__ == '__main__':
    asyncio.run(run_graph())
    # 明天广州南到深圳北最早的一班车是什么时候