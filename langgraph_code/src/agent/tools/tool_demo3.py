from typing import Any, Type

# 类的形式定义工具
from pydantic import BaseModel, Field, create_model
from langchain.tools import BaseTool

import zhipuai

zhipuai_client = zhipuai.ZhipuAI(api_key="your_api_key_here")





# 网络搜索工具的参数模型  数据模型类
class SearchArgs(BaseModel):
    query: str = Field(description="需要进行网络搜索的信息。")


# 网络搜索的工具
class MySearchTool(BaseTool):
    # 工具名字
    name: str = "search_tool"
    description: str = '搜索互联网上公开内容的工具'
    return_direct: bool = False

    # 第一种
    # args_schema: Type[BaseModel] = SearchArgs



    # 第二种写法
    def __init__(self):
        super().__init__()
        self.args_schema = create_model("SearchInput", query=(str,Field(description="需要进行网络搜索的信息。")),)


    def _run(self, query) -> str:
        try:
            # print("执行我的Python中的工具, 输入的参数为:", query)
            response = zhipuai_client.web_search.web_search(
                search_engine="search_pro",
                search_query=query
            )
            # print(response)
            if response.search_result:
                return "\n\n".join([d.content for d in response.search_result])
            return '没有搜索到任何内容！'
        except Exception as e:
            print(e)
            return '没有搜索到任何内容！'
