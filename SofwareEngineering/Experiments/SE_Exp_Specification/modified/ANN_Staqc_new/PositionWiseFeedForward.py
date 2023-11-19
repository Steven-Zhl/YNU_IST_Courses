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


class PositionWiseFeedForward(Layer):
    # inner_dim 隐藏层的维度，一般默认2048,model_dim是词向量的维度
    def __init__(self, model_dim, inner_dim, trainable=True, **kwargs):
        self._model_dim = model_dim
        self._inner_dim = inner_dim
        self._trainable = trainable
        super(PositionWiseFeedForward, self).__init__(**kwargs)
        self.weights_out = None
        self.weights_inner = None
        self.bias_inner = None
        self.bias_out = None

    def build(self, input_shape):
        self.weights_inner = self.add_weight(
            shape=(input_shape[-1], self._inner_dim),
            initializer='glorot_uniform',
            trainable=self._trainable,
            name="weights_inner")
        self.weights_out = self.add_weight(
            shape=(self._inner_dim, self._model_dim),
            initializer='glorot_uniform',
            trainable=self._trainable,
            name="weights_out")
        self.bias_inner = self.add_weight(
            shape=(self._inner_dim,),
            initializer='uniform',
            trainable=self._trainable,
            name="bias_inner")
        self.bias_out = self.add_weight(
            shape=(self._model_dim,),
            initializer='uniform',
            trainable=self._trainable,
            name="bias_out")
        super(PositionWiseFeedForward, self).build(input_shape)

    def call(self, inputs, **kwargs):
        if backend.dtype(inputs) != 'float32':
            inputs = backend.cast(inputs, 'float32')
        inner_out = backend.relu(backend.dot(inputs, self.weights_inner) + self.bias_inner)
        outputs = backend.dot(inner_out, self.weights_out) + self.bias_out
        print("==", outputs.shape)
        return outputs

    def compute_output_shape(self, input_shape):
        return input_shape
