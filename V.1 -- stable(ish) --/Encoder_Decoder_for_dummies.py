import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from Custom_keras_Encoder_Decoder import Encoder_Decoder, load_Encoder_Decoder


class ED_dummies():
	def __init__(self, preproces):
		self.preprocess = preproces
		self.ed = Encoder_Decoder()
		self.enc_model = None
		self.dec_model = None

	def train(self, epochs=100):
		self.ed.define_model(self.preprocess.num_que_tokens, self.preprocess.num_ans_tokens)
		self.ed.train([self.preprocess.encoder_input_data , self.preprocess.decoder_input_data], self.preprocess.decoder_target_data, epochs=100)
		self.enc_model , self.dec_model = self.ed.make_inference_models()

	def save(self, name):
		self.enc_model.save("./"+name+"/enc.h5")
		self.dec_model.save("./"+name+"/dec.h5")

	def load(self, name):
		self.enc_model = tf.keras.models.load_model("./"+name+"/enc.h5")
		self.dec_model = tf.keras.models.load_model("./"+name+"/dec.h5")

	def get_enc_dec(self):
		if self.enc_model:
			return self.enc_model, self.dec_model
		print("please train or load me")
		return self.enc_model, self.dec_model

