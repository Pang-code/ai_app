from typing import TypedDict, Literal

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from agent.init_llm import qwen_llm as llm


class State(TypedDict):
    joke: str          # 生成的冷笑话内容
    topic: str         # 用户指定主题
    feedback: str      # 笑话差评/优化改进建议
    funny_or_not: str  # 幽默评级（比如：好笑/一般/不好笑）


# 结构化输出模型（用于LLM评估反馈）
class Feedback(BaseModel):
    """使用此工具来结构化你的响应"""
    grade: Literal["funny", "not funny"] = Field(
        description="判断笑话是否幽默",
        examples=["funny", "not funny"]
    )
    feedback: str = Field(
        description="若不幽默，提供改进建议",
        example="可以加入双关语或意外结局"
    )

# 节点函数
def generator_func(state: State):
    """由大模型生成一个冷笑话的节点"""
    prompt = (
        f"根据反馈改进笑话: {state['feedback']}\n主题: {state['topic']}"
        if state.get("feedback", None)
        else f"创作一个关于{state['topic']}的笑话"
    )
    # 第一种
    # resp= llm.invoke(prompt)
    # return {'joke': resp.content}

    # 第二种
    chain = llm | StrOutputParser()
    resp = chain.invoke(prompt)
    return {'joke': resp}

# 节点函数
def evaluator_func(state: State):
    """评估状态中的冷笑话"""

    # 第一种方法
    # chain = llm.with_structured_output(Feedback)
    # resp  = chain.invoke(
    #     # f"评估此笑话的幽默程度: \n{state['joke']}\n"
    #     # "注意: 幽默应包含意外性或巧妙措辞"
    #     # f"请用 JSON 格式评估此笑话的幽默程度: \n{state['joke']}\n"
    #     # "注意: 幽默应包含意外性或巧妙措辞，请输出 json 格式的评估结果"
    #     f"请严格按照以下 JSON 格式评估此笑话的幽默程度: \n{state['joke']}\n"
    #     "JSON 格式必须包含 'grade' 和 'feedback' 两个字段，grade 的值只能是 'funny' 或 'not funny'，feedback 是改进建议。"
    # )
    # # llm.bind_tools([Feedback])
    # return {
    #     'feedback': resp.feedback,
    #     'funny_or_not': resp.grade
    # }

    # 第二种
    chain = llm.bind_tools([Feedback])
    evaluation = chain.invoke(
            f"评估此笑话的幽默程度: \n{state['joke']}\n"
            "注意: 幽默应包含意外性或巧妙措辞"
        )
    evaluation = evaluation.tool_calls[-1]['args']
    return {
        "funny_or_not": evaluation['grade'],
        "feedback": evaluation['feedback']
    }


# 条件边的路由函数
def route_func(state: State) -> str:
    """动态路由决策函数"""
    return 'Accepted' if state.get("funny_or_not", None) == "funny" else 'Rejected+Feedback'

# 构建一个工作流
builder = StateGraph(State)

builder.add_node('generator', generator_func)
builder.add_node('evaluator', evaluator_func)



builder.add_edge(START, 'generator')
builder.add_edge('generator', 'evaluator')
builder.add_conditional_edges(
    'evaluator',
    route_func,
    {
    "Accepted": END, # 合格则结束
    "Rejected+Feedback": "generator" # 不合格则循环优化
}
)


graph=builder.compile()