import faiss
from langchain_classic import docstore
from langchain_community.docstore import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class CustomQwen3Embeddings(Embeddings):

    def __init__(self, model_name):
        self.qwen3_embedding = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.qwen3_embedding.encode(texts)


qwen3_embedding = CustomQwen3Embeddings("Qwen/Qwen3-Embedding-0.6B")

vector_store = FAISS.load_local("./faiss_db",embeddings=qwen3_embedding,allow_dangerous_deserialization= True)

# 相识度查询
results = vector_store.similarity_search_with_score(query='今天的金融新闻', k=2,filter={"source": "news"}) # 带分数的查询 查询条件 k=2,filter={"source": "news"}

for res, score in results:
    print(type(res))
    print(res.id)
    print(f"* [Score={score:3f}] {res.page_content} [{res.metadata}]")


# 删除指定id的向量
# vector_store.delete(ids=['id1'])
