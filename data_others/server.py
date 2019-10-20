from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/bot')
def bot():
    text = request.args.get("text");
    # text => what the user sends

    # handle the AI
    
    return "Its answer"; # => what the bot answers

@app.route('/chat')
def chat():
    with open('./chatpage.html', 'r') as content_file:
        content = content_file.read()
        return content;

if __name__ == '__main__':
    app.run()
