__doc__ = """biv-hnn模型"""

import logging
import random

import numpy as np
import tensorflow as tf
from keras import Model
from keras.layers import Embedding, Input, Dense, Dropout, Lambda, Bidirectional, GRU
from keras.optimizers import Adam

from MediumLayer import MediumLayer
from models import CodeMF as BaseCodeMF

RANDOM_SEED = 1
tf.compat.v1.set_random_seed(RANDOM_SEED)  # 图级种子，使所有操作会话生成的随机序列在会话中可重复，请设置图级种子：
random.seed(RANDOM_SEED)  # 让每次生成的随机数一致
np.random.seed(RANDOM_SEED)
logger = logging.getLogger(__name__)


class CodeMF(BaseCodeMF):
    def __init__(self, config):
        super(CodeMF, self).__init__(config)

    def build(self):
        # 1. Build Code Representation Model
        logger.debug('Building Code Representation Model')
        text_S1 = Input(shape=(self.text_length,), dtype='int32', name='S1name')
        text_S2 = Input(shape=(self.text_length,), dtype='int32', name='S2name')
        code = Input(shape=(self.code_length,), dtype='int32', name='codename')
        queries = Input(shape=(self.queries_length,), dtype='int32', name='queryname')

        # 2.Embedding
        embedding_layer = Embedding(self.text_embbeding.shape[0], self.text_embbeding.shape[1],
                                    weights=[self.text_embbeding], input_length=self.text_length,
                                    trainable=False, mask_zero=True)

        text_S1_embeding = embedding_layer(text_S1)
        text_S2_embeding = embedding_layer(text_S2)
        emnedding_layer = Embedding(self.text_embbeding.shape[0], self.text_embbeding.shape[1],
                                    weights=[self.text_embbeding], input_length=self.queries_length,
                                    trainable=False, mask_zero=True)

        queries_embeding = emnedding_layer(queries)

        embedding_layer = Embedding(self.code_embbeding.shape[0], self.code_embbeding.shape[1],
                                    weights=[self.code_embbeding], input_length=self.code_length,
                                    trainable=False, mask_zero=True)
        code_embeding = embedding_layer(code)
        dropout = Dropout(self.dropout1, name='dropout_embed', seed=1)
        text_S1_embeding = dropout(text_S1_embeding)
        text_S2_embeding = dropout(text_S2_embeding)
        code_embeding = dropout(code_embeding)
        queries_embeding = dropout(queries_embeding)

        # 3. 双向gru
        layer = Bidirectional(GRU(units=64))
        t1 = layer(text_S1_embeding)
        t2 = layer(text_S2_embeding)
        c = layer(code_embeding)
        q = layer(queries_embeding)

        # query and code
        layer2 = Lambda(lambda x: tf.concat([x[0], x[1]], axis=1))
        code_q = layer2([c, q])
        code_q = dropout(code_q)
        layer2 = Dense(128, activation='tanh')
        file_c = layer2(code_q)
        sentence = MediumLayer()([t1, t2, file_c])
        sentence = dropout(sentence)

        layer5 = Bidirectional(GRU(units=128, return_sequences=True))

        f1 = layer5(sentence)
        f1 = Lambda(lambda x: backend.permute_dimensions(x, (1, 0, 2)))(f1)

        f1 = Lambda(lambda x: tf.unstack(x, axis=0))(f1)
        f1 = Lambda(lambda x: x[1])(f1)
        f1 = dropout(f1)
        # sentence = SeqSelfAttention(1, 3)(sentence)
        # sentence = dropout(sentence)

        classf = Dense(2, activation='softmax', name="final_class")(f1)

        class_model = Model(inputs=[text_S1, text_S2, code, queries], outputs=[classf], name='class_model')
        self.class_model = class_model

        print("\nsummary of class model")
        self.class_model.summary()
        fname = self.config['workdir'] + 'models/' + self.model_params['model_name'] + '/_class_model.png'

        # 7.train model
        # pred = class_model([self.text_S1,self.text_S2,self.code,self.queries])
        # loss = Lambda(lambda x:backend.minimum(1e-6,backend.categorical_crossentropy(self.labels,x)+0.2),output_shape= lambda x:(1,),name='newloss')(pred)
        # self.train_model = Model(inputs=[self.text_S1,self.text_S2,self.code,self.queries,self.labels],outputs=[loss],name='train_model')
        # self.train_model.summary()

        optimizer = Adam(learning_rate=0.001, clipnorm=0.001)
        self.class_model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def dice_coed_test(self, y_true, y_pred, P):
        e = 0.1
        loss1 = backend.categorical_crossentropy(y_true, y_pred)
        loss2 = backend.categorical_crossentropy(backend.ones_like(y_pred) / self.nb_classes, y_pred)

        total_loss = (1 - e) * loss1 + e * loss2
        print(total_loss)
        print(P)
        total_loss = total_loss
        return total_loss

    def dice_loss_test(self, P):
        def dice_test(y_true, y_pred):
            return self.dice_coed_test(y_true, y_pred, P)

        return dice_test
