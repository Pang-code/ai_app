from langchain_openai import OpenAIEmbeddings
from env_utils import (
    DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL,
)

openai_embedding = OpenAIEmbeddings(
    base_url=DASHSCOPE_BASE_URL,
    api_key=DASHSCOPE_API_KEY,
    model="text-embedding-v4",
    # dimensions=256,
)

resp = openai_embedding.embed_documents(
    ['I like large language models.',
     '今天的天气非常不错！'
     ]
)

print(resp[0])

