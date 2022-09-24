import config
import re
from SQLighter import SQLighter

def sotd(bot,message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_last()
    bot.send_message(message.chat.id, "Song of the day submitted by {}".format(row[3]))
    bot.send_audio(message.chat.id, row[1])
    db_worker.close()
    
def random_song():
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_random()
    db_worker.close()
    return row
     
def user_songs(username):
    db_worker = SQLighter(config.database_name)
    rows = db_worker.select_username(username)
    db_worker.close()
    return rows

def song(bot,message):
    username = " ".join(message.text.split()[1:2])
    count = " ".join(message.text.split()[2:])
    if username:
        if re.search('^@.+?$', username):
            username = re.search('^@(.+?)$', username).group(1)
        else:
            username = username
        if not user_songs(username):
            bot.send_message(message.chat.id, "User haven't submitted any music yet.",reply_to_message_id=message.message_id)
        else:
            if count:
                try:
                    bot.send_message(message.chat.id, "Most recent {} songs submitted by {}:".format(int(count),username))
                    for row in user_songs(username)[::-1][0:int(count)]:
                        bot.send_audio(message.chat.id, row[1])
                except ValueError:
                    bot.send_message(message.chat.id, "Number of songs must be integer.")
            else:
                bot.send_message(message.chat.id, "Most recent 3 songs submitted by {}:".format(username))
                for row in user_songs(username)[::-1][0:3]:
                    bot.send_audio(message.chat.id, row[1])
    else:
        try:
            row = random_song()
            bot.send_message(message.chat.id, u"Random song submitted by {}:".format(row[3]))
            bot.send_audio(message.chat.id, row[1])
        except:
            bot.send_message(message.chat.id, "Try again.",reply_to_message_id=message.message_id)