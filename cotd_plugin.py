import os
import random

def handle_cotd(bot,message):
    directory = 'c:\\Comic strips\\'
    f = open(random_file(directory), 'rb')
    bot.send_photo(message.chat.id, f, caption="Cartoon of the day:")

# https://stackoverflow.com/questions/6411811/randomly-selecting-a-file-from-a-tree-of-directories-in-a-completely-fair-manner
def random_file(directory):
    files = [os.path.join(path, filename)
         for path, dirs, files in os.walk(directory)
         for filename in files
         if filename.endswith(".jpg" or ".png" or "gif")]
    return random.choice(files)