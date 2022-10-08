# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2017

@author: Administrator
'''

import telebot
import config
import csv
import time
import datetime
import logging

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    # 'temperature': 'Shows current temperature in my kitchen',
    'song': 'A random song from the database',
    'song [username] <integer>': 'A list of songs submitted by [username], i.e. /song username 3',
    'sotd': 'Links a song of the day',
    # 'cotd': 'Cartoon of the day',
    'smbc': 'Recent Saturday Morning Breakfast Cereal (SMBC)',
    'xkcd': 'Recent XKCD',
    'phd': 'Recent PhD comic',
    'dilbert': 'Recent Dilbert by Scott Adams',
    'dino': 'Recent Dinosaur Comic',
    'calvin': 'Random Calvin and Hobbes by Bill Watterson',
    'announce': 'Check daily announcements',
    'slap [target]': 'Slap somebody',
    'roll [nDr]': 'Roll a dice in nDr format, i.e. /roll 3d8',
    'btc [delta]': 'Average USD market price historical chart across major bitcoin exchanges over delta, which can be either day or week or month or year, i.e. /btc week or just /btc to get current price',
    'weirdal': 'Random Weird Al Yankovic music video.',
    'rip [youtube url] <db>': 'Rip an .mp3 file from youtube and optionally add it to database',
    'likezor [download] <twitter username without @>': 'Download likes of a Twitter user, i.e. /likezor download gaestlic'
}

# Keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
# Keyboard.add('')
# hideKeyboard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console


# telebot.apihelper.proxy = {
#   'https':'socks5://{}:{}'.format(config.ip,config.port)
# }

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for message in messages:
        if message.content_type == 'text':
            # print the sent message to the console
            if message.chat.type == 'private':
                if message.chat.username:
                    print(message.chat.username + " [" + str(message.chat.id) + "]: " + message.text)
                else:
                    print(message.chat.first_name + " [" + str(message.chat.id) + "]: " + message.text)
            else:
                print(message.chat.title + " [" + str(message.chat.id) + "]: " + message.text)


bot = telebot.TeleBot(config.token)

# bot plugins
import start
# import temperature
import audio
import sotd_song
# import cotd_plugin
import announce
import roll
import webcomics
import slap_plugin
import likezor_plugin
import btc_plugin
import yankovic_plugin
import rip_plugin

bot.remove_webhook()

bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    start.handle_start_help(bot, message)


# help page
@bot.message_handler(commands=['help'])
def command_help(message):
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(message.chat.id, help_text)  # send the generated help page


# @bot.message_handler(commands=['temperature'])
# @bot.message_handler(func=lambda message: message.text == 'Temperature')
# def handle_temperature(message):
#     temperature.handle_temperature(bot, message)

from slippy_bot import bot


@bot.message_handler(content_types=['audio'])
def handle_drop_audio(message):
    audio.handle_drop_audio(bot, message)


@bot.message_handler(func=lambda message: message.text == 'SOTD')
@bot.message_handler(commands=['sotd'])
def sotd(message):
    sotd_song.sotd(bot, message)


@bot.message_handler(func=lambda message: message.text == 'Song')
@bot.message_handler(commands=['song'])
def song(message):
    sotd_song.song(bot, message)


# @bot.message_handler(commands=['cotd'])
# def cotd(message):
#     cotd_plugin.handle_cotd(bot, message)


@bot.message_handler(commands=['announce'])
def announce_command(message):
    announce.announce_command(bot, message)


@bot.message_handler(commands=['roll'])
def dice(message):
    roll.dice(bot, message)


@bot.message_handler(commands=['smbc'])
def smbc(message):
    webcomics.smbc(bot, message)


@bot.message_handler(commands=['calvin'])
def calvin(message):
    webcomics.calvin(bot, message)


@bot.message_handler(commands=['xkcd'])
def xkcd(message):
    webcomics.xkcd(bot, message)


@bot.message_handler(commands=['dilbert'])
def dilbert(message):
    webcomics.dilbert(bot, message)


@bot.message_handler(commands=['phd'])
def phd(message):
    webcomics.phd(bot, message)


@bot.message_handler(commands=['dino'])
def dino(message):
    webcomics.dinosaur(bot, message)


@bot.message_handler(commands=['slap'])
def slap(message):
    slap_plugin.slap(bot, message)


@bot.message_handler(commands=['likezor'])
def likezor(message):
    likezor_plugin.likezor(bot, message)


@bot.message_handler(commands=['btc'])
def btc(message):
    btc_plugin.btc(bot, message)


@bot.message_handler(commands=['weirdal'])
# http://pantuts.com/2013/02/16/youparse-extract-urls-from-youtube/
def yankovic(message):
    yankovic_plugin.yankovic(bot, message)


@bot.message_handler(commands=['rip'])
# https://stackoverflow.com/questions/27473526/download-only-audio-from-youtube-video-using-youtube-dl-in-python-script    
def rip(message):
    rip_plugin.rip(bot, message)


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    ##    bot.reply_to(message, "Sorry, I don't work with documents.")
    pass


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    ##    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")
    pass


@bot.message_handler(func=lambda msg: msg.text == u'\U0001F4A9')
def set_ro(message):
    bot.send_message(message.chat.id, "Sorry, no shit posting.", reply_to_message_id=message.message_id)
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + 31)


def telegram_polling():
    """
    https://github.com/eternnoir/pyTelegramBotAPI/issues/206
    https://github.com/eternnoir/pyTelegramBotAPI/issues/401
    """
    try:
        bot.polling(none_stop=True, timeout=100)  # constantly get messages from Telegram
    except Exception as err:
        logging.error(err)
        bot.stop_polling()
        print("Internet error!")
        time.sleep(10)
        telegram_polling()


if __name__ == '__main__':
    telegram_polling()
