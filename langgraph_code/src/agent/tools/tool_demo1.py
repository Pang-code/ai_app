from langchain_core.tools import tool


# 1



# 有两种工具说明 方法1: 直接在工具函数上添加description参数, 方法2: google的格式注释格式
# @tool(name="web_search", description="互联网") # 定义工具，指定工具名称,
@tool(name="web_search", parse_docstring=True) # 定义工具，指定工具名称,
def web_search(query: str):
    """
    互联网
    google的格式
    搜索互联网

    Args:
        query: 搜索查询

    Returns:
        搜索结果

    """
    return f"搜索互联网: {query}"






from langchain.tools import tool

@tool('calculate', parse_docstring=True)
def calculate4(
    a: float,
    b: float,
    operation: str
) -> float:
    """工具函数: 计算两个数字的运算结果

    Args:
        a: 第一个需要输入的数字。
        b: 第二个需要输入的数字。
        operation: 运算类型, 只能是add、subtract、multiply和divide中的任意一个。

    Returns:
        返回两个输入数字的运算结果。
    """
    print(f"调用 calculate 工具, 第一个数字: {a}, 第二个数字: {b}, 运算类型: {operation}")

    result = 0.0
    match operation:
        case "add":
            result = a + b
        case "subtract":
            result = a - b
        case "multiply":
            result = a * b
        case "divide":
            if b != 0:
                result = a / b
            else:
                raise ValueError("除数不能为零")
    return result