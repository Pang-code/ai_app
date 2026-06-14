from init_llm import deepseek_llm,tongyi_llm

# 输出解释器


from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# 1. 定义结构
class Movie(BaseModel):
    """数据模型类 povo 电影"""
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")
    director: str = Field(description="导演")
    rating: float = Field(description="评分（10分制）")


# 可以支持qwen
# 2. 创建解析器和提示模板
parser = JsonOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_template("""
回答用户问题。
问题：{question}
你必须始终输出一个包含title(电影标题)和year(上映年份)的director(导演)和rating(评分（10分制）) JSON 对象。
""")

# 3. 创建链
# chain = prompt | deepseek_reasoner_llm | parser
chain = prompt | tongyi_llm | parser
# chain = prompt | tongyi_llm | StrOutputParser()

# 4. 调用（返回字典）
response = chain.invoke({"question": "介绍电影《盗梦空间》"})
print(response)






# 5. 绑定工具方式

runnable=tongyi_llm.bind_tools( [Movie])
respj = runnable.invoke("介绍电影《盗梦空间》")


print(respj.tool_calls[-1]['args'])

respj.pretty_print()