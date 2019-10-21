import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras import preprocessing , utils

class Preprocess():
	def __init__(self, questions, answers):
		tokenizer = preprocessing.text.Tokenizer()
		tokenizer.fit_on_texts(questions) 
		tokenized_questions = tokenizer.texts_to_sequences(questions) 
		length_list = list()
		for token_seq in tokenized_questions:
			length_list.append( len( token_seq ))
		self.max_input_length = np.array( length_list ).max()
		print( 'question max length is {}'.format( self.max_input_length ))

		padded_questions = preprocessing.sequence.pad_sequences( tokenized_questions , maxlen=self.max_input_length , padding='post' )
		self.encoder_input_data = np.array( padded_questions )
		print( 'Encoder input data shape -> {}'.format( self.encoder_input_data.shape ))

		self.que_word_dict = tokenizer.word_index
		#self.que_word_dict += {"<NOT>":len( self.que_word_dict )+1}
		self.num_que_tokens = len( self.que_word_dict )+1
		print( 'Number of question tokens = {}'.format( self.num_que_tokens))


		tokenizer = preprocessing.text.Tokenizer()
		tokenizer.fit_on_texts( answers ) 
		tokenized_answers = tokenizer.texts_to_sequences( answers ) 

		length_list = list()
		for token_seq in tokenized_answers:
			length_list.append( len( token_seq ))
		self.max_output_length = np.array( length_list ).max()
		print( 'answers max length is {}'.format( self.max_output_length ))

		padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=self.max_output_length, padding='post' )
		self.decoder_input_data = np.array( padded_answers )
		print( 'Decoder input data shape -> {}'.format( self.decoder_input_data.shape ))

		self.ans_word_dict = tokenizer.word_index
		self.num_ans_tokens = len( self.ans_word_dict )+1
		print( 'Number of answers tokens = {}'.format( self.num_ans_tokens))


		self.decoder_target_data = list()
		for token_seq in tokenized_answers:
			self.decoder_target_data.append( token_seq[ 1 : ] ) 
		padded_answers = preprocessing.sequence.pad_sequences( self.decoder_target_data , maxlen=self.max_output_length, padding='post' )
		onehot_answers = utils.to_categorical( padded_answers , self.num_ans_tokens )
		self.decoder_target_data = np.array( onehot_answers )
		print( 'Decoder target data shape -> {}'.format(self.decoder_target_data.shape))
		