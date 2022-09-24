import re
import random
  
def dice(bot,message):
    roll = " ".join(message.text.split()[1:2])
    add = " ".join(message.text.split()[2:])
    if roll and add:
        if re.search('^\d+d\d+$',roll):
            count = int(re.search('(\d+)d\d+',roll).group(1))
            sides = int(re.search('\d+d(\d+)',roll).group(1))
            if sides < 2:
                bot.send_message(message.chat.id, "The minimum range is 2.",reply_to_message_id=message.message_id)
            elif sides > 1000 or count > 1000:
                bot.send_message(message.chat.id, "The maximum range and count are 1000.",reply_to_message_id=message.message_id)   
        elif re.search('^d\d+$',roll):
            count = 1
            sides = int(re.search('d(\d+)',roll).group(1))
        list_result = []
        for i in range(0,count):
            result = random.randint(1,sides)
            list_result.append(result)
        bot.send_message(message.chat.id, " + ".join(str(v) for v in list_result)+" = "+str(sum(list_result)),reply_to_message_id=message.message_id) # https://stackoverflow.com/questions/10880813/typeerror-sequence-item-0-expected-string-int-found
    elif roll:
        if re.search('^\d+d\d+$',roll):
            count = int(re.search('(\d+)d\d+',roll).group(1))
            sides = int(re.search('\d+d(\d+)',roll).group(1))
            if sides < 2:
                bot.send_message(message.chat.id, "The minimum range is 2.",reply_to_message_id=message.message_id)
            elif sides > 1000 or count > 1000:
                bot.send_message(message.chat.id, "The maximum range and count are 1000.",reply_to_message_id=message.message_id)   
        elif re.search('^d\d+$',roll):
            count = 1
            sides = int(re.search('d(\d+)',roll).group(1))
        list_result = []
        for i in range(0,count):
            result = random.randint(1,sides)
            list_result.append(result)
        bot.send_message(message.chat.id, ", ".join(str(v) for v in list_result),reply_to_message_id=message.message_id) # https://stackoverflow.com/questions/10880813/typeerror-sequence-item-0-expected-string-int-found
    else:
        bot.send_message(message.chat.id, "{}".format(random.randint(1,100)),reply_to_message_id=message.message_id)