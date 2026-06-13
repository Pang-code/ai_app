from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from agent.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL,ZHIPUAI_API_KEY,ZHIPUAI_BASE_URL

deepseek_llm: BaseChatModel = init_chat_model(
    model="deepseek-v4-pro",
    # model="deepseek-r1",
    # model_provider="deepseek", # deepseek的
    model_provider="openai",  # 阿里百炼的deepseek
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

#
# openai_llm = init_chat_model(
#     model="gpt-4",
#     model_provider="openai",
#     api_key=OPENAI_API_KEY,
#     base_url=OPENAI_BASE_URL,
# )
#
# anthropic_llm = init_chat_model(
#     model="claude-3-5-haiku-latest",
#     model_provider="anthropic",
#     api_key=ANTHROPIC_API_KEY,
#     base_url=ANTHROPIC_BASE_URL,
# )
#
#
# ollama_llm = init_chat_model(
#     model="deepseek-r1:1.5b",
#     model_provider="ollama",
#     base_url="http://192.168.1.106:11434",
# )
#
#
tongyi_llm = init_chat_model(
    model="qwen3.7-max",
    model_provider="openai",
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,

)
#
zhipu_llm = init_chat_model(
    model="glm-5.1",
    model_provider="openai",
    api_key=ZHIPUAI_API_KEY,
    base_url=ZHIPUAI_BASE_URL,

)


if __name__ == '__main__':
    # print(deepseek_llm.invoke("你是谁？"))
    print(zhipu_llm.invoke("你是谁？"))
    print(zhipu_llm.web)