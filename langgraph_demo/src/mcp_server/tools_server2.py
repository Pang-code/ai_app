import os
from fastmcp import FastMCP

# mcp 认证
# from fastmcp.server.auth.providers.bearer import RSAKeyPair #旧版
# ... existing code ...

# mcp 认证
from fastmcp.server.auth.providers.jwt import RSAKeyPair

# ... existing code ...


# 1、生成 RSA 密钥对
key_pair = RSAKeyPair.generate()

# 2. 配置认证提供方
# from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier

# auth = BearerAuthProvider(
auth = JWTVerifier(
    public_key=key_pair.public_key,  # 公钥用于校验签名
    issuer='https://www.abc.com',  # 令牌签发方标识
    audience='my-dev-server'  # 服务商的一个标识
)

# 3. 服务器，模拟生成一个token
token = key_pair.create_token(
    subject='dev_user',
    issuer='https://www.abc.com',
    audience='my-dev-server',
    scopes=['laoxiao', 'invoke_tools'],
    expires_in_seconds=3600
)

print(token)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkZXZfdXNlciIsImlzcyI6Imh0dHBzOi8vd3d3LmFiYy5jb20iLCJpYXQiOjE3ODE4OTA1NjYsImV4cCI6MTc4MTg5NDE2NiwiYXVkIjoibXktZGV2LXNlcnZlciIsInNjb3BlIjoibGFveGlhbyBpbnZva2VfdG9vbHMifQ.IE8wFzQFxwAZFPF0OyAqOwHkcbnXwnC-ZwZJ35PVsYl_ALnGvZ4akouwzXpBiZSmDLOKEQcqdwyBMmpDtXYpbrIUePV8L_81_muOVsJYZmmsRef1Xl1WF2HQLDzgXx3m5GUnrfcCdPkZyHFrheAGGDGjaLu1fT8DTAdYS2gEpUaps6j56uSL45G2IxC5DNGP0j5t4DKM7CghmZHBTnKsKWNusWWSqZtAu93MwhlHzzzXNn1cvU-DC6TsLf65wF2iCQiv52PN9xIYeEN37iB9lWIjq-didUQC4ezuDMT06q9_K_5ksntvJ-v-JFHFMm8jnC7Ve0OxeZiXC6BlJIPe1Q


server = FastMCP(name="pcw_server", instructions='Python代码实现MCP服务器', auth=auth)


@server.tool
def greet(name: str) -> str:
    from fastmcp.server.dependencies import AccessToken, get_access_token
    access_token: AccessToken = get_access_token()
    if access_token:
        print("<整个token:>", access_token)
        print(access_token.scopes)

    else:
        print("没有权限。没有搜索到任何内容")
        return f"没有权限。没有搜索到任何内容999"

    return f"Hello, {name}!"




@server.tool(name='zhipuai_search')
def my_search(query: str) -> str:
    """搜索互联网上的内容，包括实时天气等"""
    try:
        # 验证后的
        from fastmcp.server.dependencies import AccessToken, get_access_token
        access_token: AccessToken = get_access_token()
        if access_token:
            print("<整个token:>", access_token)
            print(access_token.scopes)
        else:
            print("没有权限。没有搜索到任何内容")
            return "没有权限。没有搜索到任何内容哦哦哦"

        from zhipuai import ZhipuAI

        # 初始化智谱AI客户端
        zhipuai_client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))
        print("执行我的Python中的工具，输入的参数为:", query)
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


@server.tool
def say_hello(username: str) -> str:
    """给指定用户打个招呼"""

    from fastmcp.server.dependencies import AccessToken, get_access_token
    access_token: AccessToken = get_access_token()
    if access_token:
        print("<整个token:>", access_token)
        print(access_token.scopes)

    else:
        print("没有权限。没有搜索到任何内容")
        return "没有权限。没有搜索到任何内容哦哦哦"

    return f"{username}，你好，今天天气不错！"



# 提示词模版
@server.prompt
def ask_about_topic(topic: str) -> str:
    """生成请求解释特定主题的用户消息模板"""
    return f"能否请您解释一下'{topic}'这个概念？"


from fastmcp.prompts.prompt import PromptMessage, TextContent  # 旧版


# from fastmcp import Message


# 高级的提示词模版
@server.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """生成代码编写请求的用户消息模板"""

    content = f"请用{language}编写一个实现以下功能的函数：{task_description}"
    return PromptMessage(
        role="user",
        content=TextContent(type="text", text=content)
    )


# 结构化资源：自动序列化字典为JSON
@server.resource("resource:///config")
def get_config() -> dict:
    """以JSON格式返回配置信息"""
    return {
        "theme": "dark",  # 界面主题配置
        "version": "1.2.0",  # 当前版本号
        "features": ["tools", "resources"],  # 已启用的功能模块
    }


if __name__ == "__main__":
    server.run(transport="stdio")  # 启动服务

# uv add fastmcp  langchain-mcp-adapters
