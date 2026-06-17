import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
import ast

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


def cosine_distance(a, b):
    """
    计算两个向量的余弦距离
    :param a:
    :param b:
    :return:
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_text(input, embedding_file, top_n=3):
    """
    根据用户输入的问题，进行语义检索，返回最相似的前top_n个结果
    :param input:
    :param top_n:
    :return:
    """
    df_data = pd.read_csv(embedding_file)
    # 把字符串变成向量，保存到新字段
    df_data['embedding_vector'] = df_data['embedding'].apply(ast.literal_eval)
    input_vector = text_2_embedding(input)



    df_data['similarity'] = df_data.embedding_vector.apply(lambda x: cosine_distance(x, input_vector))

    res = (
        df_data.sort_values(by='similarity', ascending=False)
        .head(top_n)
        .text_content.str.replace('Summary: ', "")  # text_content是字段名
        .str.replace('; Text: ', '; ')
    )

    for r in res:
        print(r)
        print('-' * 30)



if __name__ == '__main__':
    embedding_2_file(source_file='../datas/fine_food_reviews_100.csv', output_file='../datas/fine_food_reviews_100_embedding.csv')
    search_text(input='delicious beans', embedding_file='../datas/fine_food_reviews_100_embedding.csv')
