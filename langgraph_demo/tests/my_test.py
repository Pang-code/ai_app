from langgraph_sdk import get_sync_client

from langgraph_sdk import get_client
import asyncio

# 连接本地 langgraph dev 启动的服务
client = get_sync_client(url="http://localhost:2024")

# 同步循环接收流式返回
for chunk in client.runs.stream(
        None,  # Thread ID = None 临时一次性会话，不持久化历史
        "agent",  # 图名称，必须匹配 langgraph.json 内定义的助手名
        input={
            "messages": [{
                "role": "human",
                "content": "今天深圳的天气",
            }],
        },
        stream_mode="messages-tuple",
        # stream_mode="messages",
):
    # print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    # print('in chunk.data')
    if isinstance(chunk.data,list) and 'type' in chunk.data[0] and chunk.data[0]['type'] == 'AIMessageChunk':
        print(chunk.data[0]['content'], end='|')

    # print("\n\n")
