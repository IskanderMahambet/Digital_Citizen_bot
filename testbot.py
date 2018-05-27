import sqlite3
import telebot
from datetime import datetime
from telebot import types

dataUser = {'phone':'',
            'address':'',
            'name':'',
            'age':''}



token = '603319412:AAEw2wk-JJ7IKuXQADciHSsRC_TsV8u0vzw'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
        checkUserId(message)

def checkUserId(message):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        print(message.from_user.id)
        check_user_id = cursor.execute('Select * from users where user_id = "%s"'%(message.from_user.id)).fetchone()
        if check_user_id is not None:
                bot.send_message(message.chat.id,'Вы авторизированы')
        else:
                getNumber(message)
        conn.commit()
        conn.close()   
        
def getNumber(message):        
        buttons = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        numButton = types.KeyboardButton('Отправить номер', request_contact=True)
        buttons.add(numButton)
        bot.send_message(message.chat.id,'Добро пожаловать в бота города Астаны! Отправьте номер мобильного:',reply_markup=buttons)
        bot.register_next_step_handler(message, getAddress)

def getAddress(message):
        dataUser['phone']=message.contact.phone_number
        bot.send_message(message.chat.id,'Введите адрес:')
        bot.register_next_step_handler(message, getName)

def getName(message):
        dataUser['address']=message.text        
        bot.send_message(message.chat.id,'Введите ваше ФИО:')
        bot.register_next_step_handler(message, getAge)
        
def getAge(message):
        dataUser['name']=message.text        
        bot.send_message(message.chat.id,'Введите ваш возраст:')
        bot.register_next_step_handler(message, checkDataUser)
def checkDataUser(message):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        numButton = types.KeyboardButton('Подтвердить')
        keyboard.add(numButton)
        dataUser['age']=message.text
        bot.send_message(message.chat.id,'Номер телефона: ' + dataUser['phone'] + '\n' + 'Адрес: ' + dataUser['address'] + '\n' + 'ФИО: ' + dataUser['name'] + '\n' + 'Возраст: ' + dataUser['age'] + '\n' + '\n' + 'Если данные вверны, нажмите "Подтвердить" для повторной регистрации нажмите на "Повторить регистрацию"', reply_markup = keyboard)
        bot.register_next_step_handler(message, confirmButtonDataUser)

def confirmButtonDataUser(message):
       if message.text == 'Подтвердить':
               conn = sqlite3.connect('users.db')
               cursor = conn.cursor()
               cursor.execute('Insert into users values('+str(message.from_user.id)+',"'+dataUser['name']+'","'+dataUser['age']+'","'+dataUser['phone']+'",'"0"')')
               conn.commit()
               conn.close()
       elif message.text == 'Сначала':
               pass
       else:
               bot.send_message(message.chat.id,'Нажмите на кнопку')

       

                
#check_user.id = cursor.execute('Select * from users where login = "%s"'%(login_cr)).fetchone()

bot.polling(none_stop=True)
