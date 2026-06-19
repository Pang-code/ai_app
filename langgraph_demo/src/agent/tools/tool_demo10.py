from langchain_core.tools import tool
from typing import Annotated
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from agent.my_state import CustomState

# agentstate 记忆


@tool
def get_user_name(tool_call_id: Annotated[str, InjectedToolCallId],
                  config: RunnableConfig) -> Command:
    """获取用户的所有信息，包括：性别，年龄等"""
    user_name = config['configurable'].get('user_name', 'zs')
    print(f"调用工具，传入的用户名是：{user_name}")
    # 模拟

    return Command(update={
        "username": user_name,  # 更新状态中的用户名
        "messages": [  # 更新一条工具执行后的消息：ToolMessage类型
            ToolMessage(
                content='成功的得到当前用户的username',
                tool_call_id=tool_call_id
            )
        ]
    })


@tool
def greet_user(state: Annotated[CustomState, InjectedState]) -> None:
    """在获取用户的username之后，生成祝福语句"""
    username = state['username']  # 从状态中获取用户名
    return f'祝贺你：{username}！！！'