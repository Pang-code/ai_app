from langchain_core.tools import tool


@tool(name="calculate", parse_docstring=True)
def calculate(a: float, b: float, operation: str) -> float:
    """工具函数：计算两个数字的运算结果"""
    print(f"调用 calculate 工具，第一个数字：{a}，第二个数字：{b}，运算类型：{operation}")

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


print(calculate.name)
# 输出: calculate
print(calculate.description)
# 输出: 工具函数：计算两个数字的运算结果
print(calculate.args)
print(calculate.args_schema.model_json_schema())
print(calculate.return_direct)
