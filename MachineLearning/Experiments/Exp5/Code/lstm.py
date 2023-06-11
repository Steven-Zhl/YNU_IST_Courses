from os import path
from re import sub, compile

import numpy as np
import tensorflow as tf
from gensim.models import Word2Vec
from jieba import cut
from keras import callbacks
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.losses import BinaryCrossentropy  # 二分类交叉熵损失函数
from keras.models import Sequential  # 顺序模型
from pandas import read_csv, DataFrame
from sklearn.model_selection import train_test_split  # 划分训练集和测试集

MAX_NB_WORDS = 50000  # 设置最频繁使用的50000个词
MAX_SEQUENCE_LENGTH = 250  # 每条cut_review最大的长度
EMBEDDING_DIM = 100  # 设置Embedding层的维度
# 设定超参数
BATCH_SIZE = 100  # 批处理大小
EPOCHS = 30  # 迭代次数
LSTM_UNITS = 64  # LSTM单元数


def dataprocess(data: DataFrame, stopwords: list):
    """
    数据预处理，将data['comments']直接分成词列表
    :param data:
    :return:
    """
    content1 = data.replace(" ", "")  # 去掉文本中的空格
    pattern = compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字，去掉符号
    content2 = sub(pattern, "", str(content1))  # 把文本中匹配到的字符替换成空字符
    return [w for w in list(cut(content2)) if w not in stopwords]  # 直接分词，data['comments']格式为list[list[str]]


def stopwordlist(filepath):
    """
    加载停用词表
    :param filepath:
    :return:
    """
    stopwords = [line.strip() for line in open(filepath, "r", encoding="utf-8").readlines()]
    return stopwords


def trainWord2Vec(data, savePath: str = None) -> Word2Vec:
    """
    训练Word2Vec模型并保存
    :param savePath: Word2Vec模型的路径
    :return: Word2Vec模型
    """
    model = Word2Vec(data["comments"].values, vector_size=EMBEDDING_DIM, window=5, workers=8)
    if not savePath:
        savePath = "w2v.model"
    model.save(savePath)  # 保存模型
    return model


def data2Index(data, savePath: str = None) -> np.ndarray:
    """
    将data转换为索引矩阵
    :param data:
    :return:
    """
    indexMatrix = np.zeros((len(data), MAX_SEQUENCE_LENGTH), dtype="int32")
    for i in range(len(data)):
        review = data["comments"][i]  # 一条评论
        for j in range(len(review)):
            if j < MAX_SEQUENCE_LENGTH:  # 限制每条评论的长度，只取前250个词
                word = review[j]
                if word in wordsList:
                    indexMatrix[i][j] = wordsList.index(word)
                else:
                    indexMatrix[i][j] = 0  # 未出现在词表中的词用0表示
    # 保存data的索引矩阵
    if not savePath:
        savePath = "indexMatrix.npy"
    np.save(savePath, indexMatrix)
    return indexMatrix


if __name__ == "__main__":
    # 数据预处理
    stopwords = stopwordlist("Data/chineseStopWords.txt")  # 读取停用词表
    data = read_csv("Data/comments.csv")  # 读取数据集
    data["comments"] = data.comments.apply(dataprocess, args=(stopwords,))  # 将data['comments']处理为list[str]的分词形式
    print(data.info)  # 查看数据集信息
    print(data.head())  # 查看数据集前5行

    # 训练Word2Vec模型，将词转换为词向量
    w2vModel = (Word2Vec.load("w2v.model") if path.exists("w2v.model") else trainWord2Vec(data, "w2v.model"))
    wordsList = w2vModel.wv.index_to_key  # 获取词表
    wordVectors = w2vModel.wv.vectors  # 获取词向量矩阵
    print("wordVectors.shape:", wordVectors.shape)  # Word2Vec模型的词向量矩阵

    # 将data转换为索引矩阵
    indexMatrix = (
        np.load("indexMatrix.npy") if path.exists("indexMatrix.npy") else data2Index(data, "indexMatrix.npy"))
    print("indexMatrix.shape:", indexMatrix.shape)  # 索引矩阵的尺度应该约为(9918)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(indexMatrix, data["label"], test_size=0.3)
    X_train = X_train.squeeze()  # 不使用squeeze()的话，在训练LSTM模型时会多出一个None的维度导致报错

    # LSTM
    # 搭建LSTM模型
    model = Sequential()
    model.add(Embedding(input_dim=MAX_NB_WORDS, output_dim=EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
    model.add(LSTM(activation="sigmoid", units=LSTM_UNITS, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(Dense(units=512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(units=1, activation="sigmoid"))
    model.summary()
    model.compile(loss=BinaryCrossentropy(), optimizer="adam", metrics=["accuracy"])
    # 训练模型，并使用tensorboard可视化
    writer = tf.summary.create_file_writer("./LSTM_Logs")
    tb_callback = callbacks.TensorBoard(log_dir="./LSTM_Logs", histogram_freq=1)
    model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, callbacks=[tb_callback])
    # 保存模型
    model.save("LSTM.h5")
    # 评估模型
    score = model.evaluate(X_test, y_test)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
