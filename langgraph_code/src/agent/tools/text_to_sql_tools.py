
from langchain_core.tools import BaseTool
from agent.utils.db_utils import MySQLDatabaseManager, db_manager
from agent.utils.log_utils import log
from typing import Optional, List


class ListTablesTool(BaseTool):
    """列出数据库中的所有表及其描述信息"""

    name: str = "sql_db_list_tables"
    description: str = "列出MySQL数据库中的所有表名及其描述信息。当需要了解数据库中有哪些表时使用此工具。"

    # 数据库管理器实例（需要在初始化时传入）
    db_manager: MySQLDatabaseManager

    def _run(self) -> str:
        """执行工具逻辑：获取所有表名及注释"""
        try:
            tables_info = self.db_manager.get_tables_with_comments()

            result = f"数据库中共有 {len(tables_info)} 个表:\n\n"
            for i, table_info in enumerate(tables_info):
                table_name = table_info['table_name']
                table_comment = table_info['table_comment']

                # 处理空描述的情况
                if not table_comment or table_comment.isspace():
                    description_display = "（暂无描述）"
                else:
                    description_display = table_comment

                result += f"{i + 1}. 表名: {table_name}\n"
                result += f"   描述: {description_display}\n\n"

            return result


        except Exception as e:

            log.exception(e)
            return f"获取数据库表信息失败: {str(e)}"


    async def _run(self) -> str:
        return self._run()

from pydantic import BaseModel, Field, create_model


class TableSchemaTool(BaseTool):
    """获取表的模式信息"""

    name: str = "sql_db_schema"
    description: str = (
        "获取MySQL数据库中指定表的详细模式信息，包括列定义、主键、外键等。"
        "输入应为逗号分隔的表名列表，或留空获取所有表的模式信息。"
    )
    db_manager: MySQLDatabaseManager


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # self.db_manager = db_manager
        self.args_schema = create_model("TableSchemaToolArgs",table_namesj= (Optional[List[str]],Field(description="表名列表。")))


    def _run(self, table_names: Optional[List[str]] = None) -> str:
        try:

            # table_list = None
            # # 将输入的逗号分隔字符串转为列表
            # if table_names:
            #     table_names = table_names.strip()
            #     table_list = [t.strip() for t in table_names.split(",")] if table_names else None
            # 调用之前实现的 get_table_schema 方法
            schema_info = self.db_manager.get_table_schema(table_names)
            return schema_info  if schema_info else "未找到匹配的表"
        except Exception as e:
            log.exception(e)
            return f"获取表结构信息失败: {str(e)}"

    async def _run(self) -> str:
        return self._run()



class SQLQueryTool(BaseTool):
    """在MySQL数据库上执行安全的SELECT查询并返回结果"""

    name: str = "sql_db_query"
    description: str = "在MySQL数据库上执行安全的SELECT查询并返回结果。输入应为有效的SQL SELECT查询语句。"
    db_manager: MySQLDatabaseManager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.db_manager = db_manager
        # 定义工具的参数模型，用于LangChain的类型检查
        self.args_schema = create_model(
            "SQLQueryToolArgs",
            query=(str, Field(..., description="有效的SQL SELECT查询语句"))
        )

    def _run(self, query: str) -> str:
        """执行工具逻辑"""
        try:
            result = self.db_manager.execute_query(query)
            return result
        except Exception as e:
            return f"执行查询时出错: {str(e)}"

    async def _run(self) -> str:
        return self._run()



class SQLQueryCheckerTool(BaseTool):
    """检查SQL查询语法"""

    name: str = "sql_db_query_checker"
    description: str = "检查SQL查询语句的语法是否正确，提供验证反馈。输入应为要检查的SQL查询。"
    db_manager: MySQLDatabaseManager

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # self.db_manager = db_manager
        # 定义工具的参数模型
        self.args_schema = create_model(
            "SQLQueryCheckerToolArgs",
            query=(str, Field(..., description="需要检查的SQL查询语句"))
        )

    def _run(self, query: str) -> str:
        """执行工具逻辑"""
        try:
            result = self.db_manager.validate_query(query)
            return result
        except Exception as e:
            return f"SQL语法检查时出错: {str(e)}"


    async def _run(self) -> str:
        return self._run()

if __name__ == '__main__':
    # 配置数据库连接信息
    username = 'root'
    password = '123123'
    host = '127.0.0.1'
    port = 3306
    database = 'test_db4'

    # 构建连接字符串（补全了mysql+pymysql前缀）
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"

    # 初始化数据库管理器
    manager = MySQLDatabaseManager(connection_string)

    # 初始化工具实例
    # tool = ListTablesTool(db_manager=manager)
    # # 调用工具查询表名
    # print(tool.invoke({}))

    # # 初始化工具实例
    # tool = TableSchemaTool(db_manager=manager)
    # # 调用工具 查询表结构
    # print(tool.invoke({"table_names": ["table1",'table2']}))

    # 初始化工具实例
    # tool = SQLQueryTool(db_manager=manager)
    # # 调用工具 查询数据
    # print(tool.invoke({"query": "SELECT * FROM table1"}))

    # 初始化工具实例
    tool = SQLQueryCheckerTool(db_manager=manager)
    # 调用工具 检查SQL语法
    print(tool.invoke({"query": "SELECT * FROM table1"}))
    #  不保证完全正确  例如：select count() from table1