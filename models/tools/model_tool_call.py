from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from my_llm import deepseek_llm


# 大模型调用工具的步骤
# 1. 定义工具
# 2. 与大模型对话,返回调用大模型的请求,并不会主动调用工具
# 3. 根据返回的结果,手动处理,并且把结果告诉大模型
# 4. 大模型根据处理后的结果,回复对用户的问题


# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """获取制定城市的天气
    Args:
        city: 城市名称
        例如: 深圳
    Returns:
        城市天气
    """
    return f"{city}的天气是晴朗的,温度在25摄氏度左右"


# 绑定工具
model_bind_tool = deepseek_llm.bind_tools([get_weather])

# # 返回请求
# resp = model_bind_tool.invoke("深圳的天气")
# print(type(resp))
# print(resp)

messages = []
human_message = HumanMessage(content="北京的天气")
messages.append(human_message)

# 2. 模型生成调用工具请求
response = model_bind_tool.invoke(messages)

print("response", response)
# messages = []
messages.append(response)

# 3.开发者根据模型的响应，调用工具并获取结果
for tool_call in response.tool_calls:
    if tool_call['name'] == 'get_weather':
        # 调用工具并获取结果
        tool_result = get_weather.invoke(tool_call)
        messages.append(tool_result)

# 4. 模型根据工具调用结果生成最终响应
final_response = model_bind_tool.invoke(messages)
print("final_response", final_response)
print(final_response)
