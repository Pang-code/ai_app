from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class CustomQwen3Embeddings(Embeddings):

    def __init__(self, model_name):
        self.qwen3_embedding = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.qwen3_embedding.encode(texts)


if __name__ == '__main__':
    qwen3 = CustomQwen3Embeddings("Qwen/Qwen3-Embedding-0.6B")
    resp = qwen3.embed_documents(
        ['I like large language models.',
         '今天的天气非常不错！'
        ]
    )

    print(resp[0])
    print(len(resp[0]))