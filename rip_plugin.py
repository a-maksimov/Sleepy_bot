import youtube_dl
import os
from SQLighter import SQLighter
import mutagen

# https://stackoverflow.com/questions/27473526/download-only-audio-from-youtube-video-using-youtube-dl-in-python-script    
def rip(bot,message):
    url = " ".join(message.text.split()[1:2])
    db = " ".join(message.text.split()[2:])
    ydl_opts = {
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info("{}".format(url)) # https://github.com/rg3/youtube-dl/issues/13750
    mp3file = os.path.splitext(ydl.prepare_filename(result))[0] +'.mp3'
    # https://stackoverflow.com/questions/18369188/python-add-id3-tags-to-mp3-file-that-has-no-tags
    try:    
        audio = EasyID3(mp3file)
        name = os.path.splitext(os.path.basename(mp3file))[0]
        artist = name.split(" -")[0]
        title = name.split(" - ")[1]
        audio["artist"] = artist
        audio["title"] = title
        audio.save()
        print(audio)
    except:
        bot.send_message(message.chat.id, "Failed to insert ID3 tags.", reply_to_message_id=message.message_id)
    with open(mp3file, 'rb') as f:
        if artist:
            audio_message = bot.send_audio(message.chat.id,f,performer=artist,title=title,timeout=30)
        else:
            bot.send_audio(message.chat.id,f,timeout=30)
    os.remove(mp3file)
    if db:
        try:
            song = (audio_message.audio.file_id,audio_message.audio.performer + " - " + audio_message.audio.title,message.from_user.username)
            print(song)
            db_worker = SQLighter(config.database_name)
            table = 'sotd'
            db_worker.add(table,song)
            db_worker.close()
            bot.send_message(audio_message.chat.id, "Song " + audio_message.audio.file_id + " added to database, thanks!", reply_to_message_id=audio_message.message_id)
        except:
            bot.send_message(audio_message.chat.id, "Bad ID3 tags or duplicate.", reply_to_message_id=audio_message.message_id)