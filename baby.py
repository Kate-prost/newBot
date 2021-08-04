import datetime
import os
import random
import threading
import telebot
import coooonf

bot = telebot.TeleBot(coooonf.token)


@bot.message_handler(commands=['start'])
def handle(message):
    send_mess = F"<b>Ну здраствуй, {message.from_user.first_name} !" \
                F"Бот знает комманды: \n" \
                F"/who \n" \
                F"/help \n" \
                F"/info \n" \
                F"/timer \n" \
                F"/HW \n</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['timer'])
def start(message):
    bot.send_message(message.chat.id,
                     'Я могу установить таймер.',
                     reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda x: x.data == 'set timer')
def pre_set_timer(query):
    message = query.message
    bot.send_message(message.chat.id,
                     'Введи время для установки таймера.\n'
                     'Пример ввода: \n'
                     '1. 30 сек\n'
                     '2. 2 мин\n'
                     '3. 10 час')
    bot.register_next_step_handler(message, set_time)


def set_time(message):
    times = {
        'сек': 0,
        'мин': 0,
        'час': 0
    }

    quantity, type_time = message.text.split()

    if type_time not in times.keys():
        bot.send_message(message.chat.id,
                         'Ты ввел неправильный тип времени.')
        return

    if not quantity.isdigit():
        bot.send_message(message.chat.id,
                         'Ты ввел не число!')

    times[type_time] = int(quantity)

    pre_set_text(message, times)


def pre_set_text(message, times):
    bot.send_message(message.hat.id,
                     'Введи текст, который придёт после'
                     ' истечения таймера.')
    bot.register_next_step_handler(message, set_text, times)


def set_text(message, times):
    cur_date = datetime.datetime.now()

    timedelta = datetime.timedelta(days=0, seconds=times['сек'],
                                   minutes=times['мин'], hours=times['час'])

    cur_date += timedelta

    users[message.chat.id] = (cur_date, message.text)
    bot.send_message(message.chat.id,
                     'Олтично:) Через заданное время тебе'
                     ' придёт уведомление.')


def check_date():
    now_date = datetime.datetime.now()
    users_to_delete = []
    for chat_id, value in users.items():
        user_date = value[0]
        msg = value[1]
        if now_date >= user_date:
            bot.send_message(chat_id, msg)
            users_to_delete.append(chat_id)
    for user in users_to_delete:
        del users[user]
    threading.Timer(1, check_date).start()


def get_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton('Установить таймер', callback_data='set timer')
    keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['who'])
def hw(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Жмииии", url='https://www.linkedin.com/in/azubritskiy/'))
    bot.send_message(message.chat.id, 'главный чел,который нас пытается научить', reply_markup=markup)


@bot.message_handler(commands=['HW'])
def hw(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Жмякай", url='https://github.com/Kate-prost/HW'))
    bot.send_message(message.chat.id, 'Хочешь глянуть мою домашку?!', reply_markup=markup)


@bot.message_handler(commands=['info'])
def get_user_info(message):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    item_yes = telebot.types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = telebot.types.InlineKeyboardButton(text='НЕТ', callback_data='no')

    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Закинул ли ты домашку?!', reply_markup=markup_inline)


@bot.callback_query_handler(func= lambda call:True)
def answer(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, "Я в тебе не сомневалась!")
        directory = '/Users/katekravchenko/Desktop/memslike'
        all_file_in_directory = os.listdir(directory)
        random_file = random.choice(all_file_in_directory)
        print(all_file_in_directory)
        img = open(directory + '/' + random_file, 'rb')
        bot.send_chat_action(call.from_user.id, 'upload_photo')
        bot.send_photo(call.from_user.id, img)
        img.close()

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, "Совсем охренел в край? Быстро исправился!" )
        directory = '/Users/katekravchenko/Desktop/memsfy'
        all_file_in_directory = os.listdir(directory)
        random_file = random.choice(all_file_in_directory)
        print(all_file_in_directory)
        img = open(directory + '/' + random_file, 'rb')
        bot.send_chat_action(call.from_user.id, 'upload_photo')
        bot.send_photo(call.from_user.id, img)
        img.close()


@bot.message_handler(commands=['help'])
def get_user_info(message):
    send_mess = F"<b>Ну что ты, {message.from_user.first_name}" \
                F" ? Здесь помощи нет. Сам знаешь где искать(Google.com тебе в помощь :))</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


if __name__ == '__main__':
    users = {}
    while True:
        try:
            check_date()
            bot.polling()
        except:
            print('Что-то сломалось. Перезагрузка')