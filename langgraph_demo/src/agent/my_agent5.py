# 短期记忆
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent

from agent.init_llm import qwen_llm as llm
from agent.my_state import CustomState
from agent.tools.tool_demo9 import get_user_name, greet_user
from agent.tools.tool_demo6 import runnable_tool
from agent.tools.tool_demo8 import get_user_info_by_name
from agent.tools.tool_demo_arg2 import calculate3
# from agent.tools.tool_demo7 import MySearchTool
from langchain_core.messages import AnyMessage, BaseMessage
# from langgraph.prebuilt import AgentState
from langchain_core.runnables import RunnableConfig

from typing import Sequence, TypedDict
from langgraph.checkpoint.memory import InMemorySaver

# checkpointer = InMemorySaver()  短期存储




# PostgreSQL数据库连接配置
DB_URI = 'postgresql://postgres:123456@localhost:5432/langgraph_db'
# DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
# with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

# 必须安装: pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres

# 生产环境: Redis
# pip install -U langgraph langgraph-checkpoint-redis
# DB_URI = "redis://:6379"
# with RedisSaver.from_conn_string(DB_URI) as checkpointer:

    # checkpointer.setup() # todo 第一次使用必执行

    # 构建ReAct智能体状态图
    my_agent5 = create_react_agent(
        llm,
        tools=[calculate3, runnable_tool, get_user_name, greet_user],
        prompt="你是一个智能助手,尽可能的调用工具回答用户的问题",
        checkpointer=checkpointer
    )

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    # resp1 = my_agent5.invoke(
    #     input={"messages": [{"role": "user", "content": "今天，北京的天气怎么样？"}]},
    #     config=config,
    # )
    #
    # print(resp1['messages'][-1].content)
    #
    #
    #
    # resp2 = my_agent5.invoke(
    #     input={"messages": [{"role": "user", "content": "深圳的呢？"}]},
    #     config=config,
    # )
    #
    # print(resp2['messages'][-1].content)


    # 上面是存储
    # 短期记忆会存储到数据库中


    # 下面是获取短期记忆
    resp = list(my_agent5.get_state(config))
    print(resp)