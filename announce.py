import threading
import time
import os
import random

# https://stackoverflow.com/questions/6411811/randomly-selecting-a-file-from-a-tree-of-directories-in-a-completely-fair-manner
def random_file(directory):
    files = [os.path.join(path, filename)
         for path, dirs, files in os.walk(directory)
         for filename in files
         if filename.endswith(".jpg" or ".png" or "gif")]
    return random.choice(files)

def announce():
    directory = 'c:\\Comic strips\\'
    f = open(random_file(directory), 'rb')
    bot.send_photo(GROUP_ID, f, caption="Cartoon of the day:")
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_last()
    try:
        table = 'real_sotd'
        db_worker.add(table,row[1:4])
        bot.send_message(GROUP_ID,"Song of the day submitted by {} Drop an audio here and it will become the next song of the day.".format(row[3]))
        bot.send_audio(GROUP_ID,row[1])
    except:
        bot.send_message(GROUP_ID,"Drop an audio here and it will become the next song of the day.")
    db_worker.close()
    
announce_interval = 86400
 
def my_timer_announce(announce_interval):
    data = threading.local()
    data.counter = 1
    while True:
        time.sleep(announce_interval)
        announce()
        bot.send_message(GROUP_ID, "I am alive %d times!" % data.counter, threading.current_thread().name)
        data.counter += 1
         
t_announce = threading.Thread(target=my_timer_announce, name="Time thread for announce", args=(86400, )) # next announce in 24 hours
t_announce.daemon = True
t_announce.start()
    
def announce_command(bot,message):
    directory = 'c:\\Comic strips\\'
    f = open(random_file(directory), 'rb')
    bot.send_photo(message.chat.id, f, caption="Cartoon of the day:")
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_last()
    try:
        table = 'real_sotd'
        db_worker.add(table,row[1:4])
        bot.send_message(message.chat.id,"Song of the day submitted by {} Drop an audio here and it will become the next song of the day.".format(row[3]))
        bot.send_audio(message.chat.id,row[1])
    except:
        bot.send_message(message.chat.id,"Drop an audio here and it will become the next song of the day.")
    db_worker.close()