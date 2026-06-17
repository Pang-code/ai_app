import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


# liianweng.github.io/posts/2023-06-23-agent/
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

vector_store = Chroma(
    collection_name='t_news',
    embedding_function=qwen3_embedding,
    persist_directory='./chroma_db'
)



def create_dense_db():
    """把网络的关于Agent的博客数据写入向量数据库"""
    loader = WebBaseLoader(
        web_path=('https://lilianweng.github.io/posts/2023-06-23-agent/',),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(  # 使用BeautifulSoup解析器，只解析特定
                class_=("post-content", "post-title", "post-header")  # 指定
            )
        )
    )

    docs_list = loader.load()


    from langchain_text_splitters import RecursiveCharacterTextSplitter
    # 初始化文本分割器，设置块大小1000，重叠200
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # 分割文档
    splits = text_splitter.split_documents(docs_list)

    print('doc的数量为:', len(splits))
    ids = ['id' + str(i + 1) for i in range(len(splits))]
    # 把doc写到向量数据库
    vector_store.add_documents(documents=splits, ids=ids)



create_dense_db()