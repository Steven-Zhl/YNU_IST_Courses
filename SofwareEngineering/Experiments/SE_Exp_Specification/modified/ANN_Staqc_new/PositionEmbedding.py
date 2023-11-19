import os
import random

import numpy as np
import tensorflow as tf
from keras import backend
from keras.layers import Layer

from configs import RANDOM_SEED

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)


class PositionEmbedding(Layer):
    def __init__(self, size=None, mode='sum', **kwargs):
        self.size = size  # 必须为偶数
        self.mode = mode
        super(PositionEmbedding, self).__init__(**kwargs)

    def call(self, x, **kwargs):
        if (self.size is None) or (self.mode == 'sum'):
            self.size = int(x.shape[-1])  # d_model的长度,比如512
        batch_size, seq_len = backend.shape(x)[0], backend.shape(x)[1]  #
        # backend.arange(self.size / 2, dtype='float32' ), 生成0~256，间隔1,即公式中的i
        # 2*backend.arange(self.size / 2, dtype='float32' ), 0~512，间隔2,即公式中的2i, 0,2,4,6……,512，对应的i是0,1,2,3,4,5
        # 再除以model_dim，按公式取pow
        position_j = 1. / backend.pow(10000., 2 * backend.arange(self.size / 2, dtype='float32') / self.size)  #
        position_j = backend.expand_dims(position_j, 0)  # (1,256)
        # 生成位置的序列
        # x[:,:,0]取每个embedding的第一个分量---> bs,seq_len
        # ones_like -->bs,seq_len [[1，1，1，1……],[1,1,1……],……]
        # cumsum ---> bs,seq_len,[[1,2,3,4……],[1,2,3……],……]
        # cumsum-1 ----->bs,seq_len,[[0,1,2,3……],[0,1,2……],……]
        position_i = backend.cumsum(backend.ones_like(x[:, :, 0]), 1) - 1  # backend.arange不支持变长，只好用这种方法生成
        position_i = backend.expand_dims(position_i, 2)  # bs,seq_len,1
        position_ij = backend.dot(position_i, position_j)  # bs,seq_len,256
        # 经过dot之后,就是pe/10000^(2i/d_model)了
        # 原始的实现稍微有点问题，不应该直接concatenate偶数和奇数，应该交叉concatenate
        position_ij_2i = backend.sin(position_ij)[..., tf.newaxis]  # bs,seq_len,model_dim/2,1
        position_ij_2i_1 = backend.cos(position_ij)[..., tf.newaxis]  # bs,seq_len,model_dim/2,1
        position_ij = backend.concatenate([position_ij_2i, position_ij_2i_1])  # bs,seq_len,model_dim/2,2
        position_ij = backend.reshape(position_ij, (batch_size, seq_len, self.size))  # bs,seq_len,model_dim
        # position_ij = backend.concatenate([backend.cos(position_ij), backend.sin(position_ij)], 2)
        # 这个实现没有交叉拼接，前半部分都用的cos，后半部分都用的sin
        if self.mode == 'sum':
            return position_ij + x
        elif self.mode == 'concat':
            return backend.concatenate([position_ij, x], 2)

    def compute_output_shape(self, input_shape):
        if self.mode == 'sum':
            return input_shape
        elif self.mode == 'concat':
            return input_shape[0], input_shape[1], input_shape[2] + self.size
