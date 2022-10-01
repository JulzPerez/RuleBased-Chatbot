from flask import Flask, render_template, request
import json

data_file = open('data.json').read()
intents = json.loads(data_file)


def getResponse(msg):
    """ tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break """
    return msg

def chatbot_response(msg):
    res = getResponse(msg)
    return intents

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/getResponse")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)
