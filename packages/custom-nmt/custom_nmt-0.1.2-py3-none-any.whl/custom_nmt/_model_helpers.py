# """ This module if for a tensorflow focused implementation of the models and
#     components. Utilises tf.keras, which differs slightly from the keras-only
#     models found in keras_models.py
# """
# import tensorflow as tf
# import numpy as np
# from numpy.random import uniform

# # from tensorflow import keras
# # from tensorflow.keras import layers
# from tensorflow.keras.layers import Embedding, Dense
# from tensorflow.keras.initializers import RandomUniform, GlorotUniform

# MAX_INT = 2147483647

# START_TOKEN = '<start>'
# END_TOKEN = '<end>'
# OOV_TOKEN = '<unk>'

# # import keras_nlp

# # class Transformer:
# #     def __init__(self, source_vocab_size, target_vocab_size, max_sequence_length, embedding_dim, intermediate_dim, num_heads):
# #         # Encoder
# #         encoder_inputs = keras.Input(shape=(None,), dtype="int64", name="encoder_inputs")

# #         x = keras_nlp.layers.TokenAndPositionEmbedding(
# #             vocabulary_size=source_vocab_size,
# #             sequence_length=max_sequence_length,
# #             embedding_dim=embedding_dim,
# #             mask_zero=True,
# #         )(encoder_inputs)

# #         encoder_outputs = keras_nlp.layers.TransformerEncoder(
# #             intermediate_dim=intermediate_dim, num_heads=num_heads
# #         )(inputs=x)
# #         encoder = keras.Model(encoder_inputs, encoder_outputs)


# #         # Decoder
# #         decoder_inputs = keras.Input(shape=(None,), dtype="int64", name="decoder_inputs")
# #         encoded_seq_inputs = keras.Input(shape=(None, embedding_dim), name="decoder_state_inputs")

# #         x = keras_nlp.layers.TokenAndPositionEmbedding(
# #             vocabulary_size=target_vocab_size,
# #             sequence_length=max_sequence_length,
# #             embedding_dim=embedding_dim,
# #             mask_zero=True,
# #         )(decoder_inputs)

# #         x = keras_nlp.layers.TransformerDecoder(
# #             intermediate_dim=intermediate_dim, num_heads=num_heads
# #         )(decoder_sequence=x, encoder_sequence=encoded_seq_inputs)
# #         x = keras.layers.Dropout(0.5)(x)
# #         decoder_outputs = keras.layers.Dense(target_vocab_size, activation="softmax")(x)
# #         decoder = keras.Model(
# #             [
# #                 decoder_inputs,
# #                 encoded_seq_inputs,
# #             ],
# #             decoder_outputs,
# #         )
# #         decoder_outputs = decoder([decoder_inputs, encoder_outputs])

# #         self._transformer = keras.Model(
# #             [encoder_inputs, decoder_inputs],
# #             decoder_outputs,
# #             name="transformer",
# #         )

# #     def compile(self, optimizer: str, loss: str, metrics: list[str]):
# #         self._transformer.compile(optimizer, loss=loss, metrics=metrics)
    
# #     def fit(self, train_dataset, epochs=50, validation_dataset=None):
# #         self._transformer.fit(train_dataset, epochs=epochs, validation_data=validation_dataset)

# #     # def call(self, inp, tar, training, enc_padding_mask, look_ahead_mask, dec_padding_mask):
# #     #     enc_output = self.encoder(inp, training, enc_padding_mask)
# #     #     dec_output, attention_weights = self.decoder(tar, enc_output, training, look_ahead_mask,
# #     #                                                  dec_padding_mask)
# #     #     output = self.final_layer(dec_output) # (batch_size, tar_seq_len, target_vocab_size)
# #     #     return output, attention_weights
    
# #     # def get_dim_model(self):
# #     #     return self._d_model


# # # Old stuff
# # Supporting functions for transformer model
# def positional_encoding(position, d_model):
#     """ Calculates positional encodings. """
#     # Get angles
#     position = np.arange(position)[:, np.newaxis]
#     i = np.arange(d_model)[np.newaxis, :]
#     angle_rads = position / np.power(10000, (2 * (i//2)) / np.float32(d_model))

#     # Apply sin to even indices and cos to odd indices
#     sines, cosines = np.sin(angle_rads[:, 0::2]), np.cos(angle_rads[:, 1::2])
#     pos_encoding = np.concatenate([sines, cosines], axis=-1)
#     pos_encoding = pos_encoding[np.newaxis, ...]
#     return tf.cast(pos_encoding, dtype=tf.float32)

# def create_padding_mask(seq):
#     """ Masks all pad tokens in batch of sequence to avoid treating padding as input. """
#     seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
#     # add extra dimensions to add the padding to attention logits (batch_size, 1, 1, seq_len)
#     return seq[:, tf.newaxis, tf.newaxis, :]

# def create_look_ahead_mask(size):
#     """ Create a mask to stop backward information flow from decoder. """
#     mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
#     return mask # (seq_len, seq_len)

# def scaled_dot_product_attention(q, k, v, mask):
#     """Calculate the attention weights. q, k, v must have matching leading dimensions. The mask has
#     different shapes depending on its type(padding or look ahead) but it must be broadcastable for
#     addition.

#     Parameters:
#         q (tuple<int>): query shape == (..., seq_len_q, depth)
#         k (tuple<int>): key shape == (..., seq_len_k, depth)
#         v (tuple<int>): value shape == (..., seq_len_v, depth)
#         mask: Float tensor with shape broadcastable to (..., seq_len_q, seq_len_k). Default None.

#     Returns: output, attention_weights. """
#     matmul_qk = tf.matmul(q, k, transpose_b=True) # (..., seq_len_q, seq_len_k)

#     # scale matmul_qk
#     dk = tf.cast(tf.shape(k)[-1], tf.float32)
#     scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

#     # add the mask to the scaled tensor.
#     if mask is not None:
#         scaled_attention_logits += (mask * -1e9)

#     # softmax is normalized on the last axis (seq_len_k) so that the scores add up to 1.
#     attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)
#     output = tf.matmul(attention_weights, v) # (..., seq_len_v, depth)
#     return output, attention_weights

# class MultiHeadAttention(tf.keras.layers.Layer):
#     """ Multihead attention sublayer used in both the encoder and decoder of the transformer. """
#     def __init__(self, d_model, num_heads):
#         """ Constructor for MultiHeadAttention.

#         Parameters:
#             d_model (int): Dimension of transformer model.
#             num_heads (int): Number of heads to use in the multihead attention. Must evenly divide
#                              d_model.
#         """
#         super().__init__()
#         self.num_heads = num_heads
#         self.d_model = d_model
#         assert d_model % self.num_heads == 0
#         self.depth = d_model // self.num_heads

#         self.wq = Dense(d_model,
#                         kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
#         self.wk = Dense(d_model,
#                         kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
#         self.wv = Dense(d_model,
#                         kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
#         self.dense = Dense(d_model,
#                            kernel_initializer=GlorotUniform(seed=int(uniform(low=1,
#                                                                              high=MAX_INT))))

#     def split_heads(self, x, batch_size):
#         """Split the last dimension into (num_heads, depth) and transpose the result such that
#         the shape is (batch_size, num_heads, seq_len, depth). """
#         x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
#         return tf.transpose(x, perm=[0, 2, 1, 3])

#     def call(self, v, k, q, mask):
#         batch_size = tf.shape(q)[0]

#         q = self.wq(q) # (batch_size, seq_len, d_model)
#         k = self.wk(k) # (batch_size, seq_len, d_model)
#         v = self.wv(v) # (batch_size, seq_len, d_model)

#         q = self.split_heads(q, batch_size) # (batch_size, num_heads, seq_len_q, depth)
#         k = self.split_heads(k, batch_size) # (batch_size, num_heads, seq_len_k, depth)
#         v = self.split_heads(v, batch_size) # (batch_size, num_heads, seq_len_v, depth)

#         scaled_attention, attention_weights = scaled_dot_product_attention(q, k, v, mask)
#         # Transpose to (batch_size, seq_len_v, num_heads, depth)
#         scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
#         # Reshape to (batch_size, seq_len_v, d_model)
#         concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))
#         output = self.dense(concat_attention)
#         return output, attention_weights

# def point_wise_feed_forward_network(d_model, dff):
#     dense_kernel_initializer1 = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
#     dense_kernel_initializer2 = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
#     layer1 = Dense(dff, kernel_initializer=dense_kernel_initializer1, activation='relu')
#     layer2 = Dense(d_model, kernel_initializer=dense_kernel_initializer2)
#     return tf.keras.Sequential([layer1, layer2])

# def create_masks(inp, tar):
#     # Encoder padding mask
#     enc_padding_mask = create_padding_mask(inp)

#     # Used in the 2nd attention block in the decoder to mask the encoder outputs
#     dec_padding_mask = create_padding_mask(inp)

#     # Used in the 1st attention block in the decoder to pad and mask future tokens in the input
#     # received by the decoder.
#     look_ahead_mask = create_look_ahead_mask(tf.shape(tar)[1])
#     dec_target_padding_mask = create_padding_mask(tar)
#     combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)

#     return enc_padding_mask, combined_mask, dec_padding_mask

# class EncoderLayer(tf.keras.layers.Layer):
#     """ One encoder layer for use in the encoder of the transformer model. """
#     def __init__(self, d_model, num_heads, dff, rate=0.1):
#         super().__init__()

#         self.mha = MultiHeadAttention(d_model, num_heads)
#         self.ffn = point_wise_feed_forward_network(d_model, dff)

#         self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
#         self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

#         self.dropout1 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
#         self.dropout2 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

#     def call(self, x, training, mask):
#         attn_output, _ = self.mha(x, x, x, mask) # (batch_size, input_seq_len, d_model)
#         attn_output = self.dropout1(attn_output, training=training)
#         out1 = self.layernorm1(x + attn_output) # (batch_size, input_seq_len, d_model)

#         ffn_output = self.ffn(out1) # (batch_size, input_seq_len, d_model)
#         ffn_output = self.dropout2(ffn_output, training=training)
#         out2 = self.layernorm2(out1 + ffn_output) # (batch_size, input_seq_len, d_model)

#         return out2

# class DecoderLayer(tf.keras.layers.Layer):
#     """ One decoder layer for use in the encoder of the transformer model. """
#     def __init__(self, d_model, num_heads, dff, rate=0.1):
#         super().__init__()

#         self.mha1 = MultiHeadAttention(d_model, num_heads)
#         self.mha2 = MultiHeadAttention(d_model, num_heads)

#         self.ffn = point_wise_feed_forward_network(d_model, dff)

#         self.layernorm1 = tf.keras.layers.BatchNormalization(epsilon=1e-6)
#         self.layernorm2 = tf.keras.layers.BatchNormalization(epsilon=1e-6)
#         self.layernorm3 = tf.keras.layers.BatchNormalization(epsilon=1e-6)

#         self.dropout1 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
#         self.dropout2 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
#         self.dropout3 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

#     def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
#         attn1, attn_weights_block1 = self.mha1(x, x, x, look_ahead_mask)
#         attn1 = self.dropout1(attn1, training=training)
#         out1 = self.layernorm1(attn1 + x)

#         attn2, attn_weights_block2 = self.mha2(enc_output, enc_output, out1, padding_mask)
#         attn2 = self.dropout2(attn2, training=training)
#         out2 = self.layernorm2(attn2 + out1) # (batch_size, target_seq_len, d_model)

#         ffn_output = self.ffn(out2) # (batch_size, target_seq_len, d_model)
#         ffn_output = self.dropout3(ffn_output, training=training)
#         out3 = self.layernorm3(ffn_output + out2) # (batch_size, target_seq_len, d_model)

#         return out3, attn_weights_block1, attn_weights_block2

# class TransformerEncoder(tf.keras.layers.Layer):
#     """ Encoder (multiple stacked EncoderLayers) for use in Transformer. """
#     def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, rate=0.1):
#         super().__init__()
#         self.d_model = d_model
#         self.num_layers = num_layers
#         embeddings_initializer = RandomUniform(seed=int(uniform(low=1, high=MAX_INT)))
#         self.embedding = Embedding(input_vocab_size, d_model,
#                                    embeddings_initializer=embeddings_initializer)
#         self.pos_encoding = positional_encoding(input_vocab_size, self.d_model)
#         self.enc_layers = [EncoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
#         self.dropout = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

#     def call(self, x, training, mask):
#         seq_len = tf.shape(x)[1]

#         # adding embedding and position encoding.
#         x = self.embedding(x) # (batch_size, input_seq_len, d_model)
#         x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
#         x += self.pos_encoding[:, :seq_len, :]
#         x = self.dropout(x, training=training)

#         for i in range(self.num_layers):
#             x = self.enc_layers[i](x, training, mask)

#         return x # (batch_size, input_seq_len, d_model)

# class TransformerDecoder(tf.keras.layers.Layer):
#     """ Decoder (multiple stacked DecoderLayers) for use in Transformer. """
#     def __init__(self, num_layers, d_model, num_heads, dff, target_vocab_size, rate=0.1):
#         super().__init__()
#         self.d_model = d_model
#         self.num_layers = num_layers
#         embeddings_initializer = RandomUniform(seed=int(uniform(low=1, high=MAX_INT)))
#         self.embedding = Embedding(target_vocab_size, d_model,
#                                    embeddings_initializer=embeddings_initializer)
#         self.pos_encoding = positional_encoding(target_vocab_size, self.d_model)
#         self.dec_layers = [DecoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
#         self.dropout = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

#     def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
#         seq_len = tf.shape(x)[1]
#         attention_weights = {}
#         x = self.embedding(x) # (batch_size, target_seq_len, d_model)
#         x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
#         x += self.pos_encoding[:, :seq_len, :]
#         x = self.dropout(x, training=training)

#         for i in range(self.num_layers):
#             x, block1, block2 = self.dec_layers[i](x, enc_output, training, look_ahead_mask,
#                                                    padding_mask)
#             attention_weights[f'decoder_layer{i+1}_block1'] = block1
#             attention_weights[f'decoder_layer{i+1}_block2'] = block2

#         return x, attention_weights

# class Transformer(tf.keras.Model):
#     """ Transformer model """
#     def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, target_vocab_size,
#                  rate=0.1):
#         super().__init__()
#         self.encoder = TransformerEncoder(num_layers, d_model, num_heads, dff, input_vocab_size,
#                                           rate)
#         self.decoder = TransformerDecoder(num_layers, d_model, num_heads, dff, target_vocab_size,
#                                           rate)
#         kernel_initializer = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
#         self.final_layer = Dense(target_vocab_size, kernel_initializer=kernel_initializer)

#         self._d_model = d_model

#     def call(self, inp, tar, training, enc_padding_mask, look_ahead_mask, dec_padding_mask):
#         enc_output = self.encoder(inp, training, enc_padding_mask)
#         dec_output, attention_weights = self.decoder(tar, enc_output, training, look_ahead_mask,
#                                                      dec_padding_mask)
#         output = self.final_layer(dec_output) # (batch_size, tar_seq_len, target_vocab_size)
#         return output, attention_weights
    
#     def get_dim_model(self):
#         return self._d_model

# class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
#     """ A custom training schedule as per transformer paper. """
#     def __init__(self, d_model, warmup_steps=4000):
#         super().__init__()
#         self.d_model = tf.cast(d_model, tf.float32)
#         self.warmup_steps = warmup_steps

#     def __call__(self, step):
#         arg1 = tf.math.rsqrt(step)
#         arg2 = step * (self.warmup_steps ** -1.5)
#         return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)

""" This module if for a tensorflow focused implementation of the models and
    components. Utilises tf.keras, which differs slightly from the keras-only
    models found in keras_models.py
"""
import tensorflow as tf
import numpy as np
from numpy.random import uniform
from tensorflow.keras.layers import Embedding, Dense
from tensorflow.keras.initializers import RandomUniform, GlorotUniform

MAX_INT = 2147483647

START_TOKEN = '<start>'
END_TOKEN = '<end>'
OOV_TOKEN = '<unk>'

# Supporting functions for transformer model
def positional_encoding(position, d_model):
    """ Calculates positional encodings. """
    # Get angles
    position = np.arange(position)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rads = position / np.power(10000, (2 * (i//2)) / np.float32(d_model))

    # Apply sin to even indices and cos to odd indices
    sines, cosines = np.sin(angle_rads[:, 0::2]), np.cos(angle_rads[:, 1::2])
    pos_encoding = np.concatenate([sines, cosines], axis=-1)
    pos_encoding = pos_encoding[np.newaxis, ...]
    return tf.cast(pos_encoding, dtype=tf.float32)

def create_padding_mask(seq):
    """ Masks all pad tokens in batch of sequence to avoid treating padding as input. """
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
    # add extra dimensions to add the padding to attention logits (batch_size, 1, 1, seq_len)
    return seq[:, tf.newaxis, tf.newaxis, :]

def create_look_ahead_mask(size):
    """ Create a mask to stop backward information flow from decoder. """
    mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
    return mask # (seq_len, seq_len)

def scaled_dot_product_attention(q, k, v, mask):
    """Calculate the attention weights. q, k, v must have matching leading dimensions. The mask has
    different shapes depending on its type(padding or look ahead) but it must be broadcastable for
    addition.
    Parameters:
        q (tuple<int>): query shape == (..., seq_len_q, depth)
        k (tuple<int>): key shape == (..., seq_len_k, depth)
        v (tuple<int>): value shape == (..., seq_len_v, depth)
        mask: Float tensor with shape broadcastable to (..., seq_len_q, seq_len_k). Default None.
    Returns: output, attention_weights. """
    matmul_qk = tf.matmul(q, k, transpose_b=True) # (..., seq_len_q, seq_len_k)

    # scale matmul_qk
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

    # add the mask to the scaled tensor.
    if mask is not None:
        scaled_attention_logits += (mask * -1e9)

    # softmax is normalized on the last axis (seq_len_k) so that the scores add up to 1.
    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)
    output = tf.matmul(attention_weights, v) # (..., seq_len_v, depth)
    return output, attention_weights

class MultiHeadAttention(tf.keras.layers.Layer):
    """ Multihead attention sublayer used in both the encoder and decoder of the transformer. """
    def __init__(self, d_model, num_heads):
        """ Constructor for MultiHeadAttention.
        Parameters:
            d_model (int): Dimension of transformer model.
            num_heads (int): Number of heads to use in the multihead attention. Must evenly divide
                             d_model.
        """
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        assert d_model % self.num_heads == 0
        self.depth = d_model // self.num_heads

        self.wq = Dense(d_model,
                        kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
        self.wk = Dense(d_model,
                        kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
        self.wv = Dense(d_model,
                        kernel_initializer=GlorotUniform(seed=int(uniform(low=1, high=MAX_INT))))
        self.dense = Dense(d_model,
                           kernel_initializer=GlorotUniform(seed=int(uniform(low=1,
                                                                             high=MAX_INT))))

    def split_heads(self, x, batch_size):
        """Split the last dimension into (num_heads, depth) and transpose the result such that
        the shape is (batch_size, num_heads, seq_len, depth). """
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, v, k, q, mask):
        batch_size = tf.shape(q)[0]

        q = self.wq(q) # (batch_size, seq_len, d_model)
        k = self.wk(k) # (batch_size, seq_len, d_model)
        v = self.wv(v) # (batch_size, seq_len, d_model)

        q = self.split_heads(q, batch_size) # (batch_size, num_heads, seq_len_q, depth)
        k = self.split_heads(k, batch_size) # (batch_size, num_heads, seq_len_k, depth)
        v = self.split_heads(v, batch_size) # (batch_size, num_heads, seq_len_v, depth)

        scaled_attention, attention_weights = scaled_dot_product_attention(q, k, v, mask)
        # Transpose to (batch_size, seq_len_v, num_heads, depth)
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        # Reshape to (batch_size, seq_len_v, d_model)
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))
        output = self.dense(concat_attention)
        return output, attention_weights

def point_wise_feed_forward_network(d_model, dff):
    dense_kernel_initializer1 = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
    dense_kernel_initializer2 = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
    layer1 = Dense(dff, kernel_initializer=dense_kernel_initializer1, activation='relu')
    layer2 = Dense(d_model, kernel_initializer=dense_kernel_initializer2)
    return tf.keras.Sequential([layer1, layer2])

def create_masks(inp, tar):
    # Encoder padding mask
    enc_padding_mask = create_padding_mask(inp)

    # Used in the 2nd attention block in the decoder to mask the encoder outputs
    dec_padding_mask = create_padding_mask(inp)

    # Used in the 1st attention block in the decoder to pad and mask future tokens in the input
    # received by the decoder.
    look_ahead_mask = create_look_ahead_mask(tf.shape(tar)[1])
    dec_target_padding_mask = create_padding_mask(tar)
    combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)

    return enc_padding_mask, combined_mask, dec_padding_mask

class EncoderLayer(tf.keras.layers.Layer):
    """ One encoder layer for use in the encoder of the transformer model. """
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = point_wise_feed_forward_network(d_model, dff)

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
        self.dropout2 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

    def call(self, x, training, mask):
        attn_output, _ = self.mha(x, x, x, mask) # (batch_size, input_seq_len, d_model)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output) # (batch_size, input_seq_len, d_model)

        ffn_output = self.ffn(out1) # (batch_size, input_seq_len, d_model)
        ffn_output = self.dropout2(ffn_output, training=training)
        out2 = self.layernorm2(out1 + ffn_output) # (batch_size, input_seq_len, d_model)

        return out2

class DecoderLayer(tf.keras.layers.Layer):
    """ One decoder layer for use in the encoder of the transformer model. """
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super().__init__()

        self.mha1 = MultiHeadAttention(d_model, num_heads)
        self.mha2 = MultiHeadAttention(d_model, num_heads)

        self.ffn = point_wise_feed_forward_network(d_model, dff)

        self.layernorm1 = tf.keras.layers.BatchNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.BatchNormalization(epsilon=1e-6)
        self.layernorm3 = tf.keras.layers.BatchNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
        self.dropout2 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))
        self.dropout3 = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        attn1, attn_weights_block1 = self.mha1(x, x, x, look_ahead_mask)
        attn1 = self.dropout1(attn1, training=training)
        out1 = self.layernorm1(attn1 + x)

        attn2, attn_weights_block2 = self.mha2(enc_output, enc_output, out1, padding_mask)
        attn2 = self.dropout2(attn2, training=training)
        out2 = self.layernorm2(attn2 + out1) # (batch_size, target_seq_len, d_model)

        ffn_output = self.ffn(out2) # (batch_size, target_seq_len, d_model)
        ffn_output = self.dropout3(ffn_output, training=training)
        out3 = self.layernorm3(ffn_output + out2) # (batch_size, target_seq_len, d_model)

        return out3, attn_weights_block1, attn_weights_block2

class TransformerEncoder(tf.keras.layers.Layer):
    """ Encoder (multiple stacked EncoderLayers) for use in Transformer. """
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, rate=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        embeddings_initializer = RandomUniform(seed=int(uniform(low=1, high=MAX_INT)))
        self.embedding = Embedding(input_vocab_size, d_model,
                                   embeddings_initializer=embeddings_initializer)
        self.pos_encoding = positional_encoding(input_vocab_size, self.d_model)
        self.enc_layers = [EncoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

    def call(self, x, training, mask):
        seq_len = tf.shape(x)[1]

        # adding embedding and position encoding.
        x = self.embedding(x) # (batch_size, input_seq_len, d_model)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x += self.pos_encoding[:, :seq_len, :]
        x = self.dropout(x, training=training)

        for i in range(self.num_layers):
            x = self.enc_layers[i](x, training, mask)

        return x # (batch_size, input_seq_len, d_model)

class TransformerDecoder(tf.keras.layers.Layer):
    """ Decoder (multiple stacked DecoderLayers) for use in Transformer. """
    def __init__(self, num_layers, d_model, num_heads, dff, target_vocab_size, rate=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        embeddings_initializer = RandomUniform(seed=int(uniform(low=1, high=MAX_INT)))
        self.embedding = Embedding(target_vocab_size, d_model,
                                   embeddings_initializer=embeddings_initializer)
        self.pos_encoding = positional_encoding(target_vocab_size, self.d_model)
        self.dec_layers = [DecoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate, seed=int(uniform(low=1, high=MAX_INT)))

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        seq_len = tf.shape(x)[1]
        attention_weights = {}
        x = self.embedding(x) # (batch_size, target_seq_len, d_model)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x += self.pos_encoding[:, :seq_len, :]
        x = self.dropout(x, training=training)

        for i in range(self.num_layers):
            x, block1, block2 = self.dec_layers[i](x, enc_output, training, look_ahead_mask,
                                                   padding_mask)
            attention_weights[f'decoder_layer{i+1}_block1'] = block1
            attention_weights[f'decoder_layer{i+1}_block2'] = block2

        return x, attention_weights

class Transformer(tf.keras.Model):
    """ Transformer model """
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, target_vocab_size,
                 rate=0.1):
        super().__init__()
        self.encoder = TransformerEncoder(num_layers, d_model, num_heads, dff, input_vocab_size,
                                          rate)
        self.decoder = TransformerDecoder(num_layers, d_model, num_heads, dff, target_vocab_size,
                                          rate)
        kernel_initializer = GlorotUniform(seed=int(uniform(low=1, high=MAX_INT)))
        self.final_layer = Dense(target_vocab_size, kernel_initializer=kernel_initializer)

        self._d_model = d_model

    def call(self, inp, tar, training, enc_padding_mask, look_ahead_mask, dec_padding_mask):
        enc_output = self.encoder(inp, training, enc_padding_mask)
        dec_output, attention_weights = self.decoder(tar, enc_output, training, look_ahead_mask,
                                                     dec_padding_mask)
        output = self.final_layer(dec_output) # (batch_size, tar_seq_len, target_vocab_size)
        return output, attention_weights
    
    def get_dim_model(self):
        return self._d_model

class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
    """ A custom training schedule as per transformer paper. """
    def __init__(self, d_model, warmup_steps=4000):
        super().__init__()
        self.d_model = tf.cast(d_model, tf.float32)
        self.warmup_steps = warmup_steps

    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * (self.warmup_steps ** -1.5)
        return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)
