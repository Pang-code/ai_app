import faiss
from langchain_classic import docstore
from langchain_community.docstore import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

# pip install -qU "langchain-chroma>=0.1.2"
class CustomQwen3Embeddings(Embeddings):

    def __init__(self, model_name):
        self.qwen3_embedding = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # return self.qwen3_embedding.encode(texts)
        return self.qwen3_embedding.encode(texts).tolist()



qwen3_embedding = CustomQwen3Embeddings("Qwen/Qwen3-Embedding-0.6B")




from langchain_core.documents import Document

# 2、准备数据（Document）
document_1 = Document(
    page_content="今天早餐我吃了巧克力薄煎饼和炒蛋。",
    metadata={"source": "tweet"},  # 可以随意
)

document_2 = Document(
    page_content="明天的天气预报是阴天多云，最高气温62华氏度。",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="正在用LangChain构建一个激动人心的新项目——快来看看吧！",
    metadata={"source": "tweet"},
)

document_4 = Document(
    page_content="劫匪闯入城市银行，盗走了100万美元现金。",
    metadata={"source": "news"},
)

document_5 = Document(
    page_content="哇！那部电影太精彩了，我已经迫不及待想再看一遍。",
    metadata={"source": "tweet"},
)

document_6 = Document(
    page_content="新iPhone值得这个价格吗？阅读这篇评测一探究竟。",
    metadata={"source": "website"},
)

document_7 = Document(
    page_content="当今世界排名前十的足球运动员。",
    metadata={"source": "website"},
)

document_8 = Document(
    page_content="LangGraph是构建有状态智能体应用的最佳框架！",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="由于对经济衰退的担忧，今日股市下跌500点。",
    metadata={"source": "news"},
)

document_10 = Document(
    page_content="我有种不好的预感，我要被删除了 :(",
    metadata={"source": "tweet"},
)
documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]


from langchain_community.vectorstores import Chroma

vector_store = Chroma(
    collection_name='t_news',
    embedding_function=qwen3_embedding,
    persist_directory='./chroma_db'
)


ids = ['id' + str(i + 1) for i in range(len(documents))]
# 加载
vector_store.add_documents(documents, ids=ids)


# 搜索
# 相识度查询
results = vector_store.similarity_search_with_score(query='今天的金融新闻', k=2,filter={"source": "news"}) # 带分数的查询 查询条件 k=2,filter={"source": "news"}

for res, score in results:
    print(type(res))
    print(res.id)
    print(f"* [Score={score:3f}] {res.page_content} [{res.metadata}]")
