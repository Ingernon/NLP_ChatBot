import os
import string
import yaml

DATA_PATH = './data/'


class QandA_data():
	def __init__(self):
		self.questions = list()
		self.answers = list()
		self.init_data()

	def init_data(self):
		ls = os.listdir(DATA_PATH + os.sep)
		for filepath in ls:
			file = open( DATA_PATH + os.sep + filepath , 'rb')
			text = yaml.safe_load(file)
			conversations = text['conversations']
			for con in conversations:
				if type( con ) == str and len( con ) > 2 :
					replies = con[1:]
					for rep in replies:
						self.questions.append(str(con[0].lower()).translate(str.maketrans('', '', string.punctuation)))
						self.answers.append('<START> '+str(rep.lower()).translate(str.maketrans('', '', string.punctuation))+' <END>')
				elif type( con ) == str and len(con)> 1:
					self.questions.append(str(con[0].lower()).translate(str.maketrans('', '', string.punctuation)))
					self.answers.append('<START> '+str(con[1]).lower().translate(str.maketrans('', '', string.punctuation))+' <END>')

	def get_data(self):
		if len(self.answers) == len(self.questions):
			return self.questions, self.answers
		print("ERROR QandA")
		return None, None

if __name__ == "__main__":
	qanda = QandA_data()
	print(len(qanda.answers))
