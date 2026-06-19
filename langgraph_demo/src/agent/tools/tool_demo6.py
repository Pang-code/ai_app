

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Type
from agent.init_llm import qwen_llm as llm

# 1. 构建提示词模板，双变量占位：topic、language
prompt = (
    PromptTemplate.from_template("帮我生成一个简短的，关于{topic}的报幕词。")
    + ", 要求：1、内容搞笑一点；"
    + "2、输出的内容采用{language}。"
)

# 2. 组装链式链路：提示词 → 大模型 → 字符串解析器
chain = prompt | llm | StrOutputParser()

# 3. 定义工具入参 Schema，约束两个入参含义
class ToolArgs(BaseModel):
    topic: str = Field(description="报幕词的主题")
    language: str = Field(description="报幕词采用的语言")

# 4. 将整条 Chain 转为 LangChain 可被 Agent 调用的工具
runnable_tool = chain.as_tool(
    name='chain_tool',
    description='这是一个专门生成报幕词的工具',
    args_schema=ToolArgs
)


if __name__ == '__main__':

    # 打印工具入参完整 JSON Schema（Pydantic 模型转接口规范）
    print(runnable_tool.args_schema.model_json_schema())
    # 打印工具名称
    print(runnable_tool.name)
    # 打印工具功能描述
    print(runnable_tool.description)