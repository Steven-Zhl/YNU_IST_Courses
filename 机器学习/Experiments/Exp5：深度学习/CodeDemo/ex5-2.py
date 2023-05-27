import re
import pandas as pd
import jieba
import tensorflow as tf
from keras.layers import SpatialDropout1D, Embedding, LSTM, Dense
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split


def dataprocess(data):
    content1 = data.replace(' ', '')  # 去掉文本中的空格
    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字，去掉符号
    content2 = re.sub(pattern, '', str(content1))  # 把文本中匹配到的字符替换成空字符
    return content2

def stopwordlist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


stopwords=stopwordlist('./data_sets/chineseStopWords.txt')

# 设置最频繁使用的50000个词
MAX_NB_WORDS = 50000
# 每条cut_review最大的长度
MAX_SEQUENCE_LENGTH = 250
# 设置Embeddingceng层的维度
EMBEDDING_DIM = 100

data=pd.read_csv('./data_sets/comments.csv')
data['comments']=data.comments.apply(dataprocess)
data['comment']=data.comments.apply(lambda x: " ".join([w for w in list(jieba.cut(x)) if w not in stopwords]))
data=data[['comment','label']]
print(data.info)