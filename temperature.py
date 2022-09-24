def handle_temperature(bot,message):
    csv_file = 'c:\\Users\\Administrator\\eclipse-workspace\\gradus\\com\\temperature.csv'
    with open(csv_file, 'rU') as f:
        csvdata = csv.reader(f,delimiter=' ')
        for row in csvdata:
            temperature_tres = row[0]
            temperature_sensor = row[1]
            humidity_sensor = row[2]
    bot.send_message(message.chat.id, "The temperature is {} �C or {} °C and the humidity is {} %".format(temperature_tres,temperature_sensor,humidity_sensor))