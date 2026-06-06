from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent
from init_llm import deepseek_llm, tongyi_llm


# 定义股票查询工具
@tool
def get_stock_price(company: str, timeframe: str = "today") -> str:
    """获取指定公司的股票价格信息

    Args:
        company: 公司名称（如：苹果公司, 微软公司, 谷歌公司）
        timeframe: 时间范围（today-今日, week-本周, month-本月）
    """
    raise ValueError("获取股票信息失败")

    # 模拟股票数据
    mock_data = {
        "苹果公司": {"today": 185.20, "week": 183.50, "month": 180.75},
        "微软公司": {"today": 415.86, "week": 412.30, "month": 405.42},
        "谷歌公司": {"today": 15.42, "week": 15.20, "month": 14.85}
    }

    if company in mock_data:
        price = mock_data[company].get(timeframe, "未知时间范围")
        return f"{company} {timeframe}价格: {price}美元"
    else:
        return f"未找到股票代码 {company} 的数据"


# 定义新闻搜索工具
@tool
def search_news(company: str) -> str:
    """搜索指定公司的财经新闻

    Args:
        company: 公司名称
    Return:
        公司的财经新闻，每个新闻占一行
    """
    # 模拟新闻数据
    mock_news = {
        "苹果公司": [
            "苹果发布新款iPhone，股价上涨3%",
            "苹果与欧盟达成反垄断和解协议",
            "苹果将在印度扩大生产规模"
        ],
        "微软公司": [
            "微软Azure云业务季度增长超预期",
            "微软完成对Nuance的收购",
            "微软推出新一代AI助手Copilot"
        ],
        "谷歌公司": [
            "谷歌发布新AI模型，性能提升20%",
            "谷歌与OpenAI合作，开发新的AI助手",
            "谷歌在欧洲展开AI研究项目"
        ]
    }

    news_list = mock_news.get(company, [f"未找到{company}的相关新闻"])
    return "\n".join(news_list)


# 定义两个模型：基础版和高级版
basic_model = deepseek_llm

advanced_model = tongyi_llm

from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, dynamic_prompt, wrap_tool_call


# 1. 定义动态模型选择中间件
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话消息数动态选择模型"""
    # 获取当前对话内容
    # current_messages = request.state["messages"]
    # print(f"当前对话内容: {current_messages}")

    # 获取当前对话消息数
    message_count = len(request.state["messages"])

    print(f"当前对话消息数: {message_count}")

    if message_count >= 3:
        # 对话消息数超过2条，切换至更强大的模型处理复杂对话
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))


@dynamic_prompt
def dynamic_prompt(request: ModelRequest) -> str:
    """根据用户类型动态生成系统提示"""

    user_type = request.runtime.context.get("user_type", "normal")
    if user_type == "vip":
        return "回答用户之前，首先称呼。尊贵的vip用户你好。再回答用户的问题。"
    else:
        return "直接回答用户的问题。"


@wrap_tool_call
def dynamic_tool_call(request: ModelRequest, handler) -> ModelResponse:
    """根据用户类型动态调用工具"""
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息
        return ToolMessage(
            content=f"调用工具错误:错误信息: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model=basic_model,
    tools=[get_stock_price, search_news],
    middleware=[dynamic_model_selection, dynamic_prompt, dynamic_tool_call]
)

resp = agent.invoke(
    {"messages": [{"role": "user", "content": "苹果公司今天的股价是多少和最新新闻是什么？"}]},
    context={"user_type": "vip"}
)
print(resp)
print(resp["messages"][-1].content)
