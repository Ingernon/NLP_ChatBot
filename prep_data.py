import re
from nltk.corpus import stopwords
from read_xlsx import get_trivial
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z-A-Z #+_]')
STOPWORDS = set(stopwords.words('english'))
MAX_SIZE = 100

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def preprocess_data(questions, answers):
	for i in range(0, len(questions)):
		answers[i] = str(answers[i]).replace(".0", "")
		questions[i] = re.sub(REPLACE_BY_SPACE_RE, ' ', questions[i])
		questions[i] = re.sub(BAD_SYMBOLS_RE, '', questions[i])
		questions[i] = ' '.join(t for t in questions[i].split() if t not in STOPWORDS)
		answers[i] = re.sub(REPLACE_BY_SPACE_RE, ' ', answers[i])
		answers[i] = re.sub(BAD_SYMBOLS_RE, '', answers[i])
		answers[i] = ' '.join(t for t in answers[i].split() if t not in STOPWORDS)
		questions[i] = questions[i].lower()
		answers[i] = str(answers[i]).lower()
	return questions, answers

# trivial = get_trivial(["_", "\'", "&", "\"", ":", "(", ")"], [], MAX_SIZE)
# questions, answers = preprocess_data(trivial[1], trivial[2])