import os
from pyairtable import Table

bot_menu = None
bot_cmd = None

#####
os.environ['BOT_API_KEY'] = 'BOT_API_KEY'
os.environ['AIRTABLE_API_KEY'] = 'AIRTABLE_API_KEY'
os.environ['BASE_ID'] = 'BASE_ID'
#####

def GetMenuAir():
    global bot_menu
    if bot_menu is not None:
        return 
    api_key = os.environ['AIRTABLE_API_KEY']
    table = Table(api_key, os.environ['BASE_ID'], 'Commands')
    bot_menu = {}
    for i in table.all():
        bot_menu[i['fields']['command']] = {}
        bot_menu[i['fields']['command']]['name'] = i['fields']['name']
        bot_menu[i['fields']['command']]['message'] = i['fields']['message']
        bot_menu[i['fields']['command']]['questions'] = i['fields']['questions'].split(', ')
        bot_menu[i['fields']['command']]['function_name'] = i['fields']['function_name']
        bot_menu[i['fields']['command']]['icon'] = i['fields']['icon']
        bot_menu[i['fields']['command']]['user_level'] = i['fields']['user_level']
        bot_menu[i['fields']['command']]['menu'] = i['fields']['menu'].split('\n')
        bot_menu[i['fields']['command']]['back'] = i['fields']['back']
    return bot_menu

def GetCommandsAir():
    global bot_cmd
    if bot_cmd is not None:
        return 
    api_key = os.environ['AIRTABLE_API_KEY']
    table = Table(api_key, os.environ['BASE_ID'], 'Cmd')
    bot_cmd = {}
    for i in table.all():
        try:
            bot_cmd[i['fields']['name']] = {}
            bot_cmd[i['fields']['name']]['code'] = i['fields']['code']
        except Exception as e:
            print(str(e))
    return bot_cmd

#bot_menu = GetMenuAir()
#bot_cmd = GetCommandsAir()