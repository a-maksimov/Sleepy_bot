def btc(bot,message):
    from urllib.request import urlopen
    import re
    import time
    btc_url = 'https://blockchain.info/charts/market-price'
    api = 'https://api.blockchain.info/charts/preview/s-f/market-price.png?lang=en&start='
    html = urlopen(btc_url).read().decode('utf-8')
    title = re.search('"features.charts.description.marketprice":"(.+?)"',html).group(1)
    delta = " ".join(message.text.split()[1:2])
    if delta:
        if delta == 'year':
            delta = 31540000
        elif delta == 'month':
            delta = 2628000
        elif delta == 'week':
            delta = 604800
        elif delta == 'day':
            delta = 172800
        else:
            bot.send_message(message.chat.id, 'Delta should be either day or week or month or year.',reply_to_message_id=message.message_id)
        start = int(time.time()) - delta
        bot.send_photo(message.chat.id,api + str(start),caption=title)
    else:
        cors = 'https://blockchain.info/stats?format=json&cors=true'
        cors_html = urlopen(cors).read().decode('utf-8')
        price = re.search('"market_price_usd":(.+?),',cors_html).group(1)
        bot.send_message(message.chat.id,title[:-1] +' is $'+price,reply_to_message_id=message.message_id)