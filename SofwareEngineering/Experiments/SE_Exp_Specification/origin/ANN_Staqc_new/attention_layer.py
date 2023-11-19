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

class AttentionLayer(Layer):

    def __init__(self, **kwargs):
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

    def call(self, inputs):
        a = K.dot(inputs[0], self.kernel)
        y_trans = K.permute_dimensions(inputs[1], (0,2,1))
        b = K.batch_dot(a, y_trans, axes=[2,1])
        return K.tanh(b)
    
    def compute_output_shape(self, input_shape):

        return (None, input_shape[0][1],input_shape[1][1])
