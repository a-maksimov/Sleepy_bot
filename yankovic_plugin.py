# http://pantuts.com/2013/02/16/youparse-extract-urls-from-youtube/
def yankovic(bot,message):
    url = 'https://www.youtube.com/watch?v=zq7Eki5EZ8o&list=PLGbwKffY2xoKTszTk57KAuLY26xAClErq'
    html = urlopen(url).read().decode('utf-8')
    eq = url.rfind('=') + 1
    cPL = url[eq:]
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, html)
    final_url = []
    for PL in mat:
        yPL = str(PL)
        if '&' in yPL:
            yPL_amp = yPL.index('&')
        final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])
    bot.send_message(message.chat.id,random.choice(final_url),reply_to_message_id=message.message_id)