import datetime

import convertdate
import jdatetime
import pytz
import telebot
from astral import LocationInfo
from astral.sun import sun
from telebot import types

from bot_data import BOT_TOKEN

TOKEN = BOT_TOKEN

latitude = 35.72
longitude = 51.40

city = LocationInfo("Tehran", "Iran", "Asia/Tehran", latitude, longitude)
example = LocationInfo("Tehran", "Iran", "Asia/Tehran", 35.72, 51.40)

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

s = sun(city.observer, date=tomorrow, tzinfo=pytz.timezone(city.timezone))
out_sunrise = s["sunrise"]

############## Bot Side #####################
print("It's Working...")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def Home_fun(user):
    """this function say welcome and handel start and help command"""

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Months Arrangement')
    btn2 = types.KeyboardButton('Current Date')
    btn3 = types.KeyboardButton('Change Time')
    btn4 = types.KeyboardButton('Sunrise Time☀')
    btn5 = types.KeyboardButton('Full Information')
    btn6 = types.KeyboardButton('About Us')
    btn7 = types.KeyboardButton('Your Own City Data')
    btn8 = types.KeyboardButton('Current Time')

    markup.row(btn4)
    markup.row(btn2, btn8)
    markup.row(btn1)
    markup.row(btn3, btn5)
    markup.row(btn6, btn7)

    chat_id = user.chat.id
    bot.send_message(chat_id, "welcome! Just Testing Now....", reply_markup=markup)


@bot.message_handler(commands=['sunrise'])
def send_data(message):
    """this function send the time of sunrise at the input data"""

    try:
        sunrise = str(out_sunrise)
        bot.reply_to(message, sunrise[11:19])
    except:
        send_exception(message)


test_list = []


def months_arrangement(user):
    message = """
January => 1
February => 2
March => 3 
April => 4
May => 5
June => 6 
July =>7 
August => 8
September => 9
October => 10 
November => 11
December => 12
    """
    try:
        chat_id = user.chat.id
        bot.send_message(chat_id, message)
    except:
        send_exception(message)


def current_date(message):
    try:
        gregorian_date = str(datetime.datetime.now())[:11]
        jalali_date = str(jdatetime.datetime.now())[:11]
        text = f"""Gregorian date: {gregorian_date}
Qamari date : {jalali_date}"""
        bot.reply_to(message, text)
    except:
        send_exception(message)


def current_time(message):
    try:
        time_now = str(jdatetime.datetime.now())[11:19]
        bot.reply_to(message, time_now)
    except:
        send_exception(message)


def change_time(message):
    try:
        if ' ' in message.text:
            input_year = str(message.text)
            input_year = input_year.split(' ')

        else:
            input_year = str(message.text)
            input_year = input_year.split('/')
    except:
        send_exception(message)
    try:
        data_list = []
        data = convertdate.persian.from_gregorian(int(input_year[0]), int(input_year[1]), int(input_year[2]))
        for i in data:
            data_list.append(str(i))
        data_list = '/'.join(data_list)
        bot.reply_to(message, data_list)

    except:
        send_exception(message)


def is_date(date):
    try:
        if '/' in date:
            year, month, day = date.split('/')
        else:
            year, month, day = date.split(' ')
    except:
        return False
    try:
        datetime.datetime(int(year), int(month), int(day))
        return True
    except ValueError:
        return False


def full_information(message):
    try:
        full_data = (
            f'City:    {city.name}\n'
            f'Dawn:    {str(s["dawn"])[:19]}\n'
            f'Sunrise: {str(s["sunrise"])[:19]}\n'
            f'Noon:    {str(s["noon"])[:19]}\n'
            f'Sunset:  {str(s["sunset"])[:19]}\n'
            f'Dusk:    {str(s["dusk"])[:19]}\n'
        )
        chat_id = message.chat.id
        bot.send_message(chat_id, full_data)
    except:
        send_exception(message)


def set_city(message):
    try:
        z = str(message.text).split(' ')
        city = LocationInfo(z[0], z[1], z[2], float(z[3]), float(z[4]))
        s = sun(city.observer, date=datetime.datetime.now(), tzinfo=pytz.timezone(city.timezone))
        full_data = (
            f'Dawn:    {str(s["dawn"])[:19]}\n'
            f'Sunrise: {str(s["sunrise"])[:19]}\n'
            f'Noon:    {str(s["noon"])[:19]}\n'
            f'Sunset:  {str(s["sunset"])[:19]}\n'
            f'Dusk:    {str(s["dusk"])[:19]}\n'
        )
        chat_id = message.chat.id
        bot.send_message(chat_id, full_data)
    except:
        send_exception(message)


def send_exception(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, """Sorry! 
Maybe you did something wrong!
Or bot have trouble report that!
Try again.""")


@bot.message_handler(content_types=["text"])
def handle_other(message):
    """this function handle all other commands"""

    first_name = message.chat.first_name
    user_name = message.chat.username
    chat_id = message.chat.id
    user_text = message.text

    date_is = str(message.text)[:4]

    if user_text == 'Sunrise Time☀':
        send_data(message)
    if user_text == 'Months Arrangement':
        months_arrangement(message)
    if user_text == 'Current Date':
        current_date(message)
    if user_text == 'Current Time':
        current_time(message)
    if user_text == 'Change Time':
        bot.reply_to(message, "Send date")
        bot.send_message(chat_id, "Example : 2020 9 16")
        bot.send_message(chat_id, "or")
        bot.send_message(chat_id, "Example : 2020/9/16")
    if date_is.startswith('202'):
        change_time(message)
    if user_text == 'Full Information':
        full_information(message)
    if user_text == 'About Us':
        bot.send_message(chat_id, """This is just for resolve personal need !
thanks for using my bot♡,
creator: Amirali""")
    if user_text == 'Your Own City Data':
        bot.send_message(chat_id, """Send your city information.""")
        bot.send_message(chat_id, """[city] [country] [region/city] [latitude] [longitude]""")
        bot.send_message(chat_id, """Example => Tehran Iran Asia/Tehran 35.72 51.40""")
        bot.send_message(chat_id, "All data must be uppercase!")
    if str(user_text).count(' ') == 4:
        set_city(message)


bot.polling()
