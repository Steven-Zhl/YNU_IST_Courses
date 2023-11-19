import os
import random

import numpy as np
import tensorflow as tf
from keras import backend
from keras.layers import Layer
from tensorflow import keras

from configs import RANDOM_SEED

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
random.seed(RANDOM_SEED)


class ScaledDotProductAttention(Layer):
    """The attention layer that takes three inputs representing queries, keys and values.
    \text{Attention}(Q, backend, V) = \text{softmax}(\frac{Q backend^T}{\sqrt{d_k}}) V
    See: https://arxiv.org/pdf/1706.03762.pdf
    """

    def __init__(self, return_attention=False, history_only=False, **kwargs):
        """Initialize the layer.
        :param return_attention: Whether to return attention weights.
        :param history_only: Whether to only use history data.
        :param kwargs: Arguments for parent class.
        """
        super(ScaledDotProductAttention, self).__init__(**kwargs)
        self.supports_masking = True
        self.return_attention = return_attention
        self.history_only = history_only
        self.intensity = self.attention = None

    def get_config(self):
        config = {
            'return_attention': self.return_attention,
            'history_only': self.history_only,
        }
        base_config = super(ScaledDotProductAttention, self).getConfig()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        if isinstance(input_shape, list):
            query_shape, key_shape, value_shape = input_shape
        else:
            query_shape = key_shape = value_shape = input_shape
        output_shape = query_shape[:-1] + value_shape[-1:]
        if self.return_attention:
            attention_shape = query_shape[:2] + (key_shape[1],)
            return [output_shape, attention_shape]
        return output_shape

    def compute_mask(self, inputs, mask=None):
        if isinstance(mask, list):
            mask = mask[0]
        if self.return_attention:
            return [mask, None]
        return mask

    def call(self, inputs, mask=None, **kwargs):
        if isinstance(inputs, list):
            query, key, value = inputs
        else:
            query = key = value = inputs
        if isinstance(mask, list):
            mask = mask[1]
        feature_dim = backend.shape(query)[-1]  # 512
        # query = (bs,seq_len,dim)
        # key = (bs,seq_len,dim)
        # batch_dot后bs,seq_len,seq_len
        e = backend.batch_dot(query, key, axes=2) / backend.sqrt(backend.cast(feature_dim, dtype=backend.floatx()))
        if self.history_only:
            query_len, key_len = backend.shape(query)[1], backend.shape(key)[1]
            indices = backend.expand_dims(backend.arange(0, key_len), axis=0)
            upper = backend.expand_dims(backend.arange(0, query_len), axis=-1)
            e -= 10000.0 * backend.expand_dims(backend.cast(indices > upper, backend.floatx()), axis=0)
        if mask is not None:
            e -= 10000.0 * (1.0 - backend.cast(backend.expand_dims(mask, axis=-2), backend.floatx()))
        self.intensity = e
        e = backend.exp(e - backend.max(e, axis=-1, keepdims=True))
        self.attention = e / backend.sum(e, axis=-1, keepdims=True)
        # self.attention = bs,seq_len,seq_len
        # value = bs,seq_len,dim
        # v = bs,seq_len,dim
        v = backend.batch_dot(self.attention, value)
        if self.return_attention:
            return [v, self.attention]
        return v


class MultiHeadAttention(Layer):
    """Multi-head attention layer.
    See: https://arxiv.org/pdf/1706.03762.pdf
    """

    def __init__(self,
                 head_num,
                 activation='relu',
                 use_bias=True,
                 kernel_initializer='glorot_normal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 history_only=False,
                 **kwargs):
        """Initialize the layer.
        :param head_num: Number of heads.
        :param activation: Activations for linear mappings.
        :param use_bias: Whether to use bias term.
        :param kernel_initializer: Initializer for linear mappings.
        :param bias_initializer: Initializer for linear mappings.
        :param kernel_regularizer: Regularizer for linear mappings.
        :param bias_regularizer: Regularizer for linear mappings.
        :param kernel_constraint: Constraints for linear mappings.
        :param bias_constraint: Constraints for linear mappings.
        :param history_only: Whether to only use history in attention layer.
        """
        self.supports_masking = True
        self.head_num = head_num
        self.activation = keras.activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = keras.initializers.get(kernel_initializer)
        self.bias_initializer = keras.initializers.get(bias_initializer)
        self.kernel_regularizer = keras.regularizers.get(kernel_regularizer)
        self.bias_regularizer = keras.regularizers.get(bias_regularizer)
        self.kernel_constraint = keras.constraints.get(kernel_constraint)
        self.bias_constraint = keras.constraints.get(bias_constraint)
        self.history_only = history_only

        self.Wq = self.Wk = self.Wv = self.Wo = None
        self.bq = self.bk = self.bv = self.bo = None

        self.intensity = self.attention = None
        super(MultiHeadAttention, self).__init__(**kwargs)

    def get_config(self):
        config = {
            'head_num': self.head_num,
            'activation': keras.activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': keras.initializers.serialize(self.kernel_initializer),
            'bias_initializer': keras.initializers.serialize(self.bias_initializer),
            'kernel_regularizer': keras.regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': keras.regularizers.serialize(self.bias_regularizer),
            'kernel_constraint': keras.constraints.serialize(self.kernel_constraint),
            'bias_constraint': keras.constraints.serialize(self.bias_constraint),
            'history_only': self.history_only,
        }
        base_config = super(MultiHeadAttention, self).getConfig()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        if isinstance(input_shape, list):
            q, k, v = input_shape
            return q[:-1] + (v[-1],)
        return input_shape

    def compute_mask(self, inputs, input_mask=None):
        if isinstance(input_mask, list):
            return input_mask[0]
        return input_mask

    def build(self, input_shape):
        if isinstance(input_shape, list):
            q, k, v = input_shape
        else:
            q = k = v = input_shape
        feature_dim = int(v[-1])
        if feature_dim % self.head_num != 0:
            raise IndexError('Invalid head number %d with the given input dim %d' % (self.head_num, feature_dim))
        self.Wq = self.add_weight(
            shape=(int(q[-1]), feature_dim),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint,
            name='%s_Wq' % self.name,
        )
        if self.use_bias:
            self.bq = self.add_weight(
                shape=(feature_dim,),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint,
                name='%s_bq' % self.name,
            )
        self.Wk = self.add_weight(
            shape=(int(k[-1]), feature_dim),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint,
            name='%s_Wk' % self.name,
        )
        if self.use_bias:
            self.bk = self.add_weight(
                shape=(feature_dim,),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint,
                name='%s_bk' % self.name,
            )
        self.Wv = self.add_weight(
            shape=(int(v[-1]), feature_dim),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint,
            name='%s_Wv' % self.name,
        )
        if self.use_bias:
            self.bv = self.add_weight(
                shape=(feature_dim,),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint,
                name='%s_bv' % self.name,
            )
        self.Wo = self.add_weight(
            shape=(feature_dim, feature_dim),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint,
            name='%s_Wo' % self.name,
        )
        if self.use_bias:
            self.bo = self.add_weight(
                shape=(feature_dim,),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint,
                name='%s_bo' % self.name,
            )
        super(MultiHeadAttention, self).build(input_shape)

    @staticmethod
    def _reshape_to_batches(x, head_num):
        # split to head num
        input_shape = backend.shape(x)
        batch_size, seq_len, feature_dim = input_shape[0], input_shape[1], input_shape[2]
        head_dim = feature_dim // head_num
        x = backend.reshape(x, (batch_size, seq_len, head_num, head_dim))
        # 为了方便scaled dot attention 计算（输入是bs, seq_len,head_dim）,这里做了transpose和reshape
        x = backend.permute_dimensions(x, [0, 2, 1, 3])  # transpose,把并行计算的head_num维度提到前面
        return backend.reshape(x, (batch_size * head_num, seq_len, head_dim))  # reshape,因为bs轴在scaled dot里面不参与计算

    @staticmethod
    def _reshape_attention_from_batches(x, head_num):  # attention得分矩阵的反向恢复
        input_shape = backend.shape(x)
        batch_size, seq_len, feature_dim = input_shape[0], input_shape[1], input_shape[2]
        x = backend.reshape(x, (batch_size // head_num, head_num, seq_len, feature_dim))
        return backend.permute_dimensions(x, [0, 2, 1, 3])

    @staticmethod
    def _reshape_from_batches(x, head_num):  # attention后的向量恢复
        input_shape = backend.shape(x)
        batch_size, seq_len, feature_dim = input_shape[0], input_shape[1], input_shape[
            2]  # bs*head_num,seq_len,head_dim
        x = backend.reshape(x, (batch_size // head_num, head_num, seq_len, feature_dim))  # bs,head_num,seq_len,head_dim
        x = backend.permute_dimensions(x, [0, 2, 1, 3])  # bs,seq_len,head_num,head_dim
        return backend.reshape(x, (batch_size // head_num, seq_len, feature_dim * head_num))  # bs,seq_len,model_dim

    @staticmethod
    def _reshape_mask(mask, head_num):
        if mask is None:
            return mask
        seq_len = backend.shape(mask)[1]
        mask = backend.expand_dims(mask, axis=1)
        mask = backend.tile(mask, [1, head_num, 1])
        return backend.reshape(mask, (-1, seq_len))

    def call(self, inputs, mask=None, **kwargs):
        if isinstance(inputs, list):
            q, k, v = inputs
        else:
            q = k = v = inputs  # bs,seq_len,model_dim
        if isinstance(mask, list):
            q_mask, k_mask, v_mask = mask
        else:
            q_mask = k_mask = v_mask = mask
        q = backend.dot(q, self.Wq)  # 先做变换再分成8个，和先分成8*64个再做变换，参数量都是一样的512*512
        k = backend.dot(k, self.Wk)
        v = backend.dot(v, self.Wv)
        if self.use_bias:
            q += self.bq
            k += self.bk
            v += self.bv
        if self.activation is not None:
            q = self.activation(q)
            k = self.activation(k)
            v = self.activation(v)
        scaled_dot_product_attention = ScaledDotProductAttention(
            history_only=self.history_only,
            name='%s-Attention' % self.name,
        )
        y = scaled_dot_product_attention(
            inputs=[
                self._reshape_to_batches(q, self.head_num),  # query,bs*num(head),seq_len,dim,head_dim
                self._reshape_to_batches(k, self.head_num),  # key
                self._reshape_to_batches(v, self.head_num),  # value
            ],
            mask=[
                self._reshape_mask(q_mask, self.head_num),
                self._reshape_mask(k_mask, self.head_num),
                self._reshape_mask(v_mask, self.head_num),
            ],
        )
        # 相似度矩阵
        # self.intensity = self._reshape_attention_from_batches(scaled_dot_product_attention.intensity, self.head_num)
        # self.attention = self._reshape_attention_from_batches(scaled_dot_product_attention.attention, self.head_num)
        y = self._reshape_from_batches(y, self.head_num)  # 合并
        y = backend.dot(y, self.Wo)  # 最终输出
        if self.use_bias:
            y += self.bo
        if self.activation is not None:
            y = self.activation(y)

        # Add shape information to tensor
        input_shape = [backend.int_shape(q), backend.int_shape(k), backend.int_shape(v)]
        output_shape = self.compute_output_shape(input_shape)
        if output_shape[1] is not None:
            output_shape = (-1,) + output_shape[1:]
            y = backend.reshape(y, output_shape)
        return y


'''
query = tf.random.truncated_normal([100, 50, 160])
w = MultiHeadAttention_(16)([query,query,query])
print(w.shape)
'''
