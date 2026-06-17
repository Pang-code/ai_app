# from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# model_name = "BAAI/bge-large-zh-v1.5"
model_name = "BAAI/bge-small-zh-v1.5"
# model_kwargs = {'device': 'cuda'}
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
# bge_hf_embedding = HuggingFaceBgeEmbeddings(
bge_hf_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    # query_instruction="为这个句子生成表示以用于检索相关文章："
)
# 重复赋值，等价于初始化内的参数
# model.query_instruction = "为这个句子生成表示以用于检索相关文章："






resp = bge_hf_embedding.embed_documents(
    ['I like large language models.',
     '今天的天气非常不错！'
     ]
)

print(resp[0])


# 模型会下载到缓存目录下，默认为 ~.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5
# 也可以手动指定缓存目录 在环境变量设置 HF_HOME=your_cache_dir

# pip uninstall torch torchvision torchaudio
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
