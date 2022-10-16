from random import randint


def is_valid_num(number):
    if number.isdigit():
        return True
    else:
        return False


def is_valid_limit(limit_left, limit_right):
    if limit_right < limit_left:
        return -1
    elif limit_right == limit_left:
        return 0
    else:
        return 1


def is_inside_limits(limit_left, limit_right, number):
    if limit_left <= number <= limit_right:
        return True
    else:
        return False


def guess(bot, message):
    bot.send_message(message.chat.id, 'Это игра, в которой нужно угадать число в интервале чисел \U0001F648',
                     reply_to_message_id=message.message_id)
    msg_start = bot.send_message(message.chat.id, 'Введите начало интервала \U0001F4AC')
    bot.register_next_step_handler(msg_start, step_set_start, bot)


def step_set_start(message, bot):
    start = message.text
    if not is_valid_num(start):
        msg_invalid_num = bot.send_message(message.chat.id, 'Пожалуйста, введите целое число \U0001F921')
        bot.register_next_step_handler(msg_invalid_num, step_set_start, bot)
    else:
        start = int(start)
        msg_stop = bot.send_message(message.chat.id, 'Введите конец интервала \U0001F4AC')
        bot.register_next_step_handler(msg_stop, step_set_stop, bot, start)


def step_set_stop(message, bot, start):
    stop = message.text
    if not is_valid_num(stop):
        msg_invalid_num = bot.send_message(message.chat.id, 'Пожалуйста, введите целое число \U0001F921')
        bot.register_next_step_handler(msg_invalid_num, step_set_stop, bot, start)
    elif is_valid_limit(start, int(stop)) == -1:
        msg_invalid_limit = bot.send_message(message.chat.id,
                                             '\U0001F921 Правый предел ниже левого.\nВведите новый конец интвервала. ')
        bot.register_next_step_handler(msg_invalid_limit, step_set_stop, bot, start)
    elif is_valid_limit(start, int(stop)) == 0:
        msg_invalid_limit = bot.send_message(message.chat.id,
                                             '\U0001F921 Правый предел равен левому.\nВведите новый конец интвервала.')
        bot.register_next_step_handler(msg_invalid_limit, step_set_stop, bot, start)
    else:
        stop = int(stop)
        number = randint(start, stop)
        counter = 1
        msg_gen = bot.send_message(message.chat.id,
                                   f'\U0001F916 Случайное число в интервале от {start} до {stop} сгенерировано.\nТеперь попробуйте '
                                   f'его угадать \U0001F60F')
        bot.register_next_step_handler(msg_gen, step_set_new_num, bot, start, stop, number, counter)


def step_set_new_num(message, bot, start, stop, number, counter):
    number_guess = message.text
    if not is_valid_num(number_guess):
        msg_invalid_num = bot.send_message(message.chat.id,
                                           'Пожалуйста, введите целое число \U0001F921',
                                           reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg_invalid_num, step_set_new_num, bot, start, stop, number, counter)
    elif not is_inside_limits(start, stop, int(number_guess)):
        msg_outside_limits = bot.send_message(message.chat.id,
                                              f'{number_guess} за пределами интервала! \U0001F921 Пожалуйста, введите целое число от {start} до {stop}',
                                              reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg_outside_limits, step_set_new_num, bot, start, stop, number, counter)
    else:
        number_guess = int(number_guess)
        if number_guess > number:
            msg_num_too_big = bot.send_message(message.chat.id,
                                               '\U0001F62C Слишком много, попробуйте еще раз',
                                               reply_to_message_id=message.message_id)
            counter += 1
            bot.register_next_step_handler(msg_num_too_big, step_set_new_num, bot, start, stop, number, counter)

        elif number_guess < number:
            msg_num_too_small = bot.send_message(message.chat.id,
                                                 '\U0001F644 Слишком мало, попробуйте еще раз',
                                                 reply_to_message_id=message.message_id)
            counter += 1
            bot.register_next_step_handler(msg_num_too_small, step_set_new_num, bot, start, stop, number, counter)

        else:
            if 11 <= counter <= 19:
                counter_last_digit = counter
            elif counter > 19:
                counter_last_digit = counter % 10
            else:
                counter_last_digit = counter
            if counter_last_digit == 1:
                tries = 'попытку'
            elif counter_last_digit == 2 or counter_last_digit == 3 or counter_last_digit == 4:
                tries = 'попытки'
            else:
                tries = 'попыток'
            if counter <= 5:
                bot.send_message(message.chat.id, f'\U0001F92F Вы угадали всего за {counter} {tries}, поздравляем!',
                                 reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id,
                                 f'\U0001F973 Вы угадали всего за {counter} {tries}, неплохо\!\nНо можно лучше: в следующий раз пользуйтесь [методом дихотомии](https://ru.wikipedia.org/wiki/Дихотомия) или попробуйте интервал поменьше \U0001F609',
                                 parse_mode="MarkdownV2",
                                 reply_to_message_id=message.message_id)
