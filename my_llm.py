from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from env_utils import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL,
    ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL,
    GOOGLE_API_KEY,GOOGLE_BASE_URL,
    DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL,
    DOUBAO_API_KEY, DOUBAO_BASE_URL,
    ZHIPUAI_API_KEY, ZHIPUAI_BASE_URL,
    KIMI_API_KEY, KIMI_BASE_URL,
    OPENAI_API_KEY, OPENAI_BASE_URL,
    HUNYUAN_APP_ID, HUNYUAN_SECRET_ID, HUNYUAN_SECRET_KEY,
    MINIMAX_API_KEY, MINIMAX_BASE_URL,

)


# ==================== DeepSeek ====================
deepseek_llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_BASE_URL,
    model="deepseek-v4-pro",
)

# ==================== OpenAI ChatGPT ====================
# openai_llm = ChatOpenAI(
#     api_key=OPENAI_API_KEY,
#     base_url=OPENAI_BASE_URL,
#     model="gpt-4",
# )
# ==================== Anthropic Claude ====================
# claude_llm = ChatAnthropic(
#     api_key=ANTHROPIC_API_KEY,
#     base_url=ANTHROPIC_BASE_URL,
#     model="claude-sonnet-4-20250514",
# )

# ==================== Google Gemini ====================
# gemini_llm = ChatGoogleGenerativeAI(
#     google_api_key=GOOGLE_API_KEY,
#     base_url=GOOGLE_BASE_URL,
#     model="gemini-2.5-pro",
# )

# ==================== 阿里通义千问 Qwen ====================
# from langchain_qwq import ChatQwen
qwen_llm = ChatOpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,
    model="qwen3.7-max",
)

# ==================== 字节豆包 Doubao ====================
doubao_llm = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model="doubao-seed-2-0-pro-260215",
)



# ==================== zhipu ====================
zhipu_llm = ChatOpenAI(
    api_key=ZHIPUAI_API_KEY,
    base_url=ZHIPUAI_BASE_URL,
    model="glm-5.1",
)

# ==================== KIMI ====================
kimi_llm = ChatOpenAI(
    api_key=KIMI_API_KEY,
    base_url=KIMI_BASE_URL,
    model="kimi-k2.6",
)


# ==================== MINIMAX ====================
minimax_llm = ChatOpenAI(
    api_key=MINIMAX_API_KEY,
    base_url=MINIMAX_BASE_URL,
    model="MiniMax-M2.5",
)


# from langchain_ollama import ChatOllama
# ollama_llm = ChatOllama(
#     base_url="http://192.168.1.106:11434",
#     model="deepseek-r1:1.5b",
# )


# todo 新版的
# from langchain_community.chat_models import ChatHunyuan, ChatTongyi, ChatZhipuAI
# hunyuan_llm = ChatHunyuan(
#     hunyuan_app_id = HUNYUAN_APP_ID,
#     hunyuan_secret_id = HUNYUAN_SECRET_ID,
#     hunyuan_secret_key = HUNYUAN_SECRET_KEY,
#     model="hunyuan-lite",
# )
#
# tongyi_llm = ChatTongyi(
#     api_key=DASHSCOPE_API_KEY,
#     model="qwen-plus",
# )
#
#
# zhipu_llm = ChatZhipuAI(
#     api_key=ZHIPUAI_API_KEY,
#     model="glm-4",
# )

if __name__ == '__main__':
    pass
    print(deepseek_llm.invoke("你是谁？"))
    # print(qwen_llm.invoke("你是谁？"))
    # print(doubao_llm.invoke("你是谁？"))
    # print(zhipu_llm.invoke("你是谁？"))
    # print(kimi_llm.invoke("你是谁？"))
    # print(minimax_llm.invoke("你是谁？"))