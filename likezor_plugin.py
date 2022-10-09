import twitter
import config
import threading
import time
import os
import slippy_bot
from SQLighter import SQLighter

# Twitter:
consumer_key = '<insert api token>'
consumer_secret = '<insert api secret>'
access_token_key = '<insert access token>'
access_token_secret = '<insert access secret>'

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret,
                  sleep_on_rate_limit=True)


def likezor(bot, message):
    command = " ".join(message.text.split()[1:2])
    name = " ".join(message.text.split()[2:])
    table = 'twitter'
    if command == 'register':
        if name:
            # Check if name exists on twitter
            try:
                api_account = api.GetUser(screen_name=name)
                # Check if blocked by Twitter user
                try:
                    # Get user's like with the latest id
                    api_like = api.GetFavorites(screen_name=api_account.screen_name, count=1)
                    like_id = api_like[0].id
                    # Create row for accounts database
                    # Check if user has telegram @username
                    if message.from_user.username:
                        account = (api_account.screen_name, api_account.id, api_account.favourites_count, like_id,
                                   message.from_user.username)
                    else:
                        account = (api_account.screen_name, api_account.id, api_account.favourites_count, like_id,
                                   message.from_user.id)
                    # Connect to database
                    db_worker = SQLighter(config.database_name)
                    # Check if user already exists in database
                    if db_worker.select_one_account(table, name):
                        bot.send_message(message.chat.id, "Twitter user's been registered already.",
                                         reply_to_message_id=message.message_id)
                    else:
                        # Add row to accounts database
                        db_worker.add_twitter(table, account)
                        db_worker.close()
                        # Get the initial 25 user's likes with the latest ids and write them to file
                        api_like = api.GetFavorites(screen_name=api_account.screen_name, count=25)
                        filepath = os.path.join(os.getcwd(), "likezor")
                        if not os.path.exists(filepath):
                            os.mkdir(filepath)
                            print("folder for likezor created")
                        else:
                            print("folder likezor already exists")
                        file = os.path.join(filepath, api_account.screen_name + "_chain.csv")
                        with open(file, "w+") as like_id_chain:
                            print("saving initial likes to file: " + file)
                            for i in range(0, len(api_like)):
                                like_id = api_like[i].id
                                like_id_chain.write(str(like_id) + ", ")
                            if os.path.exists(file):
                                print("file with initial likes: " + file + " was created")
                        bot.send_message(message.chat.id,
                                         "Twitter user " + api_account.screen_name + " was successfully registered.",
                                         reply_to_message_id=message.message_id)
                except:
                    bot.send_message(message.chat.id, "Likezor blocked by {}!".format(api_account.screen_name),
                                     reply_to_message_id=message.message_id)
            except:
                bot.send_message(message.chat.id, "No such Twitter user.", reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Enter twitter username to register.",
                             reply_to_message_id=message.message_id)
    elif command == 'update':
        if name:
            # Connect to Database
            db_worker = SQLighter(config.database_name)
            # If name exists in accounts database
            if db_worker.select_one_account(table, name):
                # Check if name exists on twitter
                try:
                    api_account = api.GetUser(screen_name=name)
                    print("old account row: " + str(db_worker.select_one_account(table, name)))
                    # Try to get latest id like unless blocked
                    try:
                        api_like = api.GetFavorites(screen_name=name, count=1)
                        like_id = api_like[0].id
                        # Refresh row in accounts database with new latest in data
                        db_worker.update_twitter(table, api_account.favourites_count, like_id, api_account.screen_name)
                        print("updated account row: " + str(db_worker.select_one_account(table, name)))
                        db_worker.close()
                        bot.send_message(message.chat.id, "Twitter user {} was successfully updated.".format(name),
                                         reply_to_message_id=message.message_id)
                    except:
                        bot.send_message(message.chat.id, "Likezor blocked by {}!".format(api_account.screen_name),
                                         reply_to_message_id=message.message_id)
                except:
                    bot.send_message(message.chat.id, "No such Twitter user.", reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id, "No Twitter user {} registered.".format(name),
                                 reply_to_message_id=message.message_id)
            db_worker.close()
        else:
            bot.send_message(message.chat.id, "Enter twitter username to update.",
                             reply_to_message_id=message.message_id)
    elif command == 'unregister':
        if name:
            # Connect to database
            db_worker = SQLighter(config.database_name)
            # If name exists in database
            if db_worker.select_one_account(table, name):
                # Delete row containing the name
                db_worker.delete_twitter(table, name)
                db_worker.close()
                bot.send_message(message.chat.id, "Twitter user " + name + " was successfully unregistered.",
                                 reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id, "No Twitter user {} registered.".format(name),
                                 reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Enter twitter username to unregister.",
                             reply_to_message_id=message.message_id)
    elif command == 'download':
        if name:
            # Check if name exists on twitter
            try:
                api_account = api.GetUser(screen_name=name)
                likes_list = []
                # Download initial 200 likes
                try:
                    api_like = api.GetFavorites(screen_name=api_account.screen_name, count=200)
                    likes_list.extend(api_like)
                    print("..%s tweets downloaded so far" % (len(likes_list)))
                    oldest = likes_list[-1].id - 1
                    while len(api_like) > 0:
                        print("getting tweets before %s" % oldest)
                        # all subsequent requests use the max_id param to prevent duplicates
                        api_like = api.GetFavorites(screen_name=api_account.screen_name, count=200, max_id=oldest)
                        # save most recent likes
                        likes_list.extend(api_like)
                        # update the id of the oldest like less one
                        oldest = likes_list[-1].id - 1
                        print("..%s tweets downloaded so far" % (len(likes_list)))
                        time.sleep(3)
                    for i in range(0, len(likes_list)):
                        filepath = os.path.join(os.getcwd(), "likezor")
                        if not os.path.exists(filepath):
                            os.mkdir(filepath)
                        file = os.path.join(filepath, name + ".csv")
                        with open(file, 'a+', encoding='utf-8') as f:
                            f.write(likes_list[i].created_at + ',' + likes_list[i].id_str + ',' + likes_list[
                                i].user.screen_name + ',' + likes_list[i].text + '\n')
                    bot.send_document(message.chat.id, open(file, 'r', encoding='utf-8'),
                                      reply_to_message_id=message.message_id, timeout=10)
                except:
                    bot.send_message(message.chat.id, "Likezor blocked by {}!".format(api_account.screen_name),
                                     reply_to_message_id=message.message_id)
            except:
                bot.send_message(message.chat.id, "No such Twitter user.", reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Enter twitter username to download likes for.",
                             reply_to_message_id=message.message_id)
    elif command == 'subscribe':
        table = 'subscribers'
        # Connect to database
        db_worker = SQLighter(config.database_name)
        # Check if user already exists in database
        try:
            if name:
                # Check if user has telegram @username
                if message.from_user.username:
                    db_worker.add_subscriber(table, message.from_user.username, message.from_user.id, name)
                elif message.chat.first_name and message.chat.last_name:
                    db_worker.add_subscriber(table, message.from_user.first_name + ' ' + message.from_user.last_name,
                                             message.from_user.id, name)
                elif message.chat.first_name:
                    db_worker.add_subscriber(table, message.from_user.first_name, message.from_user.id, name)
                else:
                    db_worker.add_subscriber(table, message.from_user.id, message.from_user.id, name)
            else:
                # Check if user has telegram @username
                if message.from_user.username:
                    db_worker.add_subscriber(table, message.from_user.username, message.from_user.id, None)
                elif message.chat.first_name and message.chat.last_name:
                    db_worker.add_subscriber(table, message.from_user.first_name + ' ' + message.from_user.last_name,
                                             message.from_user.id, None)
                elif message.chat.first_name:
                    db_worker.add_subscriber(table, message.from_user.first_name, message.from_user.id, None)
                else:
                    db_worker.add_subscriber(table, message.from_user.id, message.from_user.id, None)
            bot.send_message(message.chat.id, 'You have successfully subscribed.',
                             reply_to_message_id=message.message_id)
        except:
            sub_id = db_worker.select_one_subscriber(table, message.from_user.id, )
            bot.send_message(message.chat.id, 'You are already subscribed with an id = {}.'.format(sub_id),
                             reply_to_message_id=message.message_id)
        db_worker.close()
    elif command == 'unsubscribe':
        table = 'subscribers'
        # Connect to database
        db_worker = SQLighter(config.database_name)
        if db_worker.select_one_subscriber(table, message.from_user.id, ) and message.from_user.id == \
                db_worker.select_one_subscriber(table, message.from_user.id, )[0][2]:
            db_worker.delete_subscriber(table, message.from_user.id)
            db_worker.close()
            bot.send_message(message.chat.id, "You have successfully unsubscribed.",
                             reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "You are not subscribed.", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "Enter proper command: /help likezor", reply_to_message_id=message.message_id)


def likezor_broadcast(screen_name, like):
    # connect database
    db_worker = SQLighter(config.database_name)
    table = 'subscribers'
    subscribers = db_worker.select_all(table)
    # https://stackoverflow.com/questions/7313157/python-create-list-of-tuples-from-lists
    # https://stackoverflow.com/questions/27431390/typeerror-zip-object-is-not-subscriptable
    subscribers_list = list(zip([i[2] for i in subscribers], [i[3] for i in subscribers]))
    for sub in subscribers_list:
        if sub[1] != screen_name:
            slippy_bot.bot.send_message(sub[0], like)


def likezor_announce():
    # connect database
    db_worker = SQLighter(config.database_name)
    table = 'twitter'
    accounts = db_worker.select_all(table)
    # make lists from columns in database
    screen_names = [i[2] for i in accounts]
    likes_nums = [i[3] for i in accounts]
    like_ids = [i[4] for i in accounts]
    # do this for each item in screen_names list
    for i in range(0, len(accounts)):
        # get user info with total likes amount
        api_account = api.GetUser(screen_name=screen_names[i])
        # if new total likes amount is bigger than stored one
        if api_account.favourites_count > likes_nums[i]:
            # try except if you are blocked by user
            try:
                #  get some of user's highest id likes
                api_likes = api.GetFavorites(screen_name=api_account.screen_name, count=25)
                print(screen_names[i] + ": db likes: " + str(likes_nums[i]) + "; api likes: " + str(
                    api_account.favourites_count) + "; db like id: " + str(like_ids[i]) + "; api like id: " + api_likes[
                          0].id_str)
            except:
                print('Blocked by {} while downloading likes!'.format(api_account.screen_name))
                break
            # find id for each new like that counts in difference
            api_likes_list = []
            # making a list of downloaded like ids
            for k in range(0, len(api_likes)):
                api_likes_list.append(api_likes[k].id)
            #             print("api likes: " + str(api_likes_list))
            # file with previous likes
            file = os.path.join(os.getcwd(), "likezor", api_account.screen_name + "_chain.csv")
            if os.path.exists(file):
                print("file with previous likes: " + file + " exists")
            # checking if any of downloaded ids is not in file with previous likes
            for n, item in enumerate(api_likes_list):
                if str(item) not in open(file, "r").read():
                    print("new like found: " + api_likes[n].user.screen_name + " " + api_likes[n].id_str)
                    print("opening file with previous likes: " + file)
                    open(file).close()
                    # append new found like to file so that it won't count as difference on next d iteration
                    with open(file, "a") as old_likes:
                        print("appending new likes to: " + file)
                        old_likes.write(api_likes[n].id_str + ", ")
                    #                     with open(file, "r") as old_likes:
                    #                         print(old_likes.read())
                    # broadcast found new like
                    #                     if screen_names[i] == 'gaestlic':
                    #                         bot.send_message(GROUP_ID,"{} liked tweet by @{}:\n".format(screen_names[i],api_likes[n].user.screen_name) + "https://twitter.com/{}/status/{}".format(api_likes[n].user.screen_name,api_likes[n].id_str))
                    likezor_broadcast(screen_names[i], "{} liked tweet by @{}:\n".format(screen_names[i], api_likes[
                        n].user.screen_name) + "https://twitter.com/{}/status/{}".format(api_likes[n].user.screen_name,
                                                                                         api_likes[n].id_str))
                    time.sleep(3)
            #                 else:
            #                     print(str(item) + " is old")
            # update database with new amount of total likes
            db_worker.update_twitter(table, api_account.favourites_count, api_likes[n].id, screen_names[i])
            # rewrite previous likes with new likes in file
            with open(file, "w") as old_likes:
                for i in range(0, len(api_likes)):
                    like_id = api_likes[i].id
                    old_likes.write(str(like_id) + ", ")
        else:
            # update account data in database unless blocked by Twitter user (makes stored amount of likes consistent with api)
            try:
                api_likes = api.GetFavorites(screen_name=api_account.screen_name, count=1)
                db_worker.update_twitter(table, api_account.favourites_count, api_likes[0].id, screen_names[i])
                print(screen_names[i] + ": db likes: " + str(likes_nums[i]) + "; api likes: " + str(
                    api_account.favourites_count) + "; db like id: " + str(like_ids[i]) + "; api like id: " + api_likes[
                          0].id_str)
            except:
                print('Blocked by {} while updating database!'.format(api_account.screen_name))
    db_worker.close()


likezor_interval = 60


def likezor_timer(likezor_interval):
    data = threading.local()
    data.counter = 1
    while True:
        time.sleep(likezor_interval)
        likezor_announce()
        data.counter += 1


t_likezor = threading.Thread(target=likezor_timer, name="Time thread for likezor",
                             args=(60,))  # next check after 5 mins
t_likezor.daemon = True
t_likezor.start()
