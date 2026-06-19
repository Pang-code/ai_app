import asyncio

from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm

# Python MCP 服务端的连接配置  sse
# python_mcp_server_config = {
#     'url': 'http://127.0.0.1:8080/sse',
#     'transport': 'sse',
# }

# # Python MCP 服务端的连接配置  streamable
python_mcp_server_config = {
    'url': 'http://127.0.0.1:8080/streamable',
    'transport': 'streamable_http',
}

from langchain_mcp_adapters.client import MultiServerMCPClient

# MCP的客户端
mcp_client = MultiServerMCPClient(
    {
        'python_mcp': python_mcp_server_config,
    }
)


async def create_agent():
    """必须是异步函数中"""
    mcp_tools = await mcp_client.get_tools()

    print(mcp_tools)

    p = await mcp_client.get_prompt(
        server_name='python_mcp',  # mcp 服务端名称
        prompt_name='ask_about_topic',
        arguments={'topic': '深度学习'}
    )

    print(p)
    data = await mcp_client.get_resources(
        server_name='python_mcp',  # mcp 服务端名称
        uris='resource:///config'
    )
    print(data[0])
    print(data[0].data)

    my_agent7 = create_react_agent(
        llm,
        tools=mcp_tools,
        prompt="你是一个智能助手,尽可能的调用工具回答用户的问题",

    )

    return my_agent7


agent = asyncio.run(create_agent())
