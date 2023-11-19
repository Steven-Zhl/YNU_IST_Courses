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


class SelfAttention(Layer):
    def __init__(self, r, da, name, **kwargs):
        self.Ws2 = None
        self.Ws1 = None
        self.r = r
        self.da = da
        self.scope = name
        super(SelfAttention, self).__init__(**kwargs)

    def build(self, input_shape):
        # (120,150)
        self.Ws1 = self.add_weight(name='Ws1' + self.scope,
                                   shape=(input_shape[2], self.da),
                                   initializer='glorot_uniform',
                                   trainable=True)
        # (3,120)
        self.Ws2 = self.add_weight(name='Ws2' + self.scope,
                                   shape=(self.da, self.r),
                                   initializer='glorot_uniform',
                                   trainable=True)

    def call(self, inputs, **kwargs):
        # inputs:(100,4,150)
        # (?,4,120)
        A1 = backend.dot(inputs, self.Ws1)
        # (120, 4, ?)
        A1 = tf.tanh(tf.transpose(A1))
        # (?,4,120)  da*n
        A1 = tf.transpose(A1)
        # (?, 4, 3)
        A_T = backend.softmax(backend.dot(A1, self.Ws2))
        # (?,3,4)
        A = backend.permute_dimensions(A_T, (0, 2, 1))
        # (100, 3, 150)
        B = tf.matmul(A, inputs)
        tile_eye = tf.tile(tf.eye(self.r), [tf.shape(inputs)[0], 1])
        tile_eye = tf.reshape(tile_eye, [-1, self.r, self.r])
        # (100, 3, 3)
        AA_T = tf.matmul(A, A_T) - tile_eye
        # (100,)
        P = tf.square(tf.norm(AA_T, axis=[-2, -1], ord='fro'))

        return [B, P]

    def compute_output_shape(self, input_shape):
        return [(input_shape[0], self.da, self.r), (input_shape[0],)]
