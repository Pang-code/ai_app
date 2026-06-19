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
                "content": "给当前用户的并返回一个祝福语。",
            }],
        },
            config={"configurable": {"user_name": "张三"}}
    ):

        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

asyncio.run(main())

