# -*- coding: utf-8 -*-
import sys
from time import sleep
from twx.botapi import TelegramBot, ReplyKeyboardMarkup #Telegram BotAPI
import traceback
from pyowm import OWM #Weather API
"""
Setup the bot and the Weather API
"""
TOKEN = ""
OWMKEY = ""

bot = TelegramBot(TOKEN) 
bot.update_bot_info().wait()  #wait for a message
print (bot.username)
last_update_id = 0 
def process_message(bot, u): #This is what we'll do when we get a message 
    #Use a custom keyboard 
    keyboard = [['Get Weather']] #Setting a Button to Get the Weather 
    reply_markup = ReplyKeyboardMarkup.create(keyboard) #And create the keyboard 
    if u.message.sender and u.message.text and u.message.chat: #if it is a text message then get it 
        chat_id = u.message.chat.id 
        user = u.message.sender.username
        message = u.message.text 
        print ( chat_id )
        print ( message )
        if message == 'Get Weather': #if the user is asking for the weather then we ask the location 
            bot.send_message(chat_id, 'please send me your location') 
        else: 
            bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait() #if not then just show the options
 
    elif u.message.location: #if the message contains a location then get the weather on that latitude/longitude 
        print ( u.message.location )
        chat_id = u.message.chat.id 
        owm = OWM(OWMKEY) #initialize the Weather API 
        obs = owm.weather_at_coords(u.message.location.latitude, u.message.location.longitude) #Create a weather observation 
        w = obs.get_weather() #create the object Weather as w 
        print(w) # <Weather - reference time=2013-12-18 09:20, status=Clouds> 
        l = obs.get_location() #create a location related to our already created weather object And send the parameters 
        status = str(w.get_detailed_status()) 
        placename = str(l.get_name()) 
        wtime = str(w.get_reference_time(timeformat='iso')) 
        temperature = str(w.get_temperature('celsius').get('temp'))
        wind = str(w.get_wind().get('speed'))
        bot.send_message(chat_id, 'Wind: '+wind+' at '+placename+' and temperature: '+ temperature+ 'C') #send the anwser
        bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait() #send the options again
    else: 
        print ( u )
        bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait() 
while True: #a loop to wait for messages
    updates = bot.get_updates(offset = last_update_id).wait() #we wait for a message
    try: 
        for update in updates: #get the messages
            if update.update_id > last_update_id : #if it is a new message then get it
                last_update_id = update.update_id 
                process_message(bot, update) #send it to the function 
                continue
        continue
    except Exception: 
        ex = None 
        print ( traceback.format_exc() )
        continue
