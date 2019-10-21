import os
import string
import yaml

DATA_PATH = './interface/'

class QandA_data():
	def __init__(self):
		self.questions = list()
		self.answers = list()
		self.init_data()

	def init_data(self):
		with open(DATA_PATH+"dailylife.txt") as fp:
			for cnt, line in enumerate(fp):
				#print("Line {}: {}".format(cnt, line))
				if cnt % 2 == 1:
					self.questions.append(str(line.lower()).translate(str.maketrans('', '', string.punctuation)))
				else:
					self.answers.append(str(line).lower().translate(str.maketrans('', '', string.punctuation)))

	def get_data(self):
		if len(self.answers) == len(self.questions):
			return self.questions, self.answers
		print("ERROR QandA")
		return None, None

if __name__ == "__main__":
	qanda = QandA_data()
	print(qanda.answers[205])
	print(qanda.questions[205])
