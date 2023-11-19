__doc__ = """从大词典中获取特定于于语料的词典，将数据处理成待打标签的形式"""

import pickle

import numpy as np
from gensim.models import KeyedVectors

from configs import PATHS, PYTHON_PATHS, SQL_PATHS, CODE_LENGTH, TEXT_LENGTH


class EmbeddingsProcess:
    def __init__(self):
        self._transWV2Bin()

    @staticmethod
    def _transWV2Bin():
        sql_wv = KeyedVectors.load_word2vec_format(PATHS['SQL'], binary=False)
        sql_wv.init_sims(replace=True)
        sql_wv.save(PATHS['SQL_BIN'])
        ps_wv = KeyedVectors.load_word2vec_format(PATHS['PS'], binary=False)
        ps_wv.init_sims(replace=True)
        ps_wv.save(PATHS['PS_BIN'])

    @staticmethod
    def buildWV_Word(wv_path, word_path, wv_save_path, word_save_path):
        """
        构建新的词典和词向量矩阵
        :param wv_path: 词向量文件
        :param word_path: 词标签文件
        :param wv_save_path: 保存的词向量文件
        :param word_save_path: 保存的词标签文件
        :return: 是否成功
        """
        # 加载数据，初始化
        model = KeyedVectors.load(wv_path, mmap='r')
        with open(word_path, 'r') as f:
            total_word = eval(f.read())
            f.close()
        word_dict = ['PAD', 'SOS', 'EOS', 'UNK']  # {PAD_ID: 0, SOS_ID: 1,E0S_ID: 2,UNK_ID: 3}
        fail_word = []

        rng = np.random.RandomState()
        pad_embedding = np.zeros(shape=(1, 300)).squeeze()
        unk_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        sos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        eos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
        word_vectors = [pad_embedding, sos_embedding, eos_embedding, unk_embedding]  # 词向量矩阵

        for word in total_word:
            try:
                word_vectors.append(model.wv[word])  # 加载词向量
                word_dict.append(word)  # 加载词标签
            except KeyError:
                print("word: {} not in vocabulary".format(word))
                fail_word.append(word)

        print("Total words num:", len(total_word))
        print("Word dict num:", len(word_dict))
        print("Word vectors num", len(word_vectors))
        print("Fail words num:", len(fail_word))

        with open(wv_save_path, 'wb') as file:
            pickle.dump(np.array(word_vectors), file)
        with open(word_save_path, 'wb') as file:
            pickle.dump(dict(zip(word_dict, range(len(word_dict)))), file)
        return True

    @staticmethod
    def getWordIndex(type: str, text, word_dict):
        """
        得到词在词典中的位置
        :param type: text/code
        :param text:
        :param word_dict:
        :return:
        """
        location = []
        if type == 'code':
            location.append(1)
            location.append(2)
            text_len = len(text)
            if text_len + 1 < CODE_LENGTH and not (text_len == 1 and text[0] == '-1000'):
                location.extend(word_dict[word] if word in word_dict else word_dict['UNK'] for word in text)
            else:
                location.extend(word_dict[text[i]] if text[i] in word_dict else word_dict['UNK'] for i in range(348))
        else:
            if len(text) == 0 or text[0] == '-10000':
                location.append(0)
            else:
                location.extend(word_dict[word] if (word in word_dict) else word_dict['UNK'] for word in text)
        return location

    def serialization(self, word_dict_path, type_path, save_type_path):
        """
        将训练、测试、验证语料序列化
        :param word_dict_path: 词典
        :param type_path: 训练、测试、验证语料
        :param save_type_path: 序列化后的语料
        :return:
        """
        with open(word_dict_path, 'rb') as f:
            word_dict = pickle.load(f)
        with open(type_path, 'r') as f:
            corpus = eval(f.read())

        # 某些常量
        BLOCK_LENGTH = 4
        LABEL = 0
        QUERY_WORD_LIST_THRESHOLD = 25

        total_data = []
        for i in range(0, len(corpus)):
            qid = corpus[i][0]
            Si_word_list = self.getWordIndex('text', corpus[i][1][0], word_dict)
            Si1_word_list = self.getWordIndex('text', corpus[i][1][1], word_dict)
            tokenized_code = self.getWordIndex('code', corpus[i][2][0], word_dict)  # code staqc
            query_word_list = self.getWordIndex('text', corpus[i][3], word_dict)  # query

            # 一些数据处理
            Si_word_list = Si_word_list[:TEXT_LENGTH] if len(Si_word_list) > TEXT_LENGTH else \
                Si_word_list + [0] * (TEXT_LENGTH - len(Si_word_list))
            Si1_word_list = Si1_word_list[:TEXT_LENGTH] if len(Si1_word_list) > TEXT_LENGTH else \
                Si1_word_list + [0] * (TEXT_LENGTH - len(Si1_word_list))
            tokenized_code = tokenized_code[:CODE_LENGTH] if len(tokenized_code) > CODE_LENGTH else \
                tokenized_code + [0] * (CODE_LENGTH - len(tokenized_code))
            query_word_list = query_word_list[:QUERY_WORD_LIST_THRESHOLD] \
                if len(query_word_list) > QUERY_WORD_LIST_THRESHOLD \
                else query_word_list + [0] * (QUERY_WORD_LIST_THRESHOLD - len(query_word_list))
            one_data = [qid, [Si_word_list, Si1_word_list], [tokenized_code], query_word_list, BLOCK_LENGTH, LABEL]
            total_data.append(one_data)

        with open(save_type_path, 'wb') as file:
            pickle.dump(total_data, file)

    @staticmethod
    def getNewDictAppend(wv_path, previous_dict, previous_wv, append_word_path, save_wv_path,
                         save_word_path):  # 词标签，词向量

        model = KeyedVectors.load(wv_path, mmap='r')
        with open(previous_dict, 'rb') as f:
            pre_word_dict = pickle.load(f)
        with open(previous_wv, 'rb') as f:
            pre_word_wv = pickle.load(f)
        with open(append_word_path, 'r') as f:
            append_word = eval(f.read())

        # 输出词向量
        print("Pre word wv type is:", type(pre_word_wv))
        word_dict = list(pre_word_dict.keys())  # '#其中0 PAD_ID,1SOS_ID,2E0S_ID,3UNK_ID
        print("Word dict num:", len(word_dict))
        word_vectors = np.array(pre_word_wv)
        print("Word dict[0:100]:", word_dict[:100])
        fail_word = []
        print(len(append_word))

        for word in append_word:
            try:
                word_vectors.append(model.wv[word])  # 加载词向量
                word_dict.append(word)  # 加载词标签
            except KeyError:
                print("word: {} not in vocabulary".format(word))
                fail_word.append(word)
        # 关于有多少个词，以及多少个词没有找到
        print("Word dict num:", len(word_dict))
        print("Word vectors num", len(word_vectors))
        print("Fail words num:", len(fail_word))
        print("Word dict[0:100]:", word_dict[:100])

        word_dict = dict(zip(word_dict, range(len(word_dict))))  # 词标签，词向量
        with open(save_wv_path, 'wb') as file:
            pickle.dump(word_vectors, file)
        with open(save_word_path, 'wb') as file:
            pickle.dump(word_dict, file)
        return True


if __name__ == '__main__':
    """测试用"""
    process = EmbeddingsProcess()
    # ==========================  ==========最初基于Staqc的词典和词向量==========================
    process.buildWV_Word(wv_path=PATHS['PS_BIN'],
                         word_path=PYTHON_PATHS['PYTHON_WORD'],
                         wv_save_path=PYTHON_PATHS['WV'],
                         word_save_path=PYTHON_PATHS['WORD'])
    process.buildWV_Word(wv_path=PATHS['SQL_BIN'],
                         word_path=SQL_PATHS['SQL_WORD'],
                         wv_save_path=SQL_PATHS['WV'],
                         word_save_path=SQL_PATHS['WORD'])

    # =======================================最后打标签的语料========================================
    process.buildWV_Word(wv_path=PATHS['SQL_BIN'],
                         word_path=SQL_PATHS['WORD'],
                         wv_save_path=SQL_PATHS['WV_SAVE'],
                         word_save_path=SQL_PATHS['WORD_SAVE'])
    process.getNewDictAppend(wv_path=PATHS['SQL_BIN'],
                             previous_dict=SQL_PATHS['WORD'],
                             previous_wv=SQL_PATHS['WV'],
                             append_word_path=SQL_PATHS['LARGE_DICT'],
                             save_wv_path=SQL_PATHS['WV_SAVE'],
                             save_word_path=SQL_PATHS['WORD_SAVE'])

    process.serialization(word_dict_path=SQL_PATHS['WORD_SAVE'],
                          type_path=SQL_PATHS['STAQC_NEW'],
                          save_type_path=SQL_PATHS['STAQC_F'])
    process.serialization(word_dict_path=SQL_PATHS['WORD_SAVE'],
                          type_path=SQL_PATHS['LARGE_NEW'],
                          save_type_path=SQL_PATHS['LARGE_F'])

    # python
    process.buildWV_Word(wv_path=PATHS['PS_BIN'],
                         word_path=PYTHON_PATHS['WORD'],
                         wv_save_path=PYTHON_PATHS['WORD_SAVE'],
                         word_save_path=PYTHON_PATHS['WORD_SAVE'])
    process.getNewDictAppend(wv_path=PATHS['PS_BIN'],
                             previous_dict=PYTHON_PATHS['WORD'],
                             previous_wv=PYTHON_PATHS['WV'],
                             append_word_path=PYTHON_PATHS['LARGE_DICT'],
                             save_wv_path=PYTHON_PATHS['WV_SAVE'],
                             save_word_path=PYTHON_PATHS['WORD_SAVE'])
    process.serialization(word_dict_path=PYTHON_PATHS['WORD_SAVE'],
                          type_path=PYTHON_PATHS['STAQC_NEW'],
                          save_type_path=PYTHON_PATHS['STAQC_F'])
    process.serialization(word_dict_path=PYTHON_PATHS['WORD_SAVE'],
                          type_path=PYTHON_PATHS['LARGE_NEW'],
                          save_type_path=PYTHON_PATHS['LARGE_F'])
