import os,urllib.request,json
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
#import weatherfind

#Removing information for posting publicly 
account_sid = "ENTER ACCOUNT SID HERE"
auth_token = "ENTER AUTH TOKEN HERE"

client = Client(account_sid, auth_token)
app = Flask(__name__)
 
 
@app.route('/sms', methods=['POST'])

def sms(): #Takes in text messages received to the twilio number and replies accordinly
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()
    reply = str(message_body).lower()

    
    #I don't like making a huge if/elif wall but not sure how else to do this...
    if ((reply == "hi") or (reply== "hi ")):
        resp.message('Hello, {}!'.format(number))
        return str(resp)
                     
    elif ((reply == "bye") or (reply== "bye ")):
        resp.message('Goodbye, {}'.format(number))
        return str(resp)

    elif ((reply == "temperature") or (reply== "temperature ")):
        findweather()
        return str(resp)

    elif ((reply == "forecast morning") or (reply== "forecast morning ")):
        forecast(0,6)
        return str(resp)

    elif ((reply == "forecast evening") or (reply== "forecast evening ")):
        forecast(0,12)
        return str(resp)

    elif ((reply == "forecast tomorrow")or (reply== "forecast tomorrow ")):
        forecast(0,18)
        return str(resp)
    
    elif ((reply == "commands")or (reply== "commands ")):
        commandList()
        return str(resp)

    else:
        resp.message('Invalid command. For help, text "commands"'.format(number, message_body))
        print(reply)
        return str(resp)


def findweather(): #Finds the current temperatures for nyc
    url = ('http://api.wunderground.com/api/API-KEY-HERE/conditions/q/ny/new_york.json')
    response = urllib.request.urlopen(url).read()

    json_obj = str(response,'utf-8')
    data = json.loads(json_obj)
    number = request.form['From']

    for key, value in data['current_observation'].items():
            if key == 'temperature_string':
                temp = value;

    mesText = ("The temperature is currently: " + temp)

    client.messages.create(
        to=number,
        from_="TWILIO-NUM",
        body=mesText
        )

def forecast(i,j):#Finds the forecast for current day and next three days, only uses the next day in my program as of now
    
    url = ('http://api.wunderground.com/api/API-KEY-HERE/forecast/q/ny/new_york.json')
    response = urllib.request.urlopen(url).read()

    json_obj = str(response,'utf-8')
    number = request.form['From']
    data = json.loads(json_obj)
    jlist = data['forecast']
    for key in jlist:
        for event in jlist['txt_forecast']['forecastday']:
            if (i < j):
                for k,v in event.items():
                    i = i +1
                    if (k == 'fcttext'):
                        fore = v;
    mesText = (fore)

    client.messages.create(
        to=number,
        from_="TWILIO-NUM",
        body=mesText
        )
def commandList(): #List of current commands besides hi/bye 
    number = request.form['From']

    mesText = 'For the current temperature, send "Temperature". For forecast, send Forecast "morning"/"evening"/"tomorrow".'

    client.messages.create(
        to=number,
        from_="TWILIO-NUM",
        body=mesText
        )

if __name__ == '__main__':
    app.run()
