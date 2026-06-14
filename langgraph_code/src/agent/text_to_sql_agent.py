from langchain.agents import create_agent
from agent.init_llm import deepseek_llm
from agent.tools.tool_demo2 import web_search
from agent.tools.tool_demo3 import MySearchTool

my_search=MySearchTool()  #

# 创建智能体实例
agent = create_agent(
    deepseek_llm,
    tools=[ MySearchTool],
    system_prompt="你是一个智能助手。尽可能的调用工具回答用户的问题"
)

from typing import List
from langchain_core.tools import BaseTool
from agent.tools.text_to_sql_tools import (
    ListTablesTool,
    TableSchemaTool,
    SQLQueryTool,
    SQLQueryCheckerTool
)
from agent.utils.db_utils import MySQLDatabaseManager


def get_tools(
        host: str,
        port: int,
        username: str,
        password: str,
        database: str
) -> List[BaseTool]:
    """
    创建数据库Agent所需的所有工具实例

    Args:
        host: 数据库主机地址
        port: 数据库端口
        username: 数据库用户名
        password: 数据库密码
        database: 数据库名

    Returns:
        List[BaseTool]: 工具实例列表
    """
    # 构建数据库连接字符串
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"

    # 初始化数据库管理器
    manager = MySQLDatabaseManager(connection_string)

    # 返回所有工具实例
    return [
        ListTablesTool(db_manager=manager),
        TableSchemaTool(db_manager=manager),
        SQLQueryTool(db_manager=manager),
        SQLQueryCheckerTool(db_manager=manager),
    ]

tools=get_tools("localhost", 3306, "root", "123456", "test")



system_prompt = """
你是一个专门设计用于与SQL数据库交互的AI代理。

给定一个输入问题，你需要按照以下步骤操作：
1. 创建一个语法正确的{ dialect }查询语句
2. 执行查询并查看结果
3. 基于查询结果返回最终答案

除非用户明确指定要获取的具体示例数量，否则始终将查询结果限制为最多{ top_k }条。

你可以通过相关列对结果进行排序，以返回数据库中最有意义的示例。
永远不要查询特定表的所有列，只获取与问题相关的列。

在执行查询之前，你必须仔细检查查询语句。如果在执行查询时遇到错误，请重写查询并再次尝试。

绝对不要对数据库执行任何数据操作语言（DML）语句（如INSERT、UPDATE、DELETE、DROP等）。

开始处理问题时，你应该始终先查看数据库中有哪些表可以查询。不要跳过这一步。

然后，你应该查询最相关表的模式结构信息。
""".format(
    dialect="MySQL",    # 数据库方言（如MySQL、SQLite等）
    top_k=5                # 默认返回结果的最大数量
)


agent = create_agent(
    deepseek_llm,
    tools=tools,
    system_prompt=system_prompt
)



# langgraph dev --allow-blocking  # 允许阻塞的操作