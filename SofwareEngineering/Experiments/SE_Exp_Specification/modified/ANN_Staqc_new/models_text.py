from logging import getLogger

import tensorflow as tf
from keras import regularizers, Input, Model
from keras.layers import Lambda, Embedding, Dropout, Dense, GlobalAveragePooling1D
from keras.optimizers import Adam

from LayerNormalization import LayerNormalization
from MediumLayer import MediumLayer
from MultiHeadAttention import MultiHeadAttention
from PositionEmbedding import PositionEmbedding
from PositionWiseFeedForward import PositionWiseFeedForward
from models import CodeMF as BaseCodeMF

tf.compat.v1.disable_eager_execution()
from keras.layers.rnn import GRU, Bidirectional
import os
import numpy as np
import random
import tensorflow as tf

from configs import RANDOM_SEED

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
logger = getLogger(__name__)

'''
变体：模型输入只要文本上下文
'''


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

        print("===============", text_S1.shape)

        # 2.Embedding
        embedding_layer = Embedding(self.text_embbeding.shape[0], self.text_embbeding.shape[1],
                                    weights=[self.text_embbeding], input_length=self.text_length,
                                    trainable=False, mask_zero=True)

        text_S1_embeding = embedding_layer(text_S1)
        text_S2_embeding = embedding_layer(text_S2)

        # 3.postion_embeddding
        positionembeing = PositionEmbedding(10, 'concat')
        text_S1_embeding_p = positionembeing(text_S1_embeding)
        text_S2_embeding_p = positionembeing(text_S2_embeding)

        # 4.dropout
        dropout = Dropout(self.dropout1, name='dropout_embed', seed=self.random_seed)
        text_S1_embeding_d = dropout(text_S1_embeding_p)
        text_S2_embeding_d = dropout(text_S2_embeding_p)

        # 5. transformer
        layer = MultiHeadAttention(10)
        t1 = layer([text_S1_embeding_d, text_S1_embeding_d, text_S1_embeding_d])
        t2 = layer([text_S2_embeding_d, text_S2_embeding_d, text_S2_embeding_d])

        add_out = Lambda(lambda x: x[0] + x[1])
        t1 = add_out([t1, text_S1_embeding_d])
        t2 = add_out([t2, text_S2_embeding_d])

        t1_l = LayerNormalization()(t1)
        t2_l = LayerNormalization()(t2)

        ff = PositionWiseFeedForward(310, 2048)
        ff_t1 = ff(t1_l)
        ff_t2 = ff(t2_l)

        dropout_ = Dropout(self.dropout2, name='dropout_ffn', seed=self.random_seed)
        ff_t1 = dropout_(ff_t1)
        ff_t2 = dropout_(ff_t2)

        ff_t1 = add_out([ff_t1, t1_l])
        ff_t2 = add_out([ff_t2, t2_l])

        t1 = LayerNormalization()(ff_t1)
        t2 = LayerNormalization()(ff_t2)

        # 5.1 融合代码，上下文语义
        dropout = Dropout(self.dropout3, name='dropout_qc', seed=self.random_seed)
        # t1 = dropout(t1)
        # t2 = dropout(t2)
        leakyrulu = Lambda(lambda x: tf.nn.leaky_relu(x))
        text_S1_Semantic = GlobalAveragePooling1D(name='globaltext_1')(t1)
        text_S1_Semantic = leakyrulu(text_S1_Semantic)  # -----------
        text_S2_Semantic = GlobalAveragePooling1D(name='globaltext_2')(t2)
        text_S2_Semantic = leakyrulu(text_S2_Semantic)  # -------------

        # 融合语义
        sentence_token_level_outputs = MediumLayer()(
            [text_S1_Semantic, text_S2_Semantic])
        layer5 = Bidirectional(GRU(units=128, dropout=self.dropout4))
        f1 = layer5(sentence_token_level_outputs)
        dropout = Dropout(self.dropout5, name='dropout2', seed=self.random_seed)
        f1 = dropout(f1)

        # f1 = LayerNormalization()(f1)
        # f1 = PositionWiseFeedForward(256, 2048)(f1)

        # 7 分类
        classf = Dense(2, activation='softmax', name="final_class",
                       kernel_regularizer=regularizers.l2(self.Regularizer))(f1)

        class_model = Model(inputs=[text_S1, text_S2, code, queries], outputs=[classf], name='class_model')
        self.class_model = class_model

        print("\nsummary of class model")
        self.class_model.summary()
        fname = self.config['workdir'] + 'models/' + self.model_params['model_name'] + '/_class_model.png'
        P1, P2, Pc, Pq = None, None, None, None
        myloss = self.dice_loss(P1, P2, Pc, Pq)
        optimizer = Adam(learning_rate=0.001, clipnorm=0.001)
        self.class_model.compile(loss=myloss, optimizer=optimizer)
