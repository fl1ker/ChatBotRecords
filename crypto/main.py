import telebot
import sqlite3
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = telebot.TeleBot('')

name = None
number = None
currency = None
action = None
amount = None
available_currencies = ['USDT', 'BTC', 'ETH', 'TON', 'NOT']
available_actions = ['Buy', 'Sell']

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, I will register you now. Please write your full name:')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Please write your phone number (+48 xxx xxx xxx):')
    bot.register_next_step_handler(message, user_number)

def user_number(message):
    global number
    number = message.text
    bot.send_message(message.chat.id, 'Perfect, now choose a currency:')
    bot.send_message(message.chat.id, 'Select a currency:', reply_markup=generate_currency_markup())
    bot.register_next_step_handler(message, user_currency)

def user_currency(message):
    global currency
    selected_currency = message.text
    if selected_currency in available_currencies:
        currency = selected_currency
        bot.send_message(message.chat.id, 'Please choose an action (Buy/Sell):', reply_markup=generate_action_markup())
        bot.register_next_step_handler(message, user_action)
    else:
        bot.send_message(message.chat.id, 'Invalid currency selected. Please select a valid currency.', reply_markup=generate_currency_markup())
        bot.register_next_step_handler(message, user_currency)

def user_action(message):
    global action
    action = message.text
    if action in available_actions:
        bot.send_message(message.chat.id, 'Please enter the amount you want to transact:')
        bot.register_next_step_handler(message, user_amount)
    else:
        bot.send_message(message.chat.id, 'Invalid action selected. Please select Buy or Sell.', reply_markup=generate_action_markup())
        bot.register_next_step_handler(message, user_action)

def user_amount(message):
    global amount
    amount = message.text
    if amount.isdigit():
        bot.send_message(message.chat.id, 'Now, please select a convenient date for our meeting:')
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Select {step}", reply_markup=calendar)
    else:
        bot.send_message(message.chat.id, 'Invalid amount. Please enter a valid number:')
        bot.register_next_step_handler(message, user_amount)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        global name, number, currency, action, amount
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, chat_id INTEGER, name varchar(50), number varchar(50), currency varchar(50), action varchar(10), amount varchar(50), date varchar(50))')
        cursor.execute("INSERT INTO users (chat_id, name, number, currency, action, amount, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (c.message.chat.id, name, number, currency, action, amount, result))
        conn.commit()
        cursor.close()
        conn.close()

        registration_info = f"Registration successful!\n\nName: {name}\nPhone number: {number}\nCurrency: {currency}\nAction: {action}\nAmount: {amount}\nDate: {result}"
        bot.edit_message_text(registration_info, c.message.chat.id, c.message.message_id)

def generate_currency_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for currency in available_currencies:
        markup.add(types.KeyboardButton(currency))
    return markup

def generate_action_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for action in available_actions:
        markup.add(types.KeyboardButton(action))
    return markup

bot.polling(none_stop=True)
