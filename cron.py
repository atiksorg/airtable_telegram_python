import os
from datetime import datetime

import air_db
import _globals
import config

import telebot
bot = telebot.TeleBot(os.environ['BOT_API_KEY'])

jobs = air_db.GetAllRecord('Cron')
for job in jobs:
    
    #print(int(job['fields']['time'].split(':')[0]), int(datetime.now().strftime('%H')))
    #print(int(job['fields']['time'].split(':')[1]), int(datetime.now().strftime('%M')))
    
    H_local = int(datetime.now().strftime('%H'))
    H_air = int(job['fields']['time'].split(':')[0])
    
    if H_local == H_air:
        print(H_local, H_air)
        try:
            res = _globals.RunCode(job['fields']['code'], {}, {})
        except Exception as e:
            res = {'message' : str(e)}

        for i in res['chatid_list']:
            bot.send_message(i, res['message'])
            
    

