import json
import re


data_file = open('data.json').read()
intents_json = json.loads(data_file)
rules=json.load(open('regexList.json').read())

def getTag(msg): 
    rules_list=rules['patterns']
    for j in rules_list:
        if re.search(j['regex'],msg):
            tag = j['tag']
            break
    #tag = re.sub(r"([A-Za-z\s?!\.]*[H|hello][A-Za-z\s?!\.])","greeting", msg)
    return tag

def getResponse(msg):
    tag = getTag(msg)
    result = msg
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = i['responses']
            break
    return result

def chatbot_response(msg):
    res = getResponse(msg)
    return res

from flask import Flask, render_template, request
app = Flask(__name__)
#app.static_folder = 'static'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getResponse")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

#if __name__ == "__main__":
#    app.run()