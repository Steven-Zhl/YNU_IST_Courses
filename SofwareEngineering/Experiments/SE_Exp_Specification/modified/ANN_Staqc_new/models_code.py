__doc__ = """变体：模型输入只要代码和查询描述"""

import os
import random
from logging import getLogger

import numpy as np
import tensorflow as tf
from keras import backend, regularizers, Input, Model
from keras.layers import Lambda, Dot, Embedding, Dropout, Dense, Activation, GlobalAveragePooling1D, GRU, Bidirectional
from keras.optimizers import Adam

from AttentionLayer import AttentionLayer
from LayerNormalization import LayerNormalization
from MediumLayer import MediumLayer
from MultiHeadAttention import MultiHeadAttention
from PositionEmbedding import PositionEmbedding
from PositionWiseFeedForward import PositionWiseFeedForward
from configs import RANDOM_SEED
from models import CodeMF as BaseCodeMF

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
logger = getLogger(__name__)
tf.compat.v1.disable_eager_execution()


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
        emnedding_layer = Embedding(self.text_embbeding.shape[0], self.text_embbeding.shape[1],
                                    weights=[self.text_embbeding], input_length=self.queries_length,
                                    trainable=False, mask_zero=True)
        queries_embeding = emnedding_layer(queries)
        embedding_layer = Embedding(self.code_embbeding.shape[0], self.code_embbeding.shape[1],
                                    weights=[self.code_embbeding], input_length=self.code_length,
                                    trainable=False, mask_zero=True)
        code_embeding = embedding_layer(code)

        # 3.postion_embeddding
        positionembeing = PositionEmbedding(10, 'concat')
        code_embeding_p = positionembeing(code_embeding)
        queries_embeding_p = positionembeing(queries_embeding)

        # 4.dropout
        dropout = Dropout(self.dropout1, name='dropout_embed', seed=self.random_seed)
        code_embeding_d = dropout(code_embeding_p)
        queries_embeding_d = dropout(queries_embeding_p)

        # 5. transformer
        layer = MultiHeadAttention(10)

        c = layer([code_embeding_d, code_embeding_d, code_embeding_d])
        q = layer([queries_embeding_d, queries_embeding_d, queries_embeding_d])

        add_out = Lambda(lambda x: x[0] + x[1])

        c = add_out([c, code_embeding_d])
        q = add_out([q, queries_embeding_d])

        c_l = LayerNormalization()(c)
        q_l = LayerNormalization()(q)

        ff = PositionWiseFeedForward(310, 2048)

        ff_c = ff(c_l)
        ff_q = ff(q_l)

        dropout_ = Dropout(self.dropout2, name='dropout_ffn', seed=self.random_seed)

        ff_c = dropout_(ff_c)
        ff_q = dropout_(ff_q)

        ff_c = add_out([ff_c, c_l])
        ff_q = add_out([ff_q, q_l])

        c = LayerNormalization()(ff_c)
        q = LayerNormalization()(ff_q)

        # 5.1 融合代码，上下文语义
        dropout = Dropout(self.dropout3, name='dropout_qc', seed=self.random_seed)
        leakyrulu = Lambda(lambda x: tf.nn.leaky_relu(x))

        # 5.2 代码和文本交互注意力
        c = dropout(c)
        q = dropout(q)
        attention = AttentionLayer(name='attention_layer')
        attention_out = attention([c, q])
        gmp_1 = GlobalAveragePooling1D(name='blobalmaxpool_colum')
        att_1 = gmp_1(attention_out)
        activ1 = Activation('softmax', name='AP_active_colum')
        att_1_next = activ1(att_1)
        dot1 = Dot(axes=1, normalize=False, name='column_dot')
        print("````````````````````````````", att_1_next)
        queries_semantic = dot1([att_1_next, q])
        queries_semantic = leakyrulu(queries_semantic)  # -----------

        attention_trans_layer = Lambda(lambda x: backend.permute_dimensions(x, (0, 2, 1)), name='trans_attention')
        attention_transposed = attention_trans_layer(attention_out)
        gmp_2 = GlobalAveragePooling1D(name='blobalmaxpool_row')
        att_2 = gmp_2(attention_transposed)
        activ2 = Activation('softmax', name='AP_active_row')
        att_2_next = activ2(att_2)
        dot2 = Dot(axes=1, normalize=False, name='row_dot')
        code_semantic = dot2([att_2_next, c])
        code_semantic = leakyrulu(code_semantic)  # ----------

        # 融合语义
        sentence_token_level_outputs = MediumLayer()(
            [queries_semantic, code_semantic])
        layer5 = Bidirectional(GRU(units=128, dropout=self.dropout4))
        f1 = layer5(sentence_token_level_outputs)
        dropout = Dropout(self.dropout5, name='dropout2', seed=self.random_seed)
        f1 = dropout(f1)

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
