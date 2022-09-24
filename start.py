def handle_start_help(bot,message):
    if message.chat.type == 'private':
        if message.chat.username:
            bot.send_message(message.chat.id,"Greetings, {}. Use /help".format(message.chat.username))
        else:
            bot.send_message(message.chat.id,"Greetings, {}. Use /help".format(message.chat.first_name))
    else:
        bot.send_message(message.chat.id, "Greetings, {}. Use /help".format(message.chat.title))