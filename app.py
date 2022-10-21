import json
import re
import random
import sys
from flask import Flask,render_template,request,session

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',
                  ENV='development')

data_file = open('data.json').read()
intents_json = json.loads(data_file)
current_client=""
current_msg_level=""

#read regex rules from files
def loadRules():
    myFile = open('rules.txt','r')
    rLine = myFile.readlines()
    rules_dict = {}
    x=1
    print(
        "current_client: ",session["current_client"],
        "\ncurrent_msg_level: ",session["current_msg_level"],
        "\n",file=sys.stderr)

    for line in rLine:
        if line.strip()=="" or "#" in line: #skip blank lines and comments
            continue

        regex, tag = line.split()
        
        if current_msg_level=="generic":
            if(("_first_" in tag and current_client in tag) or ("generic" in tag and current_client in tag)):
                rules_dict[x] = {'regex': regex, 'tag': tag}
            
            elif("generic" in tag):
                rules_dict[x] = {'regex': regex, 'tag': tag}
        
        elif current_msg_level=="first":
            if(("_second_" in tag and current_client in tag)("generic" in tag and current_client in tag)):
                rules_dict[x] = {'regex': regex, 'tag': tag}

        elif current_msg_level=="second":
            if(("_third_" in tag and current_client in tag)("generic" in tag and current_client in tag)):
                rules_dict[x] = {'regex': regex, 'tag': tag}


        x=x+1

    return (rules_dict) 

#get corresponding tag from triggered regex rule
def getTag(msg): 
    rules=loadRules() #will load Rules each time, optimize this 
    print("rules: ",rules,file=sys.stderr)
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
    print("tag: ",tag,"\nmessage:",msg,file=sys.stderr)
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getResponse")
def get_bot_response():
    userText = request.args.get('msg')        
    return chatbot_response(userText.lower())

@app.route("/setClient")
def set_client():
    if session.get('current_client'):
        if session['current_client']!="":
            return "already set"

    session['current_client'] = request.args.get('client')
    session['current_msg_level']='generic'
    
    return "ok"

@app.route("/clearSessions")
def clear_sessions():
    # session.pop('current_client', None)
    # session.pop('current_msg_level', None)
    session['current_client']=''
    session['current_msg_level'] = 'generic'
    return "ok"