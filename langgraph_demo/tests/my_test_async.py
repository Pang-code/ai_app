from langgraph_sdk import get_sync_client

from langgraph_sdk import get_client
import asyncio

# 连接本地启动的 LangGraph API 服务
client = get_client(url="http://localhost:2024")

async def main():
    # 流式订阅图执行输出
    async for chunk in client.runs.stream(
        None,  # Thread ID，None = 无会话线程（单次临时运行）
        "agent",  # 助手名称，对应 langgraph.json 里定义的图名称
        input={
            "messages": [{
                "role": "human",
                "content": "今天深圳的天气?",
            }],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

asyncio.run(main())


# # 连接本地 langgraph dev 启动的服务
# client = get_sync_client(url="http://localhost:2024")
#
# # 同步循环接收流式返回
# for chunk in client.runs.stream(
#     None,  # Thread ID = None 临时一次性会话，不持久化历史
#     "agent",  # 图名称，必须匹配 langgraph.json 内定义的助手名
#     input={
#         "messages": [{
#             "role": "human",
#             "content": "What is LangGraph?",
#         }],
#     },
#     stream_mode="messages-tuple",
# ):
#     print(f"Receiving new event of type: {chunk.event}...")
#     print(chunk.data)
#     print("\n\n")