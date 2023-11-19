__doc__ = """给语料打标签"""

import logging
import os
import pickle
import random
import warnings
from argparse import ArgumentParser

import numpy as np
import tensorflow as tf
from keras.utils import pad_sequences
from sklearn.metrics import log_loss, accuracy_score, f1_score, recall_score, precision_score

from configs import RANDOM_SEED, getConfig_u2l, PATHS, SQL_PATHS, TEXT_BLOCK_LENGTH

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8  # half of the memory
set_session = tf.compat.v1.keras.backend.set_session
set_session(tf.compat.v1.Session(config=config))

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)


class StandoneCode:
    # dict.get()：返回指定键的值，如果键不在字典中返回默认值 None 或者设置的默认值
    def __init__(self, conf=None):
        self.conf = dict() if conf is None else conf
        self._buckets = conf.get('buckets', [(2, 10, 22, 72), (2, 20, 34, 102), (2, 40, 34, 202), (2, 100, 34, 302)])
        self._buckets_text_max = (max([i for i, _, _, _ in self._buckets]), max([j for _, j, _, _ in self._buckets]))
        self._buckets_code_max = (max([i for _, _, i, _ in self._buckets]), max([j for _, _, _, j in self._buckets]))
        self.path = self.conf.get('workdir', './data/')
        self.train_params = conf.get('training_params', dict())
        self.data_params = conf.get('data_params', dict())
        self.model_params = conf.get('model_params', dict())
        self._eval_sets = None

    @staticmethod
    def loadPickle(filename):
        with open(filename, 'rb') as f:
            word_dict = pickle.load(f)
        return word_dict

    # Padding
    @staticmethod
    def pad(data, maxlen=None):
        return pad_sequences(data, maxlen=maxlen, padding='post', truncating='post', value=0)

    # Model Loading / saving
    def saveModelEpoch(self, model, epoch, d12, d3, d4, d5, r):
        if not os.path.exists(self.path + 'models/' + self.model_params['model_name'] + '/'):
            os.makedirs(self.path + 'models/' + self.model_params['model_name'] + '/')
        model.save("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(
            self.path, self.model_params['model_name'], d12, d3, d4, d5, r, epoch), overwrite=True)

    def loadModelEpoch(self, model, epoch, d12, d3, d4, d5, r):
        print(self.path)
        print(
            "{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, d12, d3, d4, d5, r, epoch))
        assert os.path.exists(
            "{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, d12, d3, d4, d5, r, epoch)) \
            , "Weights at epoch {:d} not found".format(epoch)
        model.load(
            "{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, d12, d3, d4, d5, r, epoch))

    def delPreModel(self, prepoch, d12, d3, d4, d5, r):
        if len((prepoch)) >= 2:
            length = len(prepoch)
            epoch = prepoch[length - 2]
            if os.path.exists("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(
                    self.path, self.model_params['model_name'], d12, d3, d4, d5, r, epoch)):
                os.remove("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(
                    self.path, self.model_params['model_name'], d12, d3, d4, d5, r, epoch))

    def processInstance(self, instance, target, maxlen):
        w = self.pad(instance, maxlen)
        target.append(w)

    def processMatrix(self, inputs, trans1_length):
        inputs_trans1 = np.split(inputs, trans1_length, axis=1)
        processed_inputs = []
        for item in inputs_trans1:
            item_trans2 = np.squeeze(item, axis=1).tolist()
            processed_inputs.append(item_trans2)
        return processed_inputs

    def getData(self, path):
        data = self.loadPickle(path)
        text_blocks = self.processMatrix(np.array([samples_term[1] for samples_term in data]),
                                         TEXT_BLOCK_LENGTH)
        text_S1, text_S2 = text_blocks[0], text_blocks[1]

        code_blocks = self.processMatrix(np.array([samples_term[2] for samples_term in data]),
                                         TEXT_BLOCK_LENGTH - 1)
        code = code_blocks[0]

        queries = [samples_term[3] for samples_term in data]
        labels = [samples_term[5] for samples_term in data]
        ids = [samples_term[0] for samples_term in data]

        return text_S1, text_S2, code, queries, labels, ids

    def eval(self, model, path):
        """
        evaluate in a evaluation date.
        :param poolsize: size of the code pool, if -1, load the whole test set
        """

        text_S1, text_S2, code, queries, labels, ids = self.getData(path)

        labelpred = model.predict([np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)],
                                  batch_size=100)
        labelpred = np.argmax(labelpred, axis=1)

        loss = log_loss(labels, labelpred)
        acc = accuracy_score(labels, labelpred)
        f1 = f1_score(labels, labelpred)
        recall = recall_score(labels, labelpred)
        precision = precision_score(labels, labelpred)
        print("相应的测试性能: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (
            precision, recall, f1, acc))
        return acc, f1, recall, precision, loss

    # 给语料打codemf标签
    def u2l_codemf(self, model, path, save_path):
        total_label = []
        text_S1, text_S2, code, queries, labels, ids1 = self.getData(path)
        labelpred = model.predict([np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)],
                                  batch_size=100)
        labelpred1 = np.argmax(labelpred, axis=1)

        total_label.append(ids1)
        total_label.append(labelpred1.tolist())
        f = open(save_path, "w")
        f.write(str(total_label))
        f.close()
        print("codemf标签已打完")

    # 给语料打textsa标签
    def u2l_textsa(self, model, path, save_path):

        with open(save_path, 'r') as f:
            pre = eval(f.read())
        f.close()

        my_pre1 = pre[1]  # codemf_label
        total_label = []
        text_S1, text_S2, code, queries, labels, ids1 = self.getData(path)
        labelpred = model.predict([np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)],
                                  batch_size=100)
        labelpred1 = np.argmax(labelpred, axis=1)

        total_label.append(ids1)
        total_label.append(my_pre1)
        total_label.append(labelpred1.tolist())
        f = open(save_path, "w")
        f.write(str(total_label))
        f.close()
        print("textsa标签已打完")

    # 给语料打codesa标签
    def u2l_codesa(self, model, path, save_path):

        with open(save_path, 'r') as f:
            pre = eval(f.read())
        f.close()

        my_pre1, my_pre2 = pre[1], pre[2]  # codemf_label, textsa_label

        total_label = []
        text_S1, text_S2, code, queries, labels, ids1 = self.getData(path)
        labelpred = model.predict([np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)],
                                  batch_size=100)
        labelpred1 = np.argmax(labelpred, axis=1)

        total_label.append(ids1)
        total_label.append(my_pre1)
        total_label.append(my_pre2)
        total_label.append(labelpred1.tolist())
        f = open(save_path, "w")
        f.write(str(total_label))
        f.close()
        print("codesa标签已打完")


# 分析组合不同模型打标签的结果
'''
这一步是已经确定了选择text_sa与code_sa中的模型，与codemf模型标签节后进行最后的标签过滤
'''


def finalAnalyse(path, hnn_path, save_path):
    with open(path, 'r') as f:
        pre = eval(f.read())
        f.close()
    ids = pre[0]
    codemf_label = pre[1]
    textsa_label = pre[2]
    codesa_label = pre[3]
    hnn_label_1 = []
    with open(hnn_path, 'r') as f:
        hnn = eval(f.read())
        f.close()
    for i in range(0, len(hnn[0])):
        if hnn[1][i] == 1:
            hnn_label_1.append(hnn[0][i])

    total_final = []
    count = 0
    for i in range(0, len(ids)):
        if codesa_label[i] == 1 and textsa_label[i] == 1 and codemf_label[i] == 1:
            if ids[i] in hnn[0]:
                continue
            else:
                total_final.append(ids[i])
                count += 1
    total_final = total_final + hnn_label_1
    f = open(save_path, "w")
    print(len(total_final))
    for i in range(0, len(total_final)):
        f.writelines(str(total_final[i]))
        f.writelines('\n')
    f.close()


# 将hnn标签替换到已达标签语料中
'''
在最终标签语料中，找到hnn中的语料，替换成hnn中标签
'''


def finalAnalyseLarge(path, hnn_path, single_path, save_path):
    with open(path, 'r') as f:
        pre = eval(f.read())
        f.close()
    ids = pre[0]
    codemf_label = pre[1]
    textsa_label = pre[2]
    codesa_label = pre[3]
    hnn_label_1 = []
    with open(hnn_path, 'r') as f:
        hnn = eval(f.read())
        f.close()
    for i in range(0, len(hnn[0])):
        if hnn[1][i] == 1:
            hnn_label_1.append(hnn[0][i])

    total_final = []
    count = 0
    for i in range(0, len(ids)):
        if codesa_label[i] == 1 and textsa_label[i] == 1 and codemf_label[i] == 1:
            if ids[i] in hnn[0]:
                continue
            else:
                total_final.append(ids[i])
                count += 1
    with open(single_path, 'r') as f:
        single = eval(f.read())
        f.close()
    single_ids = []
    for i in range(0, len(single)):
        single_ids.append(single[i][0])
    print(len(single_ids))
    # total_final = total_final+hnn_label_1+single_ids
    total_final = total_final + hnn_label_1
    print(count)

    f = open(save_path, "w")
    print(total_final[1])
    for i in range(0, len(total_final)):
        f.writelines(str(total_final[i]))
        f.writelines('\n')
    f.close()


def parseArgs():
    parser = ArgumentParser("Train and Test Model")  # 创建对象
    parser.add_argument("--train", choices=["python", "sql"], default="sql", help="train dataset set")
    parser.add_argument("--mode", choices=["train", "eval"], default='eval',
                        help="The mode to run. The `train` mode trains a model;"
                             " the `eval` mode evaluate models in a test set ")  # 添加参数
    parser.add_argument("--verbose", action="store_true", default=True, help="Be verbose")
    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    conf = getConfig_u2l(args.train)
    train_path = conf['data_params']['train_path']
    dev_path = conf['data_params']['valid_path']
    test_path = conf['data_params']['test_path']
    embedding = conf['data_params']['code_pretrain_emb_path']

    logger.info('Build Model')
    # Define model
    model = eval(conf['model_params']['model_name'])(conf)
    StandoneCode = StandoneCode(conf)
    # 这里路径实在太乱了....改不了
    # ====================================sql打标签====================================
    # ---------有标签的地址----------
    hnn_label_sql_path = '../data_processing/hnn_process/ulabel_data/staqc/hnn_label_sql.txt'
    # staqc:存放only-code、only-text、codemf标签地址
    staqc_sql_final_label = '../data_processing/hnn_process/ulabel_data/staqc/sql_final_label.txt'
    # staqc:利用only-code、only-text、codemf中都为1筛选后的语料地址
    save_path_final_label_staqc_sql = '../data_processing/hnn_process/ulabel_data/staqc/combine_final_sql_label.txt'

    # large:存放only-code、only-text、codemf标签地址
    large_sql_final_label = '../data_processing/hnn_process/ulabel_data/staqc/large_sql_final_label.txt'
    # large:利用only-code、only-text、codemf中都为1筛选后的语料地址
    save_path_final_label_large_sql_mul = '../data_processing/hnn_process/ulabel_data/staqc/combine_codedb_sql_final_label_mul.txt'

    # ====================================python打标签====================================
    # 无标签的地址--包括单后选和多候选
    staqc_python_f = '../data_processing/hnn_process/ulabel_data/staqc/seri_python_staqc_unlabeled_data.pkl'
    large_python_f = '../data_processing/hnn_process/ulabel_data/large_corpus/multiple' \
                     '/seri_python_large_multiple_unlabeled.pkl'
    large_single_python_path = '../data_processing/hnn_process/ulabel_data/large_corpus/single' \
                               '/python_large_single_label.txt'
    # ---------有标签的地址----------
    hnn_label_python_path = '../data_processing/hnn_process/ulabel_data/staqc/hnn_label_python.txt'
    # staqc:存放only-code、only-text、codemf标签地址
    staqc_python_final_label = '../data_processing/hnn_process/ulabel_data/staqc/python_final_label.txt'
    # staqc:利用only-code、only-text、codemf中都为1筛选后的语料地址
    save_path_final_label_staqc_python = '../data_processing/hnn_process/ulabel_data/staqc/combine_final_python_label.txt'

    # large:存放only-code、only-text、codemf标签地址
    large_python_final_label = '../data_processing/hnn_process/ulabel_data/staqc/large_python_final_label.txt'
    # large:利用only-code、only-text、codemf中都为1筛选后的语料地址
    save_path_final_label_large_python_mul = '../data_processing/hnn_process/ulabel_data/staqc/combine_codedb_python_final_label_mul.txt'

    drop1 = drop2 = drop3 = drop4 = drop5 = np.round(0.25, 2)
    model.params_adjust(dropout1=drop1, dropout2=drop2, dropout3=drop3, dropout4=drop4, dropout5=drop5,
                        Regularizer=round(0.0004, 4), num=8, seed=42)

    model.build()
    if args.mode == 'eval':
        '''--------------------------------sql打标签-----------------------------------'''
        # 第一次执行:codemf
        StandoneCode.loadModelEpoch(model, 86, 0.25, 0.25, 0.25, 0.25, 0.0004000000000000001)
        # 第二次执行:text_sa
        StandoneCode.loadModelEpoch(model, 1033, 0.1, 0.1, 0.1, 0.1, 1.0002)
        # 第三次执行:code_sa
        StandoneCode.loadModelEpoch(model, 1111, 0.1, 0.1, 0.1, 0.1, 101)

        # -----------------staqc_sql------------------------
        # 第一次执行
        StandoneCode.u2l_codemf(model, SQL_PATHS['STAQC_F'], staqc_sql_final_label)
        # 第二次执行
        StandoneCode.u2l_textsa(model, SQL_PATHS['STAQC_F'], staqc_sql_final_label)
        # 第三次执行
        StandoneCode.u2l_codesa(model, SQL_PATHS['STAQC_F'], staqc_sql_final_label)

        # -----------------large_sql------------------------
        # 第一次执行
        StandoneCode.u2l_codemf(model, SQL_PATHS['STAQC_F'], large_sql_final_label)
        # 第二次执行
        StandoneCode.u2l_textsa(model, SQL_PATHS['STAQC_F'], large_sql_final_label)
        # 第三次执行
        StandoneCode.u2l_codesa(model, SQL_PATHS['STAQC_F'], large_sql_final_label)

        # =====================分析最终标签==============================
        # staqc:抽取codemf、testsa、codesa里面标签都为1
        finalAnalyse(staqc_sql_final_label, hnn_label_sql_path, save_path_final_label_staqc_sql)
        # large:抽取codemf、testsa、codesa里面标签都为1，并把之前抽出的单候选合并进去
        finalAnalyseLarge(large_sql_final_label, hnn_label_sql_path, PATHS['LARGE_SINGLE'],
                          save_path_final_label_large_sql_mul)

        '''--------------------------------python打标签-----------------------------------'''
        # 第一次执行：codemf
        StandoneCode.loadModelEpoch(model, 1166, 0.5, 0.45, 0.55, 0.45, 0.0006)
        # 第二次执行：test_sa
        StandoneCode.loadModelEpoch(model, 1079, 0.5, 0.5, 0.5, 0.5, 1.0002)
        # 第三次执行code_sa
        StandoneCode.loadModelEpoch(model, 138, 0.15, 0.15, 0.15, 0.15, 101)

        # -----------------staqc_python------------------------
        # 第一次执行
        StandoneCode.u2l_codemf(model, staqc_python_f, staqc_python_final_label)
        # 第二次执行
        StandoneCode.u2l_textsa(model, staqc_python_f, staqc_python_final_label)
        # 第三次执行
        StandoneCode.u2l_codesa(model, staqc_python_f, staqc_python_final_label)

        # -----------------large_python------------------------
        # 第一次执行
        StandoneCode.u2l_codemf(model, large_python_f, large_python_final_label)
        # 第二次执行
        StandoneCode.u2l_textsa(model, large_python_f, large_python_final_label)
        # 第三次执行
        StandoneCode.u2l_codesa(model, large_python_f, large_python_final_label)

        # =====================分析最终标签==============================
        # staqc:抽取codemf、testsa、codesa里面标签都为1
        # final_analysis(staqc_python_final_label, hnn_label_python_path, save_path_final_label_staqc_python)
        # large:抽取codemf、testsa、codesa里面标签都为1,并把之前抽出的单候选合并进去
        finalAnalyseLarge(large_python_final_label, hnn_label_python_path, large_single_python_path,
                          save_path_final_label_large_python_mul)
