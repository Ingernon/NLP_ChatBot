import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras import layers , activations , models , preprocessing , utils
import QandA_data
from Custom_keras_Encoder_Decoder import Encoder_Decoder, load_Encoder_Decoder

qanda = QandA_data.QandA_data()
questions, answers = qanda.get_data()


tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(questions) 
tokenized_questions = tokenizer.texts_to_sequences(questions) 

length_list = list()
for token_seq in tokenized_questions:
	length_list.append( len( token_seq ))
max_input_length = np.array( length_list ).max()
print( 'question max length is {}'.format( max_input_length ))

padded_questions = preprocessing.sequence.pad_sequences( tokenized_questions , maxlen=max_input_length , padding='post' )
encoder_input_data = np.array( padded_questions )
print( 'Encoder input data shape -> {}'.format( encoder_input_data.shape ))

que_word_dict = tokenizer.word_index
num_que_tokens = len( que_word_dict )+1
print( 'Number of question tokens = {}'.format( num_que_tokens))


tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts( answers ) 
tokenized_answers = tokenizer.texts_to_sequences( answers ) 

length_list = list()
for token_seq in tokenized_answers:
	length_list.append( len( token_seq ))
max_output_length = np.array( length_list ).max()
print( 'answers max length is {}'.format( max_output_length ))

padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=max_output_length, padding='post' )
decoder_input_data = np.array( padded_answers )
print( 'Decoder input data shape -> {}'.format( decoder_input_data.shape ))

ans_word_dict = tokenizer.word_index
num_ans_tokens = len( ans_word_dict )+1
print( 'Number of answers tokens = {}'.format( num_ans_tokens))


decoder_target_data = list()
for token_seq in tokenized_answers:
	decoder_target_data.append( token_seq[ 1 : ] ) 
padded_answers = preprocessing.sequence.pad_sequences( decoder_target_data , maxlen=max_output_length, padding='post' )
onehot_answers = utils.to_categorical( padded_answers , num_ans_tokens )
decoder_target_data = np.array( onehot_answers )
print( 'Decoder target data shape -> {}'.format(decoder_target_data.shape))

# ed = Encoder_Decoder()
# ed.define_model(num_que_tokens, num_ans_tokens)
# ed.train([encoder_input_data , decoder_input_data], decoder_target_data, 10)
# ed.save()
# ed.load(num_que_tokens, num_ans_tokens)


def str_to_tokens( sentence : str ):
	words = sentence.lower().split()
	tokens_list = list()
	for word in words:
		tokens_list.append( que_word_dict[ word ] ) 
	return preprocessing.sequence.pad_sequences( [tokens_list] , maxlen=max_input_length , padding='post')



# enc_model , dec_model = ed.make_inference_models()
# enc_model.save("./saves/enc.h5")
# dec_model.save("./saves/dec.h5")

enc_model = tf.keras.models.load_model("./saves/enc.h5")
dec_model = tf.keras.models.load_model("./saves/dec.h5")

for epoch in questions:
#while True:
	#states_values = enc_model.predict(str_to_tokens(input('->')))
	print("->"+epoch)
	states_values = enc_model.predict(str_to_tokens(epoch))
	empty_target_seq = np.zeros( ( 1 , 1 ) )
	empty_target_seq[0, 0] = ans_word_dict['start']
	stop_condition = False
	decoded_translation = ''
	while not stop_condition :
		dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + states_values )
		sampled_word_index = np.argmax( dec_outputs[0, -1, :] )
		sampled_word = None
		for word , index in ans_word_dict.items() :
			if sampled_word_index == index :
				decoded_translation += ' {}'.format( word )
				sampled_word = word

		if sampled_word == 'end' or len(decoded_translation.split()) > max_output_length:
			stop_condition = True

		empty_target_seq = np.zeros( ( 1 , 1 ) )  
		empty_target_seq[ 0 , 0 ] = sampled_word_index
		states_values = [ h , c ] 

	print("<-",decoded_translation,"\n" )