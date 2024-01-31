def send_command(connection, command, channel):
    if channel == 0:
        message = command + '\r\n'
        print(message);
    else:
        message = command + str(channel) + '\r\n'
        print(message);
    connection.send(message)
