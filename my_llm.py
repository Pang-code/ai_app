from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from env_utils import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL,
    ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL,
    GOOGLE_API_KEY, GOOGLE_BASE_URL,
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
    #开启思考模式
    # temperature=0.5,
    # max_tokens=1024,
    # timeout=60,
    # reasoning_effort="low",
    # max_retries=2,
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

    """
    invoke()是最直接、最常用的模型调用方法。它的工作模式是阻塞式的，即程序会等待模型完全生成整个响应后，再一次性将结果返回给用户。
    支持单条消息、消息列表（字典格式）、消息列表（消息对象格式）。
    """

    print("invoke()调用-单条消息")
    # 支持单条消息
    print(deepseek_llm.invoke("你是谁？"))

    print("invoke()调用-消息列表（字典格式）")
    # 支持消息列表（字典格式）
    conversation = [
        {"role": "system", "content": "你是一个有帮助的助手，可以将汉语翻译成英语。"},
        {"role": "user", "content": "翻译: 我喜欢编程"},
        {"role": "assistant", "content": "I love programming."},
        {"role": "user", "content": "翻译: 我喜欢大模型"}
    ]

    print(deepseek_llm.invoke(conversation))

    print("invoke()调用-消息列表（消息对象格式）")
    # 支持消息列表（消息对象格式）
    # SystemMessage, HumanMessage, AIMessage）
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

    conversation = [
        SystemMessage("你是一个有帮助的助手，可以将汉语翻译成英语。"),
        HumanMessage("翻译: 我喜欢编程"),
        AIMessage("I love programming."),
        HumanMessage("翻译: 我喜欢大模型")
    ]
    print(deepseek_llm.invoke(conversation))

    """
    流式传输调用大模型允许大语言模型（LLM）在生成内容的过程中，逐块（Chunk）地实时输出结果，而不是等待整个响应完全生成后再一次性返回。流式调用大模型使用方式是通过调用 model.stream()方法会返回一个迭代器（Iterator），你可以通过循环来实时处理每一个新生成的内容块。
    """
    print("流式传输调用大模型")
    from typing import Iterator
    from langchain_core.messages import AIMessageChunk

    resp: Iterator[AIMessageChunk] = deepseek_llm.stream("使用20个字给我介绍什么是大模型？")

    for chunk in resp:
        # print(chunk,type(chunk))
        # end="" 避免打印时自动换行，flush=True 及时刷新输出
        # print(chunk.content, end="|", flush=True)
        print(chunk.content, end="", flush=True)

    print("批量调用大模型")

    """
    处理功能是一种通过并行处理多个独立请求来显著提升性能、降低成本的强大机制。批处理的核心思想是将多个独立的请求集合成一个批次，并行发送给模型处理。这与逐个顺序调用（invoke）相比，能大幅减少网络往返开销和等待时间，尤其适合处理问答、文本分类、情感分析等独立任务。
    """

    from langchain_core.runnables.utils import Output

    responses: list[Output] = deepseek_llm.batch([
        "为什么鹦鹉的羽毛是彩色的？",
        "飞机是如何飞行的？",
        "什么是量子计算？"
    ],
        config={
            'max_concurrency': 5  # 限制最大并发数为5
        }

    )

    for response in responses:
        print(response.content)

    print("异步调用大模型")
    import asyncio
    import time
    from langchain.chat_models import init_chat_model

    from env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

    # 初始化模型
    llm = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )


    async def demo_async_invoke():
        """演示单个异步调用的非阻塞特性"""
        print("=== 演示：ainvoke 的异步（非阻塞）效果 ===")

        print("程序开始...")

        # 1. 发起一个异步请求，但不等待它完成
        print(">>> 发起异步模型调用 (ainvoke)...")
        async_task = llm.ainvoke("用一句话解释人工智能。")

        # 2. 在等待模型响应的同时，主程序可以继续执行其他任务
        print(">>> 模型请求已发送，程序无需等待，继续执行...")
        for i in range(3):
            # 等待1s
            time.sleep(1)
            print(f">>> 正在执行第{i + 1}个任务... ")

        # 3. 现在，我们需要模型的结果了，所以用 await 等待它完成
        print(">>> 其他任务已完成，现在等待模型返回结果...")
        response = await async_task  # 此时才开始等待

        print(f">>> 模型返回: {response.content}")


    async def demo_async_stream():
        """演示异步调用的非阻塞特性"""
        print("=== 演示：astream 的异步（非阻塞）效果 ===")

        print("程序开始...")

        # 1. 发起异步流式请求，但不立即处理结果
        print(">>> 发起异步流式调用 (astream)...")
        stream_resp = llm.astream("请一句话解释机器学习的基本概念。")

        # 2. 在等待流式响应的同时，执行其他任务
        print(">>> 流式请求已发送，程序无需等待，继续执行...")
        for i in range(3):
            # 等待1s
            time.sleep(1)
            print(f">>> 正在执行第{i + 1}个任务... ")

        # 3. 现在开始处理流式结果
        print(">>> 其他任务已完成，开始处理流式结果...")

        print(">>> 流式输出: ", end="", flush=True)
        async for chunk in stream_resp:
            if hasattr(chunk, 'content'):
                print(chunk.content, end="", flush=True)
        print(">>> 流式输出结束\n")


    async def demo_async_batch():
        """演示单个异步调用的非阻塞特性"""
        print("=== 演示：abatch 的异步（非阻塞）效果 ===")

        print("程序开始...")

        # 准备批量输入（即使是单个输入，也用列表形式）
        questions = ["用一句话说明深度学习与传统机器学习的区别"]

        # 1. 发起异步批量请求
        print(">>> 发起异步批量调用 (abatch)...")
        batch_resp = llm.abatch(questions)

        # 2. 在等待批量处理的同时，执行其他任务
        print(">>> 批量请求已发送，程序无需等待，继续执行...")
        for i in range(3):
            # 等待1s
            time.sleep(1)
            print(f">>> 正在执行第{i + 1}个任务... ")

        # 3. 等待批量处理结果
        print(">>> 其他任务已完成，现在等待批量处理结果...")
        responses = await batch_resp

        for response in responses:
            print(f">>> 批量响应: {response.content}")


    async def main():
        """主函数"""
        await demo_async_invoke()
        await demo_async_stream()
        await demo_async_batch()


    if __name__ == "__main__":
        asyncio.run(main())

    # print(qwen_llm.invoke("你是谁？"))
    # print(doubao_llm.invoke("你是谁？"))
    # print(zhipu_llm.invoke("你是谁？"))
    # print(kimi_llm.invoke("你是谁？"))
    # print(minimax_llm.invoke("你是谁？"))
