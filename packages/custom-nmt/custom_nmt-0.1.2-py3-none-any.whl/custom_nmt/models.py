from ._model_helpers import Transformer, CustomSchedule, create_masks
from ._exceptions import InvalidGraphError
import tensorflow as tf
import numpy as np
from .constants import START_TOKEN, END_TOKEN
from tensorflow.keras.preprocessing.sequence import pad_sequences
import time

class AbstractModel:
    """An interface to be implemented by all custom models. """
    def construct(self, nodes, edges):
        raise NotImplementedError('Models must implement a construct method.')
    
    def fit(self, training_data, validation_data, hyperparameters):
        raise NotImplementedError('Models must implement a fit method')
    
    def evaluate(self, test_data, metric='bleu'):
        raise NotImplementedError('Models must implement an evaluate method')

    def infer(self, source_text):
        raise NotImplementedError('Models must implement an infer method')

class TransformerModel(AbstractModel):
    def construct(self, network_graph, settings):
        nodes = network_graph.get_nodes() # TODO: make this a nicer deconstruction of graph
        
        for node in nodes:
            node_name = node.get_name()
            if node_name == 'input':
                input_size = node.get_size()
            elif node_name == 'output':
                output_size = node.get_size()
            elif node_name == 'transformer':
                node_info = node.get_info()
                num_layers = node_info['num_layers']
                d_model = node_info['d_model']
                num_heads = node_info['num_heads']
                dff = node_info['dff']
                # input_size = node_info['input_size']
                # output_size = node_info['output_size']
                dropout = node_info['dropout']

                # num_layers, d_model, num_heads, dff, dropout = node.get_info()
            else:
                raise InvalidGraphError('This transformer model has a non input or output or transformer node')
            
        self._transformer = Transformer(num_layers, d_model, num_heads, dff, input_size, output_size, dropout)
        self._optimizer = self._get_optimizer(settings)
        self._loss_object = self._get_loss_object(settings)
        self._loss_tracker = {'training_losses': [], 'validation_losses': []}

        print('optimizer is', self._optimizer)
        print('model has', num_layers, d_model, num_heads, dff, input_size, output_size, dropout)
    
    def load_existing_model(self, checkpoint_dir):
        # Assume constructed
        ckpt = tf.train.Checkpoint(transformer=self._transformer, optimizer=self._optimizer)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        ckpt.restore(latest)
        print('loaded')

    def _get_optimizer(self, settings):
        """ Construct the optimizer object from the requested optimizer
            information in settings. Defaults to Adam optimizer.
        
        Parameters:
            settings: dictionary of training settings and hyperparameters.
        
        Pre-conditions:
            settings must contain the appropriate hyperparameters for the
            optimizer requested.
        """
        optimizer_type = settings.get('optimizer', 'Adam')
        learning_rate = settings.get('lr', 0.3)

        # TODO: take this out or make optional!
        learning_rate = CustomSchedule(self._transformer.get_dim_model())

        if optimizer_type == 'Adam':
            return tf.keras.optimizers.Adam(
                learning_rate,
                beta_1=settings.get('beta1'),
                beta_2=settings.get('beta2'),
                epsilon=settings.get('epsilon')
            )
        elif optimizer_type == 'RMSProp':
            return tf.keras.optimizers.RMSprop(
                learning_rate=learning_rate,
                rho=settings.get('rho'),
                momentum=settings.get('momentum'),
                epsilon=settings.get('epsilon'),
                centered=(settings.get('centered') == 'true'), name='RMSprop')
        elif optimizer_type == 'Adagrad':
            return tf.keras.optimizers.Adagrad(
                learning_rate=learning_rate,
                initial_accumulator_value=settings.get('initial_accum'),
                epsilon=settings.get('epsilon'),
                name='Adagrad')
        elif optimizer_type == 'Adadelta':
            return tf.keras.optimizers.Adadelta(
                learning_rate=learning_rate,
                rho=settings.get('rho'),
                epsilon=settings.get('epsilon'),
                name='Adadelta')
        elif optimizer_type == 'sgd':
            return tf.keras.optimizers.SGD(
                learning_rate=learning_rate,
                momentum=settings.get('momentum'),
                nesterov=(settings.get('nesterov', 'false') == 'true'),
                name='SGD')

    def loss_function(self, real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss_ = self._loss_object(real, pred)

        mask = tf.cast(mask, dtype=loss_.dtype)
        loss_ *= mask

        return tf.reduce_mean(loss_)
    
    def get_loss_tracker(self):
        return self._loss_tracker

    def _get_loss_object(self, settings):
        """ Construct the loss object based on the requested loss to use.
        
            Currently, only supports sparse categorical cross entropy.
        """
        return tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')


    def fit(self, dataset: 'Dataset', settings):
        train_loss = tf.keras.metrics.Mean(name='train_loss')
        train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

        @tf.function
        def train_step(inp, tar):
            tar_inp, tar_real = tar[:, :-1], tar[:, 1:]
            enc_padding_mask, combined_mask, dec_padding_mask = create_masks(inp, tar_inp)

            with tf.GradientTape() as tape:
                predictions, _ = self._transformer(inp, tar_inp, True, enc_padding_mask, combined_mask,
                                            dec_padding_mask)
                loss = self.loss_function(tar_real, predictions)

            gradients = tape.gradient(loss, self._transformer.trainable_variables)
            self._optimizer.apply_gradients(zip(gradients, self._transformer.trainable_variables))

            train_loss(loss)
            train_accuracy(tar_real, predictions)

        @tf.function
        def validation_step(inp, tar):
            tar_inp, tar_real = tar[:,:-1], tar[:, 1:]
            enc_padding_mask, combined_mask, dec_padding_mask = create_masks(inp, tar_inp)
            predictions, _ = self._transformer(inp, tar_inp, True, enc_padding_mask, combined_mask,
                                        dec_padding_mask)
            loss = self.loss_function(tar_real, predictions)
            train_loss(loss)
            train_accuracy(tar_real, predictions)
        
        # TODO: currently batch size needs to be very low with very limited data or
        # there's an error; handle better / provide error message
        train_dataset, val_dataset, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
        buffer_size = dataset.get_training_size()
        batch_size = dataset.get_batch_size()
        steps_per_epoch = buffer_size // batch_size
        max_epochs = settings.get('num_epochs', 5)

        # file = open('training_losses.txt', 'w')

        num_epochs_worse = 0
        best_validation_loss = float('inf')
        checkpoint_path = './checkpoints/train'
        ckpt = tf.train.Checkpoint(transformer=self._transformer, optimizer=self._optimizer)
        patience = settings.get('patience', 3)
        ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=patience + 1)

        # TODO: currently batch size needs to be very low with very limited data or
        # there's an error; handle better / provide error message
        train_dataset, val_dataset, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
        buffer_size = dataset.get_training_size()
        batch_size = dataset.get_batch_size()
        steps_per_epoch = buffer_size // batch_size
        max_epochs = settings.get('num_epochs', 5)

        file = open('training_losses.txt', 'w')

        for epoch in range(1, max_epochs + 1):
            epoch_start = time.time()
            epoch_loss = 0
            train_loss.reset_states()
            train_accuracy.reset_states()

            for (train_batch, (inp, tar)) in enumerate(train_dataset.take(steps_per_epoch)):
                train_step(inp, tar)
                epoch_loss += train_loss.result()
                if train_batch % 100 == 0:
                    print(f'Finished batch {train_batch} of epoch {epoch}', flush=True)
            training_loss = train_loss.result()
            
            
            # Validation and early stopping
            # train_loss.reset_states()
            # train_accuracy.reset_states()
            validation_loss = 0
            NUM_VAL_BATCHES = dataset.get_validation_size() // batch_size
            for (batch, (source, target)) in enumerate(val_dataset.take(dataset.get_validation_size())):
                validation_step(source, target)
                validation_loss += train_loss.result()
            # validation_loss = train_loss.result()
            print('validation loss is', validation_loss, 'and num_val_batches is', NUM_VAL_BATCHES)
            # TODO: took this out to get it on same scale as training (I think per epoch rather than per batch), work out a better way later
            # validation_loss /= NUM_VAL_BATCHES
            # validation_loss = validation_loss.numpy()
            training_loss = training_loss.numpy()
            self._loss_tracker['training_losses'].append(training_loss)
            self._loss_tracker['validation_losses'].append(validation_loss)

            # file.write(f'Epoch: {epoch}\nTrain loss: {training_loss}\nVal loss: {validation_loss}\n\n')
            # file.flush()
            
            if validation_loss >= best_validation_loss:
                num_epochs_worse += 1
            else:
                num_epochs_worse = 0
                best_validation_loss = validation_loss

                validation_loss /= NUM_VAL_BATCHES
                training_loss = epoch_loss / (train_batch + 1)
                print(f'train: save model,epoch {epoch}, train loss {training_loss}, val loss {validation_loss}')
                ckpt_manager.save()

            # Showing epoch information and ending training if exhausted patience
            epoch_time = time.time() - epoch_start
            epoch_loss = epoch_loss / steps_per_epoch
            print(f'epoch: {epoch}, time: {epoch_time}, training loss: {epoch_loss}, val loss: {validation_loss}')
            if num_epochs_worse >= patience:
                print(f'early stopping on epoch {epoch}')
                break
        ckpt.restore(ckpt_manager.latest_checkpoint)




        # for epoch in range(1, max_epochs + 1):
        #     epoch_start = time.time()
        #     # epoch_loss = 0
        #     train_loss.reset_states()
        #     train_accuracy.reset_states()

        #     for (train_batch, (inp, tar)) in enumerate(train_dataset.take(steps_per_epoch)):
        #         train_step(inp, tar)
        #         # epoch_loss += train_loss.result()
        #         if train_batch % 100 == 0:
        #             print(f'Finished batch {train_batch} of epoch {epoch}', flush=True)
        #     training_loss = train_loss.result()
            
            
        #     # Validation and early stopping
        #     train_loss.reset_states()
        #     train_accuracy.reset_states()
        #     # validation_loss = 0
        #     NUM_VAL_BATCHES = dataset.get_validation_size() // batch_size
        #     print('trying to take', dataset.get_validation_size(), 'from validation set')
        #     for (batch, (source, target)) in enumerate(val_dataset.take(dataset.get_validation_size())):
        #         print('in validation loop taking a step')
        #         validation_step(source, target)
        #         # validation_loss += train_loss.result()
        #     validation_loss = train_loss.result()
        #     print('validation loss is', validation_loss, 'and num_val_batches is', NUM_VAL_BATCHES)
        #     # TODO: took this out to get it on same scale as training (I think per epoch rather than per batch), work out a better way later
        #     # validation_loss /= NUM_VAL_BATCHES
        #     validation_loss = validation_loss.numpy()
        #     training_loss = training_loss.numpy()
        #     self._loss_tracker['training_losses'].append(training_loss)
        #     self._loss_tracker['validation_losses'].append(validation_loss)

        #     file.write(f'Epoch: {epoch}\nTrain loss: {training_loss}\nVal loss: {validation_loss}\n\n')
        #     file.flush()
            
        #     if validation_loss >= best_validation_loss:
        #         num_epochs_worse += 1
        #     else:
        #         num_epochs_worse = 0
        #         best_validation_loss = validation_loss

        #         print(f'train: save model,epoch {epoch}, train loss {training_loss}, val loss {validation_loss}')
        #         # loss_tracker.append((epoch, training_loss, validation_loss))
        #         ckpt_manager.save()

        #     # Showing epoch information and ending training if exhausted patience
        #     epoch_time = time.time() - epoch_start
        #     print(f'epoch: {epoch}, time: {epoch_time}, training loss: {training_loss}, val loss: {validation_loss}')
        #     if num_epochs_worse >= patience:
        #         print(f'early stopping on epoch {epoch}')
        #         break
        
        # file.close()
        # with open('./training_losses.txt', 'w') as file:
        #     file.write('Training\n' + ','.join([str(loss) for loss in self._loss_tracker['training_losses']]) + '\n\n')
        #     file.write('Val\n' + ','.join([str(loss) for loss in self._loss_tracker['validation_losses']]))



    # def evaluate(self, sentence, dataset, settings, metric='bleu'):
    #     file = open('./evaluation_test.txt', 'w')
    #     _, _, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
    #     # file.write(test_dataset)
    #     # file.write('\n')
    #     attention_plot = np.zeros((dataset.get_target_vocab_size(), dataset.get_source_vocab_size()))
    #     result = []
    #     start_token = [dataset.piece_to_id(START_TOKEN, source=False)]
    #     decoder_input = start_token
    #     output = tf.expand_dims(decoder_input, 0)

    #     first_previous = None
    #     second_previous = None

    #     for _ in range(dataset.get_target_vocab_size()):
    #         enc_padding_mask, combined_mask, dec_padding_mask = create_masks(sentence, output)
    #         predictions, attention_weights = self._transformer(sentence, output, False,
    #                                                         enc_padding_mask, combined_mask,
    #                                                         dec_padding_mask)

    #         # select the last word from the seq_len dimension
    #         predictions = predictions[:, -1:, :] # shape is (batch_size, 1, vocab_size)
    #         predicted_id = tf.argmax(predictions[0][0]).numpy()

    #         current = dataset.id_to_piece(int(predicted_id), source=False)
    #         result.append(current)

    #         current_output = dataset.decode_pieces(result, source=False)
    #         last = current_output.split(' ')[-1]
    #         file.write(f'{output}, {current}, {result}, {current_output} {last}\n')
    #         if last == END_TOKEN:
    #             source_sentence = dataset.indices_to_language(sentence)
    #             result = dataset.decode_pieces(result, source=False)
    #             file.write('reached end token\n')
    #             return result, source_sentence, attention_plot

    #         second_previous = first_previous
    #         first_previous = current
    #         output = tf.concat([output, [[predicted_id]]], axis=-1)
    #     source_sentence = dataset.indices_to_language(sentence)
    #     result = dataset.decode_pieces(result, source=False)
    #     file.write(f'ending with result {result} from source {source_sentence}')
    #     file.close()
    #     return result, source_sentence, attention_plot

    def evaluate(self, sentence, dataset, settings, metric='bleu'):
        # attention_plot = np.zeros((MAX_LENGTH_TARGET, MAX_LENGTH_INPUT))
        result = ''
        start_token = [dataset.get_start_idx(source=False)]
        decoder_input = start_token
        output = tf.expand_dims(decoder_input, 0)


        MAX_LENGTH_TARGET = dataset.get_target_vocab_size() # TODO: this is not correct; go fix
        for _ in range(MAX_LENGTH_TARGET):
            enc_padding_mask, combined_mask, dec_padding_mask = create_masks(sentence, output)
            predictions, attention_weights = self._transformer(sentence, output, False,
                                                        enc_padding_mask, combined_mask,
                                                        dec_padding_mask)

            # select the last word from the seq_len dimension
            predictions = predictions[:, -1:, :] # shape is (batch_size, 1, vocab_size)
            predicted_id = tf.argmax(predictions[0][0]).numpy()

            current = dataset.idx_to_word(int(predicted_id), source=False)
            result += current + ' '

            if current == END_TOKEN:
                source_sentence = dataset.sequences_to_texts(sentence)
                return result, source_sentence, None
                # return result, source_sentence, attention_plot

            output = tf.concat([output, [[predicted_id]]], axis=-1)

        source_sentence = dataset.sequences_to_texts(sentence)
        return result, source_sentence, attention_weights

    def infer(self, dataset, settings, source_text):
        sentences = dataset.texts_to_sequences(source_text)
        translated = []
        for sentence in sentences:
            sentence = np.expand_dims(sentence, axis=0)
            result, sentence, _ = self.evaluate(sentence, dataset, settings)
            result = dataset.sequences_to_texts(result, source=False)
            if result[-1] == END_TOKEN:
                result = ' '.join(result.split())
            translated.append((sentence, result))
        return translated

    def translate(self, sentence, target, dataset, settings):
        
        result, sentence, attention_plot = self.evaluate(sentence, dataset, settings)
        target = dataset.sequences_to_texts(target, source=False)
        if result.split()[-1] == END_TOKEN:
            result = ' '.join(result.split())
        return sentence, target, result

    # def post_process_sentence(sentence):
    #     sentence = [word if word != ',' else '<COMMA>' for word in sentence.split()]
    #     if sentence[0] == START_TOKEN:
    #         sentence = sentence[1:]
    #     try:
    #         sentence = sentence[:sentence.index(END_TOKEN)]
    #     except ValueError:
    #         pass
    #     return sentence
    def post_process_sentence(self, sentence):
        sentence = [word if word != ',' else '<COMMA>' for word in sentence.split()]
        if sentence[0] == START_TOKEN:
            sentence = sentence[1:]
        try:
            sentence = sentence[:sentence.index(END_TOKEN)]
        except ValueError:
            pass
        return sentence

    def test_bleu(self, dataset, settings):
        """ Calculate test BLEU for main and (if relevant) auxiliary task/s. Write to LOG_FILE.
        Parameters:
            amount_of_training (str): '' for fully trained, '(no training) ' for untrained model, and
                                    '(pretrain only) ' for model trained only on auxiliary task.
        """
        _, _, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
        references = []
        hypotheses = []
        for (num, (source_sentence, target_sentence)) in enumerate(test_dataset):
            source_sentence = np.expand_dims(source_sentence, axis=0)
            target_sentence = np.expand_dims(target_sentence, axis=0)
            inp, target, hypothesis = self.translate(source_sentence, target_sentence, dataset, settings)
            inp, target = inp[0], target[0]
            
            inp = ' '.join(self.post_process_sentence(inp))

            target = self.post_process_sentence(target)
            references.append([target])
            target = ' '.join(target)

            hypothesis = self.post_process_sentence(hypothesis)
            hypotheses.append(hypothesis)
            hypothesis = ' '.join(hypothesis)

            if num % 10 == 0:
                print(f'input, {inp}, target, {target}, predicted, {hypothesis}')
        # test_bleu_score = corpus_bleu(references, hypotheses)
        # print(f'Test BLEU,{test_bleu_score}')

# # from ._model_helpers import Transformer, CustomSchedule, create_masks
# from ._model_helpers import Transformer
# from ._exceptions import InvalidGraphError
# import tensorflow as tf
# import numpy as np
# from .constants import START_TOKEN, END_TOKEN
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import time

# class AbstractModel:
#     """An interface to be implemented by all custom models. """
#     def construct(self, network_graph, settings):
#         raise NotImplementedError('Models must implement a construct method.')
    
#     def fit(self, training_data, validation_data, hyperparameters):
#         raise NotImplementedError('Models must implement a fit method')
    
#     def evaluate(self, test_data, metric='bleu'):
#         raise NotImplementedError('Models must implement an evaluate method')

#     def infer(self, source_text):
#         raise NotImplementedError('Models must implement an infer method')

# # class GenericModel(AbstractModel):
# #     def construct(self, network_graph, settings):
# #         nodes = network_graph.get_nodes()
# #         edges = network_graph.get_edges()
        


# class TransformerModel(AbstractModel):
#     def construct(self, network_graph, settings):
#         nodes = network_graph.get_nodes() # TODO: make this a nicer deconstruction of graph
        
#         for node in nodes:
#             node_name = node.get_name()
#             if node_name == 'input':
#                 input_size = node.get_size()
#             elif node_name == 'output':
#                 output_size = node.get_size()
#             elif node_name == 'transformer':
#                 node_info = node.get_info()
#                 num_layers = node_info['num_layers']
#                 d_model = node_info['d_model']
#                 num_heads = node_info['num_heads']
#                 dff = node_info['dff']
#                 # input_size = node_info['input_size']
#                 # output_size = node_info['output_size']
#                 dropout = node_info['dropout']

#                 # TODO: make this changeable in modal
#                 # max_sequence_length = node_info.get('max_sequence_length', 256)
#                 # num_layers, d_model, num_heads, dff, dropout = node.get_info()
#             else:
#                 raise InvalidGraphError('This transformer model has a non input or output or transformer node')
        
#         # self._transformer = Transformer(input_size, output_size, max_sequence_length, d_model, dff, num_heads)
#         self._transformer = Transformer(num_layers, d_model, num_heads, dff, input_size, output_size, dropout)
#         self._optimizer = self._get_optimizer(settings)
#         self._loss_object = self._get_loss_object(settings)
#         self._loss_tracker = {'training_losses': [], 'validation_losses': []}

#         print('optimizer is', self._optimizer)
#         print('model has', num_layers, d_model, num_heads, dff, input_size, output_size, dropout)

#     def fit(self, training_data, validation_data=None, num_epochs=50):
#         """ Train the model on the given dataset using the given settings.
        
#         Parameters:
#             dataset: a Dataset object containing the training and validation data.
#             settings: a dictionary of training settings and hyperparameters.
#         """
#         self._transformer.compile("rmsprop", "sparse_categorical_crossentropy", ["accuracy"])

        

#         # training_data = dataset.get_training_data()
#         # validation_data = dataset.get_validation_data()
#         # train_loss = tf.keras.metrics.Mean(name='train_loss')
#         # train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

#         # num_epochs = settings.get('num_epochs', 10)
#         # batch_size = settings.get('batch_size', 64)

#         self._transformer.fit(training_data, epochs=num_epochs, validation_dataset=validation_data)

#     # def load_existing_model(self, checkpoint_dir):
#     #     # Assume constructed
#     #     ckpt = tf.train.Checkpoint(transformer=self._transformer, optimizer=self._optimizer)
#     #     latest = tf.train.latest_checkpoint(checkpoint_dir)
#     #     ckpt.restore(latest)
#     #     print('loaded')

#     # def _get_optimizer(self, settings):
#     #     """ Construct the optimizer object from the requested optimizer
#     #         information in settings. Defaults to Adam optimizer.
        
#     #     Parameters:
#     #         settings: dictionary of training settings and hyperparameters.
        
#     #     Pre-conditions:
#     #         settings must contain the appropriate hyperparameters for the
#     #         optimizer requested.
#     #     """
#     #     optimizer_type = settings.get('optimizer', 'Adam')
#     #     learning_rate = settings.get('lr', 0.3)

#     #     # TODO: take this out or make optional!
#     #     learning_rate = CustomSchedule(self._transformer.get_dim_model())

#     #     if optimizer_type == 'Adam':
#     #         return tf.keras.optimizers.Adam(
#     #             learning_rate,
#     #             beta_1=settings.get('beta1'),
#     #             beta_2=settings.get('beta2'),
#     #             epsilon=settings.get('epsilon')
#     #         )
#     #     elif optimizer_type == 'RMSProp':
#     #         return tf.keras.optimizers.RMSprop(
#     #             learning_rate=learning_rate,
#     #             rho=settings.get('rho'),
#     #             momentum=settings.get('momentum'),
#     #             epsilon=settings.get('epsilon'),
#     #             centered=(settings.get('centered') == 'true'), name='RMSprop')
#     #     elif optimizer_type == 'Adagrad':
#     #         return tf.keras.optimizers.Adagrad(
#     #             learning_rate=learning_rate,
#     #             initial_accumulator_value=settings.get('initial_accum'),
#     #             epsilon=settings.get('epsilon'),
#     #             name='Adagrad')
#     #     elif optimizer_type == 'Adadelta':
#     #         return tf.keras.optimizers.Adadelta(
#     #             learning_rate=learning_rate,
#     #             rho=settings.get('rho'),
#     #             epsilon=settings.get('epsilon'),
#     #             name='Adadelta')
#     #     elif optimizer_type == 'sgd':
#     #         return tf.keras.optimizers.SGD(
#     #             learning_rate=learning_rate,
#     #             momentum=settings.get('momentum'),
#     #             nesterov=(settings.get('nesterov', 'false') == 'true'),
#     #             name='SGD')

#     # def loss_function(self, real, pred):
#     #     mask = tf.math.logical_not(tf.math.equal(real, 0))
#     #     loss_ = self._loss_object(real, pred)

#     #     mask = tf.cast(mask, dtype=loss_.dtype)
#     #     loss_ *= mask

#     #     return tf.reduce_mean(loss_)
    
#     # def get_loss_tracker(self):
#     #     return self._loss_tracker

#     # def _get_loss_object(self, settings):
#     #     """ Construct the loss object based on the requested loss to use.
        
#     #         Currently, only supports sparse categorical cross entropy.
#     #     """
#     #     return tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')


#     # def fit(self, dataset: 'Dataset', settings):
#     #     train_loss = tf.keras.metrics.Mean(name='train_loss')
#     #     train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

#     #     @tf.function
#     #     def train_step(inp, tar):
#     #         tar_inp, tar_real = tar[:, :-1], tar[:, 1:]
#     #         enc_padding_mask, combined_mask, dec_padding_mask = create_masks(inp, tar_inp)

#     #         with tf.GradientTape() as tape:
#     #             predictions, _ = self._transformer(inp, tar_inp, True, enc_padding_mask, combined_mask,
#     #                                         dec_padding_mask)
#     #             loss = self.loss_function(tar_real, predictions)

#     #         gradients = tape.gradient(loss, self._transformer.trainable_variables)
#     #         self._optimizer.apply_gradients(zip(gradients, self._transformer.trainable_variables))

#     #         train_loss(loss)
#     #         train_accuracy(tar_real, predictions)

#     #     @tf.function
#     #     def validation_step(inp, tar):
#     #         tar_inp, tar_real = tar[:,:-1], tar[:, 1:]
#     #         enc_padding_mask, combined_mask, dec_padding_mask = create_masks(inp, tar_inp)
#     #         predictions, _ = self._transformer(inp, tar_inp, True, enc_padding_mask, combined_mask,
#     #                                     dec_padding_mask)
#     #         loss = self.loss_function(tar_real, predictions)
#     #         train_loss(loss)
#     #         train_accuracy(tar_real, predictions)
        
#     #     # TODO: currently batch size needs to be very low with very limited data or
#     #     # there's an error; handle better / provide error message
#     #     train_dataset, val_dataset, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
#     #     buffer_size = dataset.get_training_size()
#     #     batch_size = dataset.get_batch_size()
#     #     steps_per_epoch = buffer_size // batch_size
#     #     max_epochs = settings.get('num_epochs', 5)

#     #     # file = open('training_losses.txt', 'w')

#     #     num_epochs_worse = 0
#     #     best_validation_loss = float('inf')
#     #     checkpoint_path = './checkpoints/train'
#     #     ckpt = tf.train.Checkpoint(transformer=self._transformer, optimizer=self._optimizer)
#     #     patience = settings.get('patience', 3)
#     #     ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=patience + 1)

#     #     # TODO: currently batch size needs to be very low with very limited data or
#     #     # there's an error; handle better / provide error message
#     #     train_dataset, val_dataset, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
#     #     buffer_size = dataset.get_training_size()
#     #     batch_size = dataset.get_batch_size()
#     #     steps_per_epoch = buffer_size // batch_size
#     #     max_epochs = settings.get('num_epochs', 5)

#     #     file = open('training_losses.txt', 'w')

#     #     for epoch in range(1, max_epochs + 1):
#     #         epoch_start = time.time()
#     #         epoch_loss = 0
#     #         train_loss.reset_states()
#     #         train_accuracy.reset_states()

#     #         for (train_batch, (inp, tar)) in enumerate(train_dataset.take(steps_per_epoch)):
#     #             train_step(inp, tar)
#     #             epoch_loss += train_loss.result()
#     #             if train_batch % 100 == 0:
#     #                 print(f'Finished batch {train_batch} of epoch {epoch}', flush=True)
#     #         training_loss = train_loss.result()
            
            
#     #         # Validation and early stopping
#     #         # train_loss.reset_states()
#     #         # train_accuracy.reset_states()
#     #         validation_loss = 0
#     #         NUM_VAL_BATCHES = dataset.get_validation_size() // batch_size
#     #         for (batch, (source, target)) in enumerate(val_dataset.take(dataset.get_validation_size())):
#     #             validation_step(source, target)
#     #             validation_loss += train_loss.result()
#     #         # validation_loss = train_loss.result()
#     #         print('validation loss is', validation_loss, 'and num_val_batches is', NUM_VAL_BATCHES)
#     #         # TODO: took this out to get it on same scale as training (I think per epoch rather than per batch), work out a better way later
#     #         # validation_loss /= NUM_VAL_BATCHES
#     #         # validation_loss = validation_loss.numpy()
#     #         training_loss = training_loss.numpy()
#     #         self._loss_tracker['training_losses'].append(training_loss)
#     #         self._loss_tracker['validation_losses'].append(validation_loss)

#     #         # file.write(f'Epoch: {epoch}\nTrain loss: {training_loss}\nVal loss: {validation_loss}\n\n')
#     #         # file.flush()
            
#     #         if validation_loss >= best_validation_loss:
#     #             num_epochs_worse += 1
#     #         else:
#     #             num_epochs_worse = 0
#     #             best_validation_loss = validation_loss

#     #             validation_loss /= NUM_VAL_BATCHES
#     #             training_loss = epoch_loss / (train_batch + 1)
#     #             print(f'train: save model,epoch {epoch}, train loss {training_loss}, val loss {validation_loss}')
#     #             ckpt_manager.save()

#     #         # Showing epoch information and ending training if exhausted patience
#     #         epoch_time = time.time() - epoch_start
#     #         epoch_loss = epoch_loss / steps_per_epoch
#     #         print(f'epoch: {epoch}, time: {epoch_time}, training loss: {epoch_loss}, val loss: {validation_loss}')
#     #         if num_epochs_worse >= patience:
#     #             print(f'early stopping on epoch {epoch}')
#     #             break
#     #     ckpt.restore(ckpt_manager.latest_checkpoint)




#         # for epoch in range(1, max_epochs + 1):
#         #     epoch_start = time.time()
#         #     # epoch_loss = 0
#         #     train_loss.reset_states()
#         #     train_accuracy.reset_states()

#         #     for (train_batch, (inp, tar)) in enumerate(train_dataset.take(steps_per_epoch)):
#         #         train_step(inp, tar)
#         #         # epoch_loss += train_loss.result()
#         #         if train_batch % 100 == 0:
#         #             print(f'Finished batch {train_batch} of epoch {epoch}', flush=True)
#         #     training_loss = train_loss.result()
            
            
#         #     # Validation and early stopping
#         #     train_loss.reset_states()
#         #     train_accuracy.reset_states()
#         #     # validation_loss = 0
#         #     NUM_VAL_BATCHES = dataset.get_validation_size() // batch_size
#         #     print('trying to take', dataset.get_validation_size(), 'from validation set')
#         #     for (batch, (source, target)) in enumerate(val_dataset.take(dataset.get_validation_size())):
#         #         print('in validation loop taking a step')
#         #         validation_step(source, target)
#         #         # validation_loss += train_loss.result()
#         #     validation_loss = train_loss.result()
#         #     print('validation loss is', validation_loss, 'and num_val_batches is', NUM_VAL_BATCHES)
#         #     # TODO: took this out to get it on same scale as training (I think per epoch rather than per batch), work out a better way later
#         #     # validation_loss /= NUM_VAL_BATCHES
#         #     validation_loss = validation_loss.numpy()
#         #     training_loss = training_loss.numpy()
#         #     self._loss_tracker['training_losses'].append(training_loss)
#         #     self._loss_tracker['validation_losses'].append(validation_loss)

#         #     file.write(f'Epoch: {epoch}\nTrain loss: {training_loss}\nVal loss: {validation_loss}\n\n')
#         #     file.flush()
            
#         #     if validation_loss >= best_validation_loss:
#         #         num_epochs_worse += 1
#         #     else:
#         #         num_epochs_worse = 0
#         #         best_validation_loss = validation_loss

#         #         print(f'train: save model,epoch {epoch}, train loss {training_loss}, val loss {validation_loss}')
#         #         # loss_tracker.append((epoch, training_loss, validation_loss))
#         #         ckpt_manager.save()

#         #     # Showing epoch information and ending training if exhausted patience
#         #     epoch_time = time.time() - epoch_start
#         #     print(f'epoch: {epoch}, time: {epoch_time}, training loss: {training_loss}, val loss: {validation_loss}')
#         #     if num_epochs_worse >= patience:
#         #         print(f'early stopping on epoch {epoch}')
#         #         break
        
#         # file.close()
#         # with open('./training_losses.txt', 'w') as file:
#         #     file.write('Training\n' + ','.join([str(loss) for loss in self._loss_tracker['training_losses']]) + '\n\n')
#         #     file.write('Val\n' + ','.join([str(loss) for loss in self._loss_tracker['validation_losses']]))



#     # def evaluate(self, sentence, dataset, settings, metric='bleu'):
#     #     file = open('./evaluation_test.txt', 'w')
#     #     _, _, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
#     #     # file.write(test_dataset)
#     #     # file.write('\n')
#     #     attention_plot = np.zeros((dataset.get_target_vocab_size(), dataset.get_source_vocab_size()))
#     #     result = []
#     #     start_token = [dataset.piece_to_id(START_TOKEN, source=False)]
#     #     decoder_input = start_token
#     #     output = tf.expand_dims(decoder_input, 0)

#     #     first_previous = None
#     #     second_previous = None

#     #     for _ in range(dataset.get_target_vocab_size()):
#     #         enc_padding_mask, combined_mask, dec_padding_mask = create_masks(sentence, output)
#     #         predictions, attention_weights = self._transformer(sentence, output, False,
#     #                                                         enc_padding_mask, combined_mask,
#     #                                                         dec_padding_mask)

#     #         # select the last word from the seq_len dimension
#     #         predictions = predictions[:, -1:, :] # shape is (batch_size, 1, vocab_size)
#     #         predicted_id = tf.argmax(predictions[0][0]).numpy()

#     #         current = dataset.id_to_piece(int(predicted_id), source=False)
#     #         result.append(current)

#     #         current_output = dataset.decode_pieces(result, source=False)
#     #         last = current_output.split(' ')[-1]
#     #         file.write(f'{output}, {current}, {result}, {current_output} {last}\n')
#     #         if last == END_TOKEN:
#     #             source_sentence = dataset.indices_to_language(sentence)
#     #             result = dataset.decode_pieces(result, source=False)
#     #             file.write('reached end token\n')
#     #             return result, source_sentence, attention_plot

#     #         second_previous = first_previous
#     #         first_previous = current
#     #         output = tf.concat([output, [[predicted_id]]], axis=-1)
#     #     source_sentence = dataset.indices_to_language(sentence)
#     #     result = dataset.decode_pieces(result, source=False)
#     #     file.write(f'ending with result {result} from source {source_sentence}')
#     #     file.close()
#     #     return result, source_sentence, attention_plot

#     def evaluate(self, sentence, dataset, settings, metric='bleu'):
#         # attention_plot = np.zeros((MAX_LENGTH_TARGET, MAX_LENGTH_INPUT))
#         result = ''
#         start_token = [dataset.get_start_idx(source=False)]
#         decoder_input = start_token
#         output = tf.expand_dims(decoder_input, 0)


#         MAX_LENGTH_TARGET = dataset.get_target_vocab_size() # TODO: this is not correct; go fix
#         for _ in range(MAX_LENGTH_TARGET):
#             enc_padding_mask, combined_mask, dec_padding_mask = create_masks(sentence, output)
#             predictions, attention_weights = self._transformer(sentence, output, False,
#                                                         enc_padding_mask, combined_mask,
#                                                         dec_padding_mask)

#             # select the last word from the seq_len dimension
#             predictions = predictions[:, -1:, :] # shape is (batch_size, 1, vocab_size)
#             predicted_id = tf.argmax(predictions[0][0]).numpy()

#             current = dataset.idx_to_word(int(predicted_id), source=False)
#             result += current + ' '

#             if current == END_TOKEN:
#                 source_sentence = dataset.sequences_to_texts(sentence)
#                 return result, source_sentence, None
#                 # return result, source_sentence, attention_plot

#             output = tf.concat([output, [[predicted_id]]], axis=-1)

#         source_sentence = dataset.sequences_to_texts(sentence)
#         return result, source_sentence, attention_weights

#     def infer(self, dataset, settings, source_text):
#         sentences = dataset.texts_to_sequences(source_text)
#         translated = []
#         for sentence in sentences:
#             sentence = np.expand_dims(sentence, axis=0)
#             result, sentence, _ = self.evaluate(sentence, dataset, settings)
#             result = dataset.sequences_to_texts(result, source=False)
#             if result[-1] == END_TOKEN:
#                 result = ' '.join(result.split())
#             translated.append((sentence, result))
#         return translated

#     def translate(self, sentence, target, dataset, settings):
        
#         result, sentence, attention_plot = self.evaluate(sentence, dataset, settings)
#         target = dataset.sequences_to_texts(target, source=False)
#         if result.split()[-1] == END_TOKEN:
#             result = ' '.join(result.split())
#         return sentence, target, result

#     # def post_process_sentence(sentence):
#     #     sentence = [word if word != ',' else '<COMMA>' for word in sentence.split()]
#     #     if sentence[0] == START_TOKEN:
#     #         sentence = sentence[1:]
#     #     try:
#     #         sentence = sentence[:sentence.index(END_TOKEN)]
#     #     except ValueError:
#     #         pass
#     #     return sentence
#     def post_process_sentence(self, sentence):
#         sentence = [word if word != ',' else '<COMMA>' for word in sentence.split()]
#         if sentence[0] == START_TOKEN:
#             sentence = sentence[1:]
#         try:
#             sentence = sentence[:sentence.index(END_TOKEN)]
#         except ValueError:
#             pass
#         return sentence

#     def test_bleu(self, dataset, settings):
#         """ Calculate test BLEU for main and (if relevant) auxiliary task/s. Write to LOG_FILE.

#         Parameters:
#             amount_of_training (str): '' for fully trained, '(no training) ' for untrained model, and
#                                     '(pretrain only) ' for model trained only on auxiliary task.
#         """
#         _, _, test_dataset = dataset.batch(batch_size=settings.get('batch_size'))
#         references = []
#         hypotheses = []
#         for (num, (source_sentence, target_sentence)) in enumerate(test_dataset):
#             source_sentence = np.expand_dims(source_sentence, axis=0)
#             target_sentence = np.expand_dims(target_sentence, axis=0)
#             inp, target, hypothesis = self.translate(source_sentence, target_sentence, dataset, settings)
#             inp, target = inp[0], target[0]
            
#             inp = ' '.join(self.post_process_sentence(inp))

#             target = self.post_process_sentence(target)
#             references.append([target])
#             target = ' '.join(target)

#             hypothesis = self.post_process_sentence(hypothesis)
#             hypotheses.append(hypothesis)
#             hypothesis = ' '.join(hypothesis)

#             if num % 10 == 0:
#                 print(f'input, {inp}, target, {target}, predicted, {hypothesis}')
#         # test_bleu_score = corpus_bleu(references, hypotheses)
#         # print(f'Test BLEU,{test_bleu_score}')
