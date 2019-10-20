import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras import layers , activations , models , preprocessing , utils
import pickle
import numpy as np
import tempfile

ED_DEBUG = True

def load_Encoder_Decoder(name="Encoder_Decoder.save"):
	ed = Encoder_Decoder()
	# ed = None
	# with open(name, 'rb') as f:
	# 	ed = dill.load(f)
	return ed

class E_D_saver():
	def __init__(self, decoder_lstm, decoder_dense):
		self.decoder_lstm = decoder_lstm
		self.decoder_dense = decoder_dense



class Encoder_Decoder():
	def __init__(self):
		self.model = None
		self.encoder_inputs = None
		self.encoder_states = None
		self.decoder_embedding = None
		self.decoder_inputs = None
		self.decoder_lstm = None
		self.decoder_dense = None
		self.trained = False

	def define_model(self, num_que_tokens, num_ans_tokens):
		self.encoder_inputs = tf.keras.layers.Input(shape=( None , ))
		encoder_embedding = tf.keras.layers.Embedding( num_que_tokens, 256 , mask_zero=True ) (self.encoder_inputs)
		encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 128 , return_state=True  )( encoder_embedding )
		self.encoder_states = [ state_h , state_c ]

		self.decoder_inputs = tf.keras.layers.Input(shape=( None ,  ))
		self.decoder_embedding = tf.keras.layers.Embedding( num_ans_tokens, 256 , mask_zero=True) (self.decoder_inputs)
		self.decoder_lstm = tf.keras.layers.LSTM( 128 , return_state=True , return_sequences=True)
		decoder_outputs , _ , _ = self.decoder_lstm ( self.decoder_embedding , initial_state=self.encoder_states )
		self.decoder_dense = tf.keras.layers.Dense( num_ans_tokens , activation=tf.keras.activations.softmax ) 
		output = self.decoder_dense ( decoder_outputs )
		self.model = tf.keras.models.Model([self.encoder_inputs, self.decoder_inputs], output )
		self.model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')
		if ED_DEBUG:
			self.model.summary()

	def train(self, x_train, y_train, epochs=100, batch_size=1000):
		if self.model:
			self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
			self.trained = True
		else:
			print("ERROR train use define_model")

	def make_inference_models(self):
		if not self.trained:
			print("ERROR model not trained")
			return None, None
		encoder_model = tf.keras.models.Model(self.encoder_inputs, self.encoder_states)
		decoder_state_input_h = tf.keras.layers.Input(shape=( 128 ,))
		decoder_state_input_c = tf.keras.layers.Input(shape=( 128 ,))
		decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
		decoder_outputs, state_h, state_c = self.decoder_lstm(self.decoder_embedding , initial_state=decoder_states_inputs)
		decoder_states = [state_h, state_c]
		decoder_outputs = self.decoder_dense(decoder_outputs)
		decoder_model = tf.keras.models.Model([self.decoder_inputs] + decoder_states_inputs,[decoder_outputs] + decoder_states)
		return encoder_model , decoder_model

	def save(self, name="Encoder_Decoder.save"):
		save_data = E_D_saver(self.decoder_lstm.get_weights(), self.decoder_dense.get_weights())
		with open(name, 'wb') as f:
			pickle.dump(save_data, f)
		if ED_DEBUG:
			print("model saved")

	def load(self,num_que_tokens, num_ans_tokens, name="Encoder_Decoder.save"):
		with open(name, 'rb') as f:
			save_data = pickle.load(f)
		print (save_data.decoder_dense.shape)
		self.encoder_inputs = tf.keras.layers.Input(shape=( None , ))
		encoder_embedding = tf.keras.layers.Embedding( num_que_tokens, 256 , mask_zero=True ) (self.encoder_inputs)
		encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 128 , return_state=True  )( encoder_embedding )
		self.encoder_states = [ state_h , state_c ]

		self.decoder_inputs = tf.keras.layers.Input(shape=( None ,  ))
		self.decoder_embedding = tf.keras.layers.Embedding( num_ans_tokens, 256 , mask_zero=True) (self.decoder_inputs)
		self.decoder_lstm = tf.keras.layers.LSTM( 128 , return_state=True , return_sequences=True)
		
		self.decoder_lstm.set_weights(save_data.decoder_lstm)
		
		decoder_outputs , _ , _ = self.decoder_lstm ( self.decoder_embedding , initial_state=self.encoder_states )
		self.decoder_dense = tf.keras.layers.Dense( num_ans_tokens , activation=tf.keras.activations.softmax ) 
		
		self.decoder_dense.set_weights(save_data.decoder_dense)
		
		output = self.decoder_dense ( decoder_outputs )
		self.model = tf.keras.models.Model([self.encoder_inputs, self.decoder_inputs], output )
		self.model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')


	def print(self):
		print(self.encoder_inputs)
		print(self.encoder_states)
		print(self.decoder_embedding)
		print(self.decoder_inputs)
		print(self.decoder_lstm.get_weights())
		print(self.decoder_dense.get_weights())

if __name__ == "__main__":
	import Main