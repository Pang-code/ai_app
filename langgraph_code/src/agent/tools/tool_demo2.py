from pydantic import BaseModel, Field

from langchain_core.tools import tool
from zhipuai import api_key

from agent.init_llm import zhipu_llm as zhipuai_client

# zhipuai_client  = zhipuai(api_key=ZHIPUAI_API_KEY)


class SearchArgs(BaseModel):
    query: str = Field(description="搜索查询")


@tool("web_search", description="互联网", args_schema=SearchArgs)
def web_search(query: str, args_schema=SearchArgs, description="互联网", parse_docstring=True):
    # return f"搜索互联网: {query}"




    try:
        resp = zhipuai_client.web_search.web_search(
            search_engine='search_pro',
            search_query=query,
        )
        if resp.search_result:
            return "\n\n".join([d.content for d in resp.search_result])
        return "没有搜索到任何结果"
    except Exception as e:
        print(e)
        return f"Error: {e}"





if __name__ == '__main__':
    print(web_search.name)  # 工具的名字
    print(web_search.description)  # 工具的描述
    print(web_search.args)  # 工具的参数
    print(web_search.args_schema.model_json_schema())


    # 调用
    result = web_search.invoke({"query":"如何使用lanchain"})
    print( result)











#  类的形式
# from pydantic import BaseModel, Field
# from langchain.tools import BaseTool, Type
# from zhipuai import ZhipuAI
#
# # 网络搜索工具的参数模型
# class SearchArgs(BaseModel):
#     query: str = Field(description="需要进行网络搜索的信息。")
#
# # 网络搜索的工具
# class MySearchTool(BaseTool):
#     # 工具名字
#     name: str = "search_tool"
#     description: str = '搜索互联网上公开内容的工具'
#     return_direct: bool = False
#     args_schema: Type[BaseModel] = SearchArgs
#
#     def _run(self, query) -> str:
#         try:
#             # print("执行我的Python中的工具, 输入的参数为:", query)
#             response = zhipuai_client.web_search.web_search(
#                 search_engine="search_pro",
#                 search_query=query
#             )
#             # print(response)
#             if response.search_result:
#                 return "\n\n".join([d.content for d in response.search_result])
#             return '没有搜索到任何内容！'
#         except Exception as e:
#             print(e)
#             return '没有搜索到任何内容！'
#



