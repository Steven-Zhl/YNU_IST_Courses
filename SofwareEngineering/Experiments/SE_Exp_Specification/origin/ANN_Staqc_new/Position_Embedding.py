#! -*- coding: utf-8 -*-
# %%
from __future__ import print_function
from tensorflow.keras import backend as K
from tensorflow.keras.layers import *
import tensorflow as tf
import os
import numpy as np
import random
import tensorflow as tf
seed = 42
np.random.seed(seed)
tf.random.set_seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
random.seed(seed)

class Position_Embedding(Layer):
    def __init__(self, size=None, mode='sum', **kwargs):
        self.size = size  # 必须为偶数
        self.mode = mode
        super(Position_Embedding, self).__init__(**kwargs)

    def call(self, x):  # 上一层一般就是embedding层，batch_size,seq_len,model_dim
        if (self.size == None) or (self.mode == 'sum'):
            self.size = int(x.shape[-1])  # d_model的长度,比如512
        batch_size, seq_len = K.shape(x)[0], K.shape(x)[1]  #
        ## K.arange(self.size / 2, dtype='float32' ), 生成0~256，间隔1,即公式中的i
        ## 2*K.arange(self.size / 2, dtype='float32' ), 0~512，间隔2,即公式中的2i, 0,2,4,6……,512，对应的i是0,1,2,3,4,5
        ## 再除以model_dim，按公式取pow
        position_j = 1. / K.pow(10000., 2 * K.arange(self.size / 2, dtype='float32') / self.size)  #
        position_j = K.expand_dims(position_j, 0)  # (1,256)
        # 生成位置的序列
        # x[:,:,0]取每个embedding的第一个分量---> bs,seq_len
        # ones_like -->bs,seq_len [[1，1，1，1……],[1,1,1……],……]
        # cumsum ---> bs,seq_len,[[1,2,3,4……],[1,2,3……],……]
        # cumsum-1 ----->bs,seq_len,[[0,1,2,3……],[0,1,2……],……]
        position_i = K.cumsum(K.ones_like(x[:, :, 0]), 1) - 1  # K.arange不支持变长，只好用这种方法生成
        position_i = K.expand_dims(position_i, 2)  # bs,seq_len,1
        position_ij = K.dot(position_i, position_j)  # bs,seq_len,256
        ##经过dot之后,就是pe/10000^(2i/d_model)了
        ##原始的实现稍微有点问题，不应该直接concatenate偶数和奇数，应该交叉concatenate
        position_ij_2i = K.sin(position_ij)[..., tf.newaxis]  # bs,seq_len,model_dim/2,1
        position_ij_2i_1 = K.cos(position_ij)[..., tf.newaxis]  # bs,seq_len,model_dim/2,1
        position_ij = K.concatenate([position_ij_2i, position_ij_2i_1])  # bs,seq_len,model_dim/2,2
        position_ij = K.reshape(position_ij, (batch_size, seq_len, self.size))  # bs,seq_len,model_dim
        # position_ij = K.concatenate([K.cos(position_ij), K.sin(position_ij)], 2)#这个实现没有交叉拼接，前半部分都用的cos，后半部分都用的sin
        if self.mode == 'sum':
            return position_ij + x
        elif self.mode == 'concat':
            return K.concatenate([position_ij, x], 2)

    def compute_output_shape(self, input_shape):
        if self.mode == 'sum':
            return input_shape
        elif self.mode == 'concat':
            return (input_shape[0], input_shape[1], input_shape[2] + self.size)


'''
query = tf.random.truncated_normal([100, 50, 150])
w = Position_Embedding(150,'concat')(query)
print(w.shape)
'''