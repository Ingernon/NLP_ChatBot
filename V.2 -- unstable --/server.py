from flask import Flask
from flask import request
from Bot import *
app = Flask(__name__)


@app.route('/bot')
def bot():
    text = request.args.get("text");
    # text => what the user sends

    # handle the AI
    ans = get_ans(text)
    print (ans)
    return  ans# => what the bot answers

@app.route('/chat')
def chat():
    with open('./chatpage.html', 'r') as content_file:
        content = content_file.read()
        return content;

if __name__ == '__main__':
	app.run(host='192.168.137.1', debug=True)
    #app.run()
