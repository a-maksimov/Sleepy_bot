from urllib.request import urlopen
import re
import time

def smbc(bot,message):
    smbc_url = 'https://www.smbc-comics.com/'
    html = urlopen(smbc_url).read().decode('utf-8')
    strip_url = re.search('<meta property="og:image" content="(.+?)" />',html).group(1)
    title = re.search('<img title="(.+?)"',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url,caption=title)
    
def calvin(bot,message):
    calvin_url = 'http://www.gocomics.com/random/calvinandhobbes'
    html = urlopen(calvin_url).read().decode('utf-8')
    strip_url = re.search('<meta property="og:image" content="(.+?)" />',html).group(1)
    title = re.search('<meta property="og:title" content="(.+?)" />',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url,caption=title)
    
def xkcd(bot,message):
    xkcd_url = 'https://xkcd.com/info.0.json'
    html = urlopen(xkcd_url).read().decode('utf-8')
    strip_url = re.search('"img": "(.+?)",',html).group(1)
    title = re.search('"alt": "(.+?)",',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url.split('.png')[0] +'_2x.png',caption=title)
    
def dilbert(bot,message):
    dilbert_base_url = 'http://dilbert.com/strip/'
    dilbert_url = dilbert_base_url + str(datetime.date.today())
    html = urlopen(dilbert_url).read().decode('utf-8')
    strip_url = re.search('<meta property="og:image" content="(.+?)"/>',html).group(1)
    title = re.search('<meta property="article:publish_date" content="(.+?)"/>',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url,caption=title)
    
def phd(bot,message):
    phd_url = 'http://phdcomics.com/'
    html = urlopen(phd_url).read().decode('utf-8')
    strip_url = re.search("<meta property='og:image' content='(.+?)'/>",html).group(1)
    title = re.search('<meta name="twitter:title" content="(.+?)">',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url,caption=title)
    
def dinosaur(bot,message):
    dinosaur_url = 'http://www.qwantz.com/index.php'
    html = str(urlopen(dinosaur_url).read())
    strip_url = re.search('<meta property="og:image" content="(.+?)" />',html).group(1)
    title = re.search('<meta property="og:description" content="(.+?)" />',html).group(1)
    time.sleep(1)
    bot.send_photo(message.chat.id,strip_url,caption=title)