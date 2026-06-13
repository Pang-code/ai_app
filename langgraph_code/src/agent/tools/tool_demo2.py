from pydantic import BaseModel, Field

from langchain_core.tools import tool

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











