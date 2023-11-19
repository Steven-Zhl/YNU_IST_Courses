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


class AttentionLayer(Layer):

    def __init__(self, **kwargs):
        self.kernel = None
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        if not isinstance(input_shape, list) or len(input_shape) != 2:
            raise ValueError('An attention layer should be called '
                             'on a list of 2 inputs.')
        if not input_shape[0][2] == input_shape[1][2]:
            raise ValueError('Embedding sizes should be of the same size')

        self.kernel = self.add_weight(shape=(input_shape[0][2], input_shape[0][2]),
                                      initializer='glorot_uniform',
                                      name='kernel',
                                      trainable=True)

        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs, *args, **kwargs):
        a = backend.dot(inputs[0], self.kernel)
        y_trans = backend.permute_dimensions(inputs[1], (0, 2, 1))
        b = backend.batch_dot(a, y_trans, axes=[2, 1])
        return backend.tanh(b)

    def compute_output_shape(self, input_shape):

        return None, input_shape[0][1], input_shape[1][1]
