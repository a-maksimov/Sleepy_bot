import config
from SQLighter import SQLighter
import time

def handle_drop_audio(bot,message):
    try:
        song = (message.audio.file_id,message.audio.performer + " - " + message.audio.title,message.from_user.username)
        db_worker = SQLighter(config.database_name)
        table = 'sotd'
        db_worker.add(table,song)
        db_worker.close()
        bot.send_message(message.chat.id, "Song " + message.audio.file_id + " added to database, thanks!", reply_to_message_id=message.message_id)
    except:
        bot.send_message(message.chat.id, "Something went wrong (bad ID3 tags, duplicate etc.)", reply_to_message_id=message.message_id)
    time.sleep(3)