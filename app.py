import json
import re
import random


data_file = open('data.json').read()
intents_json = json.loads(data_file)

#read regex rules from files
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

#get corresponding tag from triggered regex rule
def getTag(msg): 
    rules=loadRules() #will load Rules each time, optimize this 
    intent = "" #will return empty string if no rule matched
    for i in rules.keys():
        pattern = rules[i]['regex']
        if(re.search(pattern,msg)):
            intent = rules[i]['tag']
            break
        
    return intent

#get response based on intent or tag (i.e. tag associated with user message)
def getResponse(msg):
    tag = getTag(msg)
    result = msg
    list_of_intents = intents_json['intents']
    if (tag == ""): #no rule matched, hence ask for clarification
        msg = ["Palihug isulat pag-usab ang imong pangutana ug dugangi ang mga detalye aron akong masabtan kini.", "Wala ko kasabot sa imong pangutana. Palihug ug dungag ug detalye."]
        result = random.choice(msg)
    else:
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
    return chatbot_response(userText.lower())

#if __name__ == "__main__":
#    app.run()