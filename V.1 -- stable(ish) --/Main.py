import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras import preprocessing , utils
import QandA_data
from Custom_keras_Encoder_Decoder import Encoder_Decoder, load_Encoder_Decoder
import Encoder_Decoder_for_dummies
import Preprocess

qanda = QandA_data.QandA_data()
questions, answers = qanda.get_data()

preprocess = Preprocess.Preprocess(questions, answers)


def str_to_tokens(sentence : str):
	words = sentence.lower().split()
	tokens_list = list()
	for word in words:
		if word in preprocess.que_word_dict:
			tokens_list.append(preprocess.que_word_dict[word]) 
	return preprocessing.sequence.pad_sequences( [tokens_list] , maxlen=preprocess.max_input_length , padding='post')

ed = Encoder_Decoder_for_dummies.ED_dummies(preprocess)

#ed.train(epochs=500)
#ed.save("saves")
ed.load("saves")

enc_model , dec_model = ed.get_enc_dec()
#for epoch in questions:
while True:
	states_values = enc_model.predict(str_to_tokens(input('->')))
	empty_target_seq = np.zeros( ( 1 , 1 ) )
	empty_target_seq[0, 0] = preprocess.ans_word_dict['start']
	stop_condition = False
	decoded_translation = ''
	while not stop_condition :
		dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + states_values )
		sampled_word_index = np.argmax(dec_outputs[0, -1, :])
		sampled_word = None
		for word , index in preprocess.ans_word_dict.items() :
			if sampled_word_index == index :
				decoded_translation += ' {}'.format(word)
				sampled_word = word

		if sampled_word == 'end' or len(decoded_translation.split()) > preprocess.max_output_length:
			stop_condition = True

		empty_target_seq = np.zeros( ( 1 , 1 ) )  
		empty_target_seq[ 0 , 0 ] = sampled_word_index
		states_values = [ h , c ] 

	print("<-",decoded_translation[:-4],"\n" )