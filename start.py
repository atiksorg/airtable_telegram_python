import os
from pyairtable import Table
from pyairtable.formulas import match
import json
from telebot import types

import _globals
import air_api

import telebot
bot = telebot.TeleBot(os.environ['BOT_API_KEY'])
_globals.bot = bot

###
air_api.bot_menu = air_api.GetMenuAir()
air_api.bot_cmd = air_api.GetCommandsAir()
###

@bot.message_handler(content_types=['text'])
def start(message):

    _globals.query_params = []
    if message.text[0] == '/':
        m = message.text.split(' ')
        cmd = m[0]
        _globals.query_params = m[1:]
        RunCommand(message, cmd, _globals.query_params)            
        return
    
    for cmd in air_api.bot_menu.keys():
        if message.text == cmd or air_api.bot_menu[cmd]['name'] in message.text:
            RunCommand(message, cmd)            
            return
        
    RunCommand(message, '/help')
            
def RunCommand(message, cmd = '', query_params = []):

    user_level = 0
    user_table = Table(os.environ['AIRTABLE_API_KEY'], os.environ['BASE_ID'], 'Users')
    formula = match({"chatid": str(message.chat.id)})
    user_data = user_table.first(formula=formula)
    if user_data is not None:
        user_level = 1
    _globals.user_level = user_level
    ###
    
    if _globals.cmd != '':
        cmd = _globals.cmd
        _globals.answers.append(message.text)
    else:
        # Message
        if cmd in air_api.bot_menu.keys() and air_api.bot_menu[cmd]['message'] != '' and air_api.bot_menu[cmd]['message'] != '-':
            bot.send_message(message.chat.id, air_api.bot_menu[cmd]['message'])

    # Questions
    answers = []
    #print(message.text)
    #bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    #print('clear_step_handler_by_chat_id', message.chat.id)
    ###
    Flag = True
    if _globals.q_step > 0:
        for cmd_tmp in air_api.bot_menu.keys():
            if message.text == cmd_tmp or air_api.bot_menu[cmd_tmp]['name'] in message.text:
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)          
                Flag = False
                _globals.cmd = ''
                _globals.q_step = 0
                _globals.answers = []
                cmd = cmd_tmp
    ###
    if Flag:
        if cmd in air_api.bot_menu.keys() and air_api.bot_menu[cmd]['questions'] != ['-']:
            if _globals.q_step < len(air_api.bot_menu[cmd]['questions']):
                bot.send_message(message.chat.id, air_api.bot_menu[cmd]['questions'][_globals.q_step])
                _globals.cmd = cmd
                bot.register_next_step_handler(message, RunCommand)
                _globals.q_step += 1
                return
            else:
                answers = _globals.answers
                _globals.cmd = ''
                _globals.q_step = 0
                _globals.answers = []

    # Function    
    if cmd != '' and air_api.bot_menu[cmd]['function_name'] != '-':
        #cmd_table = Table(os.environ['AIRTABLE_API_KEY'], os.environ['BASE_ID'], 'Cmd')
        #formula = match({"name": air_api.bot_menu[cmd]['function_name']})
        #code = cmd_table.first(formula=formula)
        try:
            function_name = air_api.bot_menu[cmd]['function_name']
            res = _globals.RunCode(air_api.bot_cmd[function_name]['code'], {}, {'chatid' : message.chat.id, 'answers' : answers, 'query_params' : query_params, 'user_level' : _globals.user_level})
        except Exception as e:
            print(str(e))
            res = str(e)
        if 'message' in res:
            if res['message'] == '':
                res['message'] = 'Нет информации 😕'
            if 'InlineKeyboard' in res:
                reply_markup = GetInline(res['InlineKeyboard'])
            else:
                reply_markup = GetMarkup(message, cmd)
            bot.send_message(message.chat.id, res['message'], reply_markup=reply_markup)
    else:
        bot.send_message(message.chat.id, 'Выберите раздел из меню', reply_markup=GetMarkup(message, cmd))
        
def GetMarkup(message, cmd = ''):
    if cmd == '':
        return types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_in_row = 2
    btn_count = 0
    buttons = []
    bot_menu = {}
    ###
    for i in air_api.bot_menu[cmd]['menu']:
        l = i.split(' : ')[0]
        bot_menu[int(l)] = i.split(' : ')[1].split(' ')
    ### Получили список команд
    
    for i in bot_menu[_globals.user_level]:
        buttons.append(types.KeyboardButton(air_api.bot_menu[i]['icon'] + ' ' + air_api.bot_menu[i]['name']))
        btn_count += 1
        if btn_count > btn_in_row - 1:
            markup.add(*tuple(buttons))
            buttons = []
            btn_count = 0
    
    if air_api.bot_menu[cmd]['back'] != '-':
        i = air_api.bot_menu[cmd]['back']
        buttons_back = types.KeyboardButton('◀ ' + air_api.bot_menu[i]['name'])
        markup.add(buttons_back)
        
    return markup

def GetInline(InlineKeyboard=[]):
    btn_in_row = 2
    btn_count = 0
    buttons = []
    inline_kb = types.InlineKeyboardMarkup(row_width=8)
    for i in InlineKeyboard:
        btn_count += 1
        buttons.append(types.InlineKeyboardButton(i[0], callback_data=i[1]))
        if btn_count > btn_in_row:
            inline_kb.add(*tuple(buttons))
            btn_count = 0
            buttons = []
    return inline_kb

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('/'))
def callback_query_handler(callback_query: types.CallbackQuery):
    callback_query.message.text = callback_query.data
    start(callback_query.message)

#bot.polling(none_stop=True, interval=0)
bot.infinity_polling(timeout=10, long_polling_timeout = 5)