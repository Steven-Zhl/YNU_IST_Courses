import os
import random

import numpy as np
import tensorflow as tf
from keras.layers import Layer

from configs import RANDOM_SEED

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)


class ConcatLayer(Layer):
    def __init__(self, **kwargs):
        super(ConcatLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        super(ConcatLayer, self).build(input_shape)

    def call(self, inputs, **kwargs):
        block_level_code_output = tf.split(inputs, inputs.shape[1], axis=1)
        block_level_code_output = tf.concat(block_level_code_output, axis=2)
        # (bs,600)
        block_level_code_output = tf.squeeze(block_level_code_output, axis=1)
        print(block_level_code_output)
        return block_level_code_output

    def compute_output_shape(self, input_shape):
        print("===========================", input_shape)
        return input_shape[0], input_shape[1] * input_shape[2]
