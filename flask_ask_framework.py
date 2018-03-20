from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import requests
import logging
import os

app = Flask(__name__)
ask = Ask(app, '/alexa_faskask')
app.config['ASK_VERIFY_REQUESTS'] = False
app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.2dbd6792-766b-4dc8-a6ee-1c53189f1675'

if os.getenv('GREETINGS_DEBUG_EN',False):
    logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch ():
    speech_text = '<speak> Welcome to Greetings skill. Using our skill you can greet your guests.</speak>'
    reprompt_text = '<speak> Whom you want to greet? You can say for example, say hello to John </speak>'
    return question(speech_text).reprompt(reprompt_text)

@ask.intent('HelloIntent', mapping={'first_name' : 'FirstName'}, default={'first_name':'Unknown'})
def hello_intent(first_name):
    wish_text = 'Hello '+first_name+'. '+get_wish()
    quote_text = get_quote()
    speech_text = wish_text+' This is quote of the day for you. '+quote_text+'.'
    return statement('<speak>'+speech_text+'</speak>').standard_card(wish_text, quote_text,
    small_image_url='https://commons.wikimedia.org/wiki/File:Hello_smile.png',
    large_image_url='https://commons.wikimedia.org/wiki/File:Hello_smile.png')

@ask.intent('QuoteIntent')
def quote_intent():
    speech_text = '<speak>This is quote of the day for you. </speak>'+get_quote+'. </speak>Do you want listen one more quote?</speak>'
    reprompt_text ='<speak> You can say, more, one more, yes, or yes please.</speak>'
    session.attributes['quote_intent'] = True
    return question(speech_text).reprompt(reprompt_text)

@ask.intent('NextQuoteIntent')
def next_quote_intent():
    if 'quote_intent' in seession.attributes:
        speech_text = '<speak> This is one more quote for you. </speak>'+get_quote+'. </speak>Do you want listen one more quote?</speak>'
        reprompt_text = '<speak> You can say, more, one more, yes, or yes please.</speak>'
        return question(speech_text).reprompt(reprompt_text)
    else:
        speech_text = '<speak>Wromg invocation of the intent.</speak>'
        return statement(speech_text)

@ask.intent('AMAZON.StopIntent')
def amazon_stop_intent():
    speech_text = '<speak>Good bye. See you soon.</speak>'
    return statement(speech_text)

@ask.on_session_started
def new_session():
    log.info('New session started...')

@ask.session_ended
def session_ended():
    return "{}",200

def get_wish():
    'Return good morning/afternoon/evening depending on time of the day'
    current_time = datetime.datetime.utcnow()
    hours = current_time.hour-8
    if hours <0:
        hours = 24+hours

    if hours < 12:
        return  'Good Morning. '
    elif hours < 18:
        return 'Good Afternoon. '
    else:
        return 'Good Evening. '

def get_quote():
    r = requests.get('http://api.forismatic.com/api/1.0/json?method=getQuote&lang=en&format=json')
    r._content = r._content.decode('unicode_escape').encode('ascii','ignore')
    '''r._content = r._content.replace('\\','')
    quote = r.json()['quoteText']'''
    quote = 'This quote is hard coded. Need to fix get_quote function'
    return quote

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
