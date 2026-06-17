import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings

model_name = "BAAI/bge-small-zh-v1.5"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity

bge_hf_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


def embedding_2_file(source_file, output_file):
    """读取原始的美食评论数据，通过调用Embedding模型，得到向量，并保持到新文件中"""
    # 步骤：1、准备数据，并读取
    df = pd.read_csv(source_file, index_col=0)
    df = df[['Time', 'ProductId', 'UserId', 'Score', 'Summary', 'Text']]
    print(df.head(2))

    # 步骤2：清洗数据和 合并数据
    # df = df.dropna()
    # 把评论的摘要和内容字段合并成 一个字段（方便后续处理）
    df['text_content'] = 'Summary: ' + df.Summary.str.strip() + "; Text: " + df.Text.str.strip()


    df['embedding'] = df.text_content.apply(lambda x: text_2_embedding(x))

    df.to_csv(output_file)

def text_2_embedding(text):
    resp = bge_hf_embedding.embed_documents(
        [text]
    )
    return resp[0]

if __name__ == '__main__':
    embedding_2_file(source_file='../datas/fine_food_reviews_100.csv', output_file='../datas/fine_food_reviews_100_embedding.csv.csv')
