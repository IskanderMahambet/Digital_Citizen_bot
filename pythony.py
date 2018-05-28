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
        check_user_id = cursor.execute('Select * from users where user_id = "%s"'%(message.from_user.id)).fetchone()
        if check_user_id is not None:
                bot.send_message(message.chat.id,'Ваша заявка находится на расмотрении. Как только админ одобрит заявку мы отправим вам уведомление.')
                checkAdminConfirmedDataUser(message)
        else:
                getNumber(message)
                conn.commit()
                conn.close()   
        
def getNumber(message):        
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
        ConfirmButton = types.KeyboardButton('Отправить номер телефона',request_contact=True)
        keyboard.add(ConfirmButton)
        
        bot.send_message(message.chat.id,'Добро пожаловать в бота города Астаны! Отправьте номер мобильного:',reply_markup=keyboard)
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
        bot.register_next_step_handler(message, confirmDataUser)
        
def confirmDataUser(message):
        dataUser['age']=message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
        ConfirmButton = types.KeyboardButton('Подтвердить')
        keyboard.add(ConfirmButton)        
        againButton = types.KeyboardButton('Повторить регистрацию')
        keyboard.add(againButton)
        bot.send_message(message.chat.id,'Номер телефона: ' + dataUser['phone'] + '\n' + 'Адрес: ' + dataUser['address'] + '\n' + 'ФИО: ' + dataUser['name'] + '\n' + 'Возраст: ' + dataUser['age'] + '\n' + '\n' + 'Если данные вверны, нажмите "Подтвердить" для повторной регистрации нажмите на "Повторить регистрацию"', reply_markup = keyboard)
        bot.register_next_step_handler(message, checkChangeButtonDataUser)

def checkChangeButtonDataUser(message):
        if message.text == 'Подтвердить':
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                cursor.execute('Insert into users values('+str(message.from_user.id)+',"'+dataUser['name']+'","'+dataUser['age']+'","'+dataUser['phone']+'",'"0"')')
                bot.send_message(message.chat.id,'Спасибо! Ваша заявка находится на расмотрении. Как только админ одобрит заявку мы отправим вам уведомление.')                
                conn.commit()
                conn.close()
                bot.register_next_step_handler(message, checkAdminConfirmedDataUser)               
        elif message.text == 'Повторить регистрацию':
                checkUserId(message)
        else:
                bot.send_message(message.chat.id,'Нажмите на кнопку')
                bot.register_next_step_handler(message, confirmDataUser(message))

def checkAdminConfirmedDataUser(message):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        user_id = cursor.execute('Select * from users where is_confirmed = "%s"'%(1)).fetchall()
        for i in user_id:                     
                bot.send_message(i[0],"Вы авторизированны, Админ подтвердил вашу заявку")
                buttonMainMenu(message)
        conn.commit()
        conn.close()                 
        bot.register_next_step_handler(message, buttonMainMenu)                       







def buttonMainMenu(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
        aboutProjectButton = types.KeyboardButton('О проекте')
        keyboard.add(aboutProjectButton)        
        sendMessageButton = types.KeyboardButton('Отправить обращение')
        keyboard.add(sendMessageButton)
        myMessageButton = types.KeyboardButton('Мои обращения')
        keyboard.add(myMessageButton)        
        feedbackButton = types.KeyboardButton('Обратная связь')
        keyboard.add(feedbackButton)
        bot.send_message(message.chat.id,'Главное меню:', reply_markup = keyboard)
        bot.register_next_step_handler(message, checkChangeButtonMainMenu)                      

def readMoreButton(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
        readMore = types.KeyboardButton('Читать далее...')
        keyboard.add(readMore)
        bot.send_message(message.chat.id,"Клуб Активистам города которым не всё равно где жить ",reply_markup = keyboard)
        bot.register_next_step_handler(message, changeReadMoreButton)                      
        
def changeReadMoreButton(message):
        if message.text == 'Читать далее...':                
                bot.send_message(message.chat.id,"Эту инфу должен заполнить админ")       










def sendMessageButton(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)        
        button1 = types.KeyboardButton('Грязь и мусор')
        keyboard.add(button1)
        button2 = types.KeyboardButton('Ямы')
        keyboard.add(button2)
        button3 = types.KeyboardButton('Неисправное освещение')
        keyboard.add(button3)
        button4 = types.KeyboardButton('Показать все категории')
        keyboard.add(button4)
        button5 = types.KeyboardButton('Поменять избранные категории')
        keyboard.add(button5)

        bot.send_message(message.chat.id,"Чтобы отправить обращение нужно пройти 4 шага - №1 <Выберите категорию обращения>",reply_markup = keyboard)
        bot.register_next_step_handler(message, changeReadMoreButton)
        





def checkChangeButtonMainMenu(message):
        if message.text == 'О проекте':
                readMoreButton(message)
                
        elif message.text == 'Отправить обращение':
                pass
        elif message.text == 'Мои обращения':
                pass
        elif message.text == 'Обратная связь':
                pass
bot.polling(none_stop=True)
