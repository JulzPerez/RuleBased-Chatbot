import json
import re
import random


data_file = open('data.json').read()
intents_json = json.loads(data_file)
#rules_dict = {1:re.compile("[A-Za-z\s?!\.]*[H|hello][A-Za-z\s?!\.]")}

def loadRules():
    myFile = open('rules.txt','r')
    rLine = myFile.readlines()
    rules_dict = {}
    x=1
    for line in rLine:
        regex, tag = line.split()

        rules_dict[x] = {'regex': regex, 'tag': tag}
        x=x+1

    return (rules_dict) 

def getTag(msg): 
    rules = loadRules()
    i=1
    for i in rules.keys():
        if re.match(rules[i]['regex'],msg):
            tag=(rules[i]['tag'])
            break
        
    return tag

def getResponse(msg):
    tag = getTag(msg)
    result = msg
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
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