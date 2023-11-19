import os
import pickle
import random
from logging import getLogger

import numpy as np
import tensorflow as tf
from keras import backend, regularizers, Input, Model
from keras.layers import Lambda, GRU, Bidirectional, Embedding, Dropout, Dense, Activation, GlobalAveragePooling1D
from keras.optimizers import Adam
from keras.utils import to_categorical

from AttentionLayer import AttentionLayer
from LayerNormalization import LayerNormalization
from MediumLayer import MediumLayer
from MultiHeadAttention import MultiHeadAttention
from PositionEmbedding import PositionEmbedding
from PositionWiseFeedForward import PositionWiseFeedForward
from configs import CODE_LENGTH, TEXT_LENGTH, QUERIES_LENGTH, RANDOM_SEED

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

logger = getLogger(__name__)
tf.compat.v1.disable_eager_execution()


class CodeMF:
    def __init__(self, config):
        self.config = config
        self.text_length = TEXT_LENGTH
        self.queries_length = QUERIES_LENGTH
        self.code_length = CODE_LENGTH
        self.class_model = None
        self.train_model = None
        self.text_S1 = Input(shape=(self.text_length,), dtype='int32', name='i_S1name')
        self.text_S2 = Input(shape=(self.text_length,), dtype='int32', name='i_S2name')
        self.code = Input(shape=(self.code_length,), dtype='int32', name='i_codename')
        self.queries = Input(shape=(self.queries_length,), dtype='int32', name='i_queryname')
        self.labels = Input(shape=(1,), dtype='int32', name='i_queryname')
        self.nb_classes = 2

        self.model_params = config.get('model_params', dict())
        self.data_params = config.get('data_params', dict())
        self.text_embbeding = pickle.load(open(self.data_params['text_pretrain_emb_path'], "rb"), encoding='iso-8859-1')
        self.code_embbeding = pickle.load(open(self.data_params['code_pretrain_emb_path'], "rb"), encoding='iso-8859-1')
        # create a model path to store model info
        if not os.path.exists(self.config['workdir'] + 'models/' + self.model_params['model_name'] + '/'):
            os.makedirs(self.config['workdir'] + 'models/' + self.model_params['model_name'] + '/')
        self.dropout1 = None
        self.dropout2 = None
        self.dropout3 = None
        self.dropout4 = None
        self.dropout5 = None
        self.Regularizer = None
        self.random_seed = None
        self.num = None

    # 设置超参数
    def params_adjust(self, dropout1=0.5, dropout2=0.5, dropout3=0.5, dropout4=0.5, dropout5=0.5, Regularizer=0.01,
                      num=100,
                      seed=42):
        self.dropout1 = dropout1
        self.dropout2 = dropout2
        self.dropout3 = dropout3
        self.dropout4 = dropout4
        self.dropout5 = dropout5
        self.Regularizer = Regularizer
        self.random_seed = seed

        self.num = num

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
        text_S1_embeding_p = positionembeing(text_S1_embeding)
        text_S2_embeding_p = positionembeing(text_S2_embeding)
        code_embeding_p = positionembeing(code_embeding)
        queries_embeding_p = positionembeing(queries_embeding)

        # 4.dropout
        dropout = Dropout(self.dropout1, name='dropout_embed', seed=self.random_seed)
        text_S1_embeding_d = dropout(text_S1_embeding_p)
        text_S2_embeding_d = dropout(text_S2_embeding_p)
        code_embeding_d = dropout(code_embeding_p)
        queries_embeding_d = dropout(queries_embeding_p)

        # 5. transformer
        layer = MultiHeadAttention(10)
        t1 = layer([text_S1_embeding_d, text_S1_embeding_d, text_S1_embeding_d])
        t2 = layer([text_S2_embeding_d, text_S2_embeding_d, text_S2_embeding_d])
        c = layer([code_embeding_d, code_embeding_d, code_embeding_d])
        q = layer([queries_embeding_d, queries_embeding_d, queries_embeding_d])

        add_out = Lambda(lambda x: x[0] + x[1])
        t1 = add_out([t1, text_S1_embeding_d])
        t2 = add_out([t2, text_S2_embeding_d])
        c = add_out([c, code_embeding_d])
        q = add_out([q, queries_embeding_d])

        t1_l = LayerNormalization()(t1)
        t2_l = LayerNormalization()(t2)
        c_l = LayerNormalization()(c)
        q_l = LayerNormalization()(q)

        ff = PositionWiseFeedForward(310, 2048)
        ff_t1 = ff(t1_l)
        ff_t2 = ff(t2_l)
        ff_c = ff(c_l)
        ff_q = ff(q_l)

        dropout_ = Dropout(self.dropout2, name='dropout_ffn', seed=self.random_seed)
        ff_t1 = dropout_(ff_t1)
        ff_t2 = dropout_(ff_t2)
        ff_c = dropout_(ff_c)
        ff_q = dropout_(ff_q)

        ff_t1 = add_out([ff_t1, t1_l])
        ff_t2 = add_out([ff_t2, t2_l])
        ff_c = add_out([ff_c, c_l])
        ff_q = add_out([ff_q, q_l])

        t1 = LayerNormalization()(ff_t1)
        t2 = LayerNormalization()(ff_t2)
        c = LayerNormalization()(ff_c)
        q = LayerNormalization()(ff_q)

        # 5.1 融合代码，上下文语义
        dropout = Dropout(self.dropout3, name='dropout_qc', seed=self.random_seed)
        # t1 = dropout(t1)
        # t2 = dropout(t2)
        leakyrulu = Lambda(lambda x: tf.nn.leaky_relu(x))
        text_S1_Semantic = GlobalAveragePooling1D(name='globaltext_1')(t1)
        text_S1_Semantic = leakyrulu(text_S1_Semantic)  # -----------
        text_S2_Semantic = GlobalAveragePooling1D(name='globaltext_2')(t2)
        text_S2_Semantic = leakyrulu(text_S2_Semantic)  # -------------

        # 5.2 代码和文本交互注意力
        c = dropout(c)
        q = dropout(q)
        attention = AttentionLayer(name='attention_layer')
        attention_out = attention([c, q])
        gmp_1 = GlobalAveragePooling1D(name='blobalmaxpool_colum')
        att_1 = gmp_1(attention_out)
        activ1 = Activation('softmax', name='AP_active_colum')
        att_1_next = activ1(att_1)
        dot1 = Lambda(axes=1, normalize=False, name='column_dot')
        print("````````````````````````````", att_1_next)
        queries_semantic = dot1([att_1_next, q])
        queries_semantic = leakyrulu(queries_semantic)  # -----------

        attention_trans_layer = Lambda(lambda x: backend.permute_dimensions(x, (0, 2, 1)),
                                       name='trans_attention')
        attention_transposed = attention_trans_layer(attention_out)
        gmp_2 = GlobalAveragePooling1D(name='blobalmaxpool_row')
        att_2 = gmp_2(attention_transposed)
        activ2 = Activation('softmax', name='AP_active_row')
        att_2_next = activ2(att_2)
        dot2 = Lambda(axes=1, normalize=False, name='row_dot')
        code_semantic = dot2([att_2_next, c])
        code_semantic = leakyrulu(code_semantic)  # ----------

        # 融合语义
        sentence_token_level_outputs = MediumLayer()(
            [text_S1_Semantic, text_S2_Semantic, queries_semantic, code_semantic])
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

    def compile(self, optimizer, **kwargs):
        logger.info('compiling models')
        '''
        model_dice = self.dice_loss(smooth=1e-5, thresh=0.5)
        model.compile(loss=model_dice)
        '''
        self.class_model.compile(loss=self.example_loss, optimizer=optimizer, **kwargs)

    def fit(self, x, y, **kwargs):
        assert self.class_model is not None, 'Must compile the model before fitting data'
        return self.class_model.fit(x, to_categorical(y), **kwargs)

    def predict(self, x, **kwargs):
        return self.class_model.predict(x, **kwargs)

    def save(self, class_model_file, **kwargs):
        assert self.class_model is not None, 'Must compile the model before saving weights'
        self.class_model.save_weights(class_model_file, **kwargs)

    def load(self, class_model_file, **kwargs):
        assert self.class_model is not None, 'Must compile the model loading weights'
        self.class_model.load_weights(class_model_file, **kwargs)

    def concat(self, inputs):
        block_level_code_output = tf.split(inputs, inputs.shape[1], axis=1)
        block_level_code_output = tf.concat(block_level_code_output, axis=2)
        # (bs,600)
        block_level_code_output = tf.squeeze(block_level_code_output, axis=1)
        return block_level_code_output

    def mycrossentropy(self, y_true, y_pred, e=0.1):
        loss1 = backend.categorical_crossentropy(y_true, y_pred)
        loss2 = backend.categorical_crossentropy(backend.ones_like(y_pred) / self.nb_classes, y_pred)
        return (1 - e) * loss1 + e * loss2

    def example_loss(self, y_true, y_pred):
        crossent = tf.compat.v1.nn.softmax_cross_entropy_with_logits(logits=y_pred, labels=y_true)
        # crossent = backend.categorical_crossentropy(y_true, y_pred)
        loss = tf.reduce_sum(crossent) / tf.cast(TEXT_LENGTH, tf.float32)
        print("========", loss.shape)
        return loss

    def dice_coef(self, y_true, y_pred, p1, p2, p3, p4, e=0.1):
        # P_loss = (p1 + p2 + p3 + p4) / 4

        loss1 = backend.categorical_crossentropy(y_true, y_pred)
        loss2 = backend.categorical_crossentropy(backend.ones_like(y_pred) / self.nb_classes, y_pred)
        return (1 - e) * loss1 + e * loss2  # + 0.001 * P_loss

    def dice_loss(self, p1, p2, p3, p4):
        def dice(y_true, y_pred):
            return self.dice_coef(y_true, y_pred, p1, p2, p3, p4)

        return dice
