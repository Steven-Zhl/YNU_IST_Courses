from __future__ import print_function

import os
import tensorflow as tf
import sys
import numpy as np
import random
import pickle
import argparse
random.seed(42)
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")


from sklearn.metrics import *
from configs import *

from models import CodeMF
#from models_no_bidi_SA import CodeMF
#from models_no_SA import CodeMF
#from models2_no_sa import CodeMF
import warnings
warnings.filterwarnings("ignore")

'''
tf.compat.v1.set_random_seed(1)  # 图级种子，使所有操作会话生成的随机序列在会话中可重复，请设置图级种子：
random.seed(1)  # 让每次生成的随机数一致
np.random.seed(1)  #
'''
set_session =  tf.compat.v1.keras.backend.set_session

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.55 #half of the memory
set_session(tf.compat.v1.Session(config=config))


seed = 42
np.random.seed(seed)
tf.random.set_seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
random.seed(seed)

class StandoneCode:
    # dict.get(）：返回指定键的值，如果键不在字典中返回默认值 None 或者设置的默认值
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

    def load_pickle(self, filename):
        with open(filename, 'rb') as f:
            word_dict = pickle.load(f)
        return word_dict

        ##### Data Set #####


    ##### Padding #####
    def pad(self, data, len=None):
        from keras.preprocessing.sequence import pad_sequences
        return pad_sequences(data, maxlen=len, padding='post', truncating='post', value=0)

    ##### Model Loading / saving #####
    def save_model_epoch(self, model, epoch,d12,d3,d4,d5,r):
        if not os.path.exists(self.path + 'models/' + self.model_params['model_name'] + '/'):
            os.makedirs(self.path + 'models/' + self.model_params['model_name'] + '/')
        model.save("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, self.model_params['model_name'], d12,d3,d4,d5,r,epoch),overwrite=True)

    def load_model_epoch(self, model, epoch, d12, d3, d4,d5, r):
        assert os.path.exists(
            "{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, self.model_params['model_name'], d12, d3, d4,d5, r, epoch)) \
            , "Weights at epoch {:d} not found".format(epoch)
        model.load("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, self.model_params['model_name'], d12, d3, d4,d5, r, epoch))

    def del_pre_model(self,prepoch,d12,d3,d4,d5,r):
        if (len((prepoch)))>=2:
            lenth = len(prepoch)
            epoch = prepoch[lenth-2]
            if os.path.exists("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, self.model_params['model_name'], d12, d3, d4,d5, r, epoch)):
                os.remove("{}models/{}/pysparams:d12={}_d3={}_d4={}_d5={}_r={}_epo={:d}_class.h5".format(self.path, self.model_params['model_name'], d12, d3, d4,d5, r, epoch))

    def process_instance(self,instance, target, maxlen):
        w = self.pad(instance, maxlen)
        target.append(w)

    def process_matrix(self,inputs, trans1_length, maxlen):
        inputs_trans1 = np.split(inputs, trans1_length, axis=1)
        processed_inputs = []
        for item in inputs_trans1:
            item_trans2 = np.squeeze(item, axis=1).tolist()
            processed_inputs.append(item_trans2)
        return processed_inputs

    def get_data(self,path):
        data = self.load_pickle(path)#,self.data_params['train_path']

        #dev_data = self.load_pickle(self.data_params['valid_path'])
        #test_data = self.load_pickle(self.data_params['test_path'])

        text_S1 = []
        text_S2 = []
        code = []
        queries = []
        labels = []
        id = []



        text_block_length, text_word_length, query_word_length, code_token_length = 2, 100, 25, 350
        text_blocks = self.process_matrix(np.array([samples_term[1] for samples_term in data]),
                                          text_block_length, 100)

        text_S1 = text_blocks[0]
        text_S2 = text_blocks[1]

        code_blocks = self.process_matrix(np.array([samples_term[2] for samples_term in data]),
                                     text_block_length - 1, 350)
        code = code_blocks[0]

        queries = [samples_term[3] for samples_term in data]
        labels = [samples_term[5] for samples_term in data]
        ids = [samples_term[0] for samples_term in data]


        return text_S1, text_S2, code, queries, labels, ids
        #return text_S1, text_S2, code, queries, ids

    ##### Training #####
    def train(self, model):
        if self.train_params['reload'] > 0:
            self.load_model_epoch(model, self.train_params['reload'])

        d12,d3,d4,d5,r = self.train_params['dropout1'], self.train_params['dropout3'], self.train_params['dropout4'], self.train_params['dropout5'],self.train_params['regularizer']
        batch_size = self.train_params.get('batch_size', 100)  # 100
        nb_epoch = self.train_params.get('nb_epoch', 20)  # 2000

        val_loss = {'loss': 1., 'epoch': 0}
        previous_dev_f1 = float(0)
        previous_test_f1 = float(0)
        epoch_train_losses, epoch_train_precision, epoch_train_recall, \
        epoch_train_f1, epoch_train_accuracy = [], [], [], [], []
        epoch_dev_losses, epoch_dev_precision, epoch_dev_recall, \
        epoch_dev_f1, epoch_dev_accuracy = [], [], [], [], []
        epoch_test_losses, epoch_test_precision, epoch_test_recall, \
        epoch_test_f1, epoch_test_accuracy = [], [], [], [], []
        save_i = []
        save_i_test = []
        indicator = []
        indicator_1 = []
        indicator_2 = []
        final = 150
        #text_S1, text_S2, code, queries, labels, _ = self.get_data(self.data_params['train_path'])


        for i in range(self.train_params['reload'] + 1, nb_epoch):
            print('Epoch %d :: \n' % i, end='')
            logger.debug('loading data ..')
            text_S1, text_S2, code, queries, labels, _ = self.get_data(self.data_params['train_path'])
            hist = model.fit(
                [np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)], np.array(labels), shuffle=True, epochs=1, batch_size=batch_size)

            if hist.history['loss'][0] < val_loss['loss']:
                val_loss = {'loss': hist.history['loss'][0], 'epoch': i}

            print('Best: Loss = {}, Epoch = {}'.format(val_loss['loss'], val_loss['epoch']))
            # loss precison,recall,f1,accuracy

            train_acc, train_f1, train_recall, train_precison, train_loss = self.valid(model,
                                                                                       self.data_params['train_path'])
            epoch_train_losses.append(train_loss)
            epoch_train_accuracy.append(train_acc)
            epoch_train_recall.append(train_recall)
            epoch_train_precision.append(train_precison)
            epoch_train_f1.append(train_f1)
            print("train data: %d loss=%.3f, acc=%.3f,  precison=%.3f,  recall=%.3f,  f1=%.3f,  " % (
                i, train_loss, train_acc, train_precison, train_recall, train_f1))
            dev_acc, dev_f1, dev_recall, dev_precision, loss = self.valid(model, self.data_params['valid_path'])
            epoch_dev_losses.append(loss)
            epoch_dev_precision.append(dev_precision)
            epoch_dev_recall.append(dev_recall)
            epoch_dev_f1.append(dev_f1)
            epoch_dev_accuracy.append(dev_acc)
            print("dev data: %d loss=%.3f, acc=%.3f,  precison=%.3f,  recall=%.3f,  f1=%.3f,  " % (
                i, loss, dev_acc, dev_precision, dev_recall, dev_f1))
            test_acc, test_f1, test_recall, test_precision, loss = self.valid(model, self.data_params['test_path'])
            epoch_test_losses.append(loss)
            epoch_test_precision.append(test_precision)
            epoch_test_recall.append(test_recall)
            epoch_test_f1.append(test_f1)
            epoch_test_accuracy.append(test_acc)
            print("test data: %d loss=%.3f, acc=%.3f,  precison=%.3f,  recall=%.3f,  f1=%.3f,  " % (
                i, loss, test_acc, test_precision, test_recall, test_f1))
            indicator_one1 = [i, [test_acc, test_f1, test_recall, test_precision, loss]]
            indicator_one2 = [i, [dev_acc, dev_f1, dev_recall, dev_precision, loss]]
            indicator_1.append(indicator_one1)
            indicator_2.append(indicator_one2)
            if dev_f1 > previous_dev_f1:
                previous_dev_f1 = dev_f1
                save_i.append(i)
                self.save_model_epoch(model, i, d12, d3, d4, d5, r)
                print("更新最大f1: %.3f" % previous_dev_f1)
            else:
                print("dev set上最好的f1: %.3f.\nCurrent f1 on dev set: %.3f." % (previous_dev_f1, dev_f1))
            self.del_pre_model(save_i, d12, d3, d4, d5, r)
            # 直接保留测试集得指标
            if test_f1 > previous_test_f1:
                previous_test_f1 = test_f1
                save_i_test.append(i + 1000)
                self.save_model_epoch(model, i + 1000, d12, d3, d4, d5, r)
            self.del_pre_model(save_i_test, d12, d3, d4, d5, r)
         
        
        indicator.append(indicator_1)
        indicator.append(indicator_2)
        max_idx = np.argmax(epoch_dev_f1)
        max_idx_t = np.argmax(epoch_test_f1)
        print("最大dev f1由 %d-th epoch: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (
            max_idx, epoch_dev_precision[max_idx], epoch_dev_recall[max_idx], epoch_dev_f1[max_idx],
            epoch_dev_accuracy[max_idx]))
        print("相应的测试性能: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (
            epoch_test_precision[max_idx], epoch_test_recall[max_idx], epoch_test_f1[max_idx],
            epoch_test_accuracy[max_idx]))
        print("*" * 10)  # for formatting

        # ================================================记录:

        filename = 'adjust_python_15.txt'
        #filename = 'test_no_sa.txt'
        f = open(filename, 'a+')
        # params = "记录:dropout1=%.3f,dropout2=%.3f,dropout3=%.3f,re=%.3f" % (d1,d2,d3,r)
        params = "记录:dropout12=%.3f,dropout3=%.3f,dropout4=%.3f,dropout5=%.3f,num =%.5f" % (d12, d3, d4, d5, r)
        loss = "结束epoch=%d" % (final) + " " + 'loss:' + '自定义,'  # 交叉熵
        f.writelines(loss)
        f.writelines('\n')
        f.writelines(params)
        f.writelines('\n')
        f.writelines("最大dev f1由 %d-th epoch: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (
            max_idx, epoch_dev_precision[max_idx], epoch_dev_recall[max_idx], epoch_dev_f1[max_idx],
            epoch_dev_accuracy[max_idx]))
        f.writelines('\n')
        f.writelines("相应的测试性能: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (
            epoch_test_precision[max_idx], epoch_test_recall[max_idx], epoch_test_f1[max_idx],
            epoch_test_accuracy[max_idx]))
        f.writelines('\n')
        f.writelines("最大test f1由 %d-th epoch:f1: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % (max_idx_t, epoch_test_precision[ max_idx_t],epoch_test_recall[max_idx_t],epoch_test_f1[max_idx_t],epoch_test_accuracy[max_idx_t]))

        #f.writelines("验证集-测试集：: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % ((epoch_test_precision[max_idx] - 0.872), (epoch_test_recall[max_idx] - 0.903),(epoch_test_f1[max_idx] - 0.888),(epoch_test_accuracy[max_idx] - 0.867)))
        #f.writelines('\n')
        #f.writelines("测试集-测试集：: precision=%.3f, recall=%.3f, f1=%.3f, accuracy=%.3f" % ((epoch_test_precision[max_idx_t]-0.872), (epoch_test_recall[max_idx_t]-0.903), (epoch_test_f1[max_idx_t]-0.888),(epoch_test_accuracy[max_idx_t]-0.867)))
        f.writelines('\n')
        f.writelines("*" * 10)
        f.writelines('\n')
        f.writelines("                                             ")
        f.writelines('\n')
        f.close()

        indicator_txt = 'final_test.txt'
        #indicator_txt = 'test_in_no_Sa.txt'
        f = open(indicator_txt, 'a+')
        f.writelines("\nre\n")
        f.write(str(indicator))
        f.close()
        sys.stdout.flush()


    def valid(self, model,path):
        """
        quick validation in a code pool.
        param:
            poolsize - size of the code pool, if -1, load the whole test set
        """

        text_S1,text_S2,code,queries,labels,_ = self.get_data(path)

        labelpred = model.predict([np.array(text_S1), np.array(text_S2), np.array(code), np.array(queries)], batch_size=100)
        labelpred = np.argmax(labelpred, axis=1)
        loss = log_loss(labels,labelpred)
        acc = accuracy_score(labels, labelpred)
        f1 = f1_score(labels, labelpred)
        recall = recall_score(labels,labelpred)
        precision = precision_score(labels,labelpred)
        return acc, f1,recall,precision,loss

        ##### Evaluation in the develop set #####

    def eval(self, model, path):
        """
        evaluate in a evaluation date.
        param:
            poolsize - size of the code pool, if -1, load the whole test set
        """

        text_S1, text_S2, code, queries, labels, ids = self.get_data(path)

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


#https://wenku.baidu.com/view/5101dd03cfbff121dd36a32d7375a417866fc19f.html
'''
name or flags - 选项字符串的名字或者列表，例如 foo 或者 -f, --foo
choices:参数可允许的值的⼀个容器
default - 不指定参数时的默认值。
help - 参数的帮助信息，当指定为 argparse.SUPPRESS 时表⽰不显⽰该参数的帮助信息.
action - 命令⾏遇到参数时的动作，默认值是 store
'''
def parse_args():
    parser = argparse.ArgumentParser("Train and Test Model") # 创建对象
    parser.add_argument("--train",choices=["python","sql"],default="python",help="train dataset set")
    parser.add_argument("--mode", choices=["train","eval"], default="train",
                        help="The mode to run. The `train` mode trains a model;"
                        " the `eval` mode evaluat models in a test set ") #添加参数
    parser.add_argument("--verbose",action="store_true", default=True, help="Be verbose")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    conf = get_config(args.train)
    train_path = conf['data_params']['train_path']
    dev_path = conf['data_params']['valid_path']
    test_path = conf['data_params']['test_path']


    ##### Define model ######
    logger.info('Build Model')
    # 这里是不是相当于创建了CARLCS_CNN类，并用conf里面的参数去初始化它
    model = eval(conf['model_params']['model_name'])(
        conf)  # initialize the model,  model== <models.CARLCS_CNN object at 0x7f1d9c2e2cc0>

    StandoneCode = StandoneCode(conf)
    drop1 = drop2 = drop3 = drop4 = drop5 = 0.8

    r = 0.0002

    conf['training_params']['regularizer'] = 8
    model.params_adjust(dropout1=drop1, dropout2=drop2, dropout3=drop3, dropout4=drop4,
                        dropout5=drop5,
                        Regularizer=round(r, 5), num=8,
                        seed=42)
    conf['training_params']['dropout1'] = drop1
    conf['training_params']['dropout2'] = drop2
    conf['training_params']['dropout3'] = drop3
    conf['training_params']['dropout4'] = drop4
    conf['training_params']['dropout5'] = drop5
    conf['training_params']['regularizer'] = round(r, 5) + 1
    model.build()

    if args.mode == 'train':
        StandoneCode.train(model)
    elif args.mode == 'eval':

        # 加载模型python
        #StandoneCode.load_model_epoch(model, 121, 0.5, 0.5, 0.5, 0.5, 0.0006)
        ## 加载模型sql
        StandoneCode.load_model_epoch(model, 83, 0.25, 0.25, 0.25, 0.25, 0.0006)
        # 测试集评估
        StandoneCode.eval(model, test_path)
    #for d in np.arange(0.49,0.51,0.01):





