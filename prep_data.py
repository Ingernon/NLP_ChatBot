import re
from nltk.corpus import stopwords
from read_xlsx import get_trivial
import nltk

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z-A-Z #+_]')
STOPWORDS = set(stopwords.words('english'))
MAX_SIZE = 100

def preprocess_data(trivial):
	for i in range(0, len(trivial[0])):
		trivial[2][i] = str(trivial[2][i]).replace(".0", "")
		trivial[1][i] = re.sub(REPLACE_BY_SPACE_RE, ' ', trivial[1][i])
		trivial[1][i] = re.sub(BAD_SYMBOLS_RE, '', trivial[1][i])
		trivial[1][i] = ' '.join(t for t in trivial[1][i].split() if t not in STOPWORDS)
		trivial[2][i] = re.sub(REPLACE_BY_SPACE_RE, ' ', trivial[2][i])
		trivial[2][i] = re.sub(BAD_SYMBOLS_RE, '', trivial[2][i])
		trivial[2][i] = ' '.join(t for t in trivial[2][i].split() if t not in STOPWORDS)
		trivial[1][i] = trivial[1][i].lower()
		trivial[2][i] = str(trivial[2][i]).lower()
	return trivial[1], trivial[2]

print(prep_data(get_trivial(["_", "\'", "&", "\"", ":", "(", ")"], [], MAX_SIZE)))