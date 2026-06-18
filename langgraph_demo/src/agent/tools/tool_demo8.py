from langchain_core.tools import tool
from typing import Annotated
from langchain_core.runnables import RunnableConfig


@tool
def get_user_info_by_name(config: RunnableConfig) -> dict:
    """获取用户的所有信息，包括：性别，年龄等"""
    user_name = config['configurable'].get('user_name', 'zs')
    print(f"调用工具，传入的用户名是：{user_name}")
    # 模拟
    return {'user_name': user_name, 'sex': '男', 'age': 18}

# print(calculate3.name)
# # 输出: calculate
# print(calculate3.description)
# # 输出: 工具函数：计算两个数字的运算结果
# print(calculate3.args)
# print(calculate3.args_schema.model_json_schema())
# print(calculate3.return_direct)
# print(calculate3.invoke({'a': 40, 'b': 2, 'operation': 'multiply'}))