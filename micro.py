def send_micro_command(connection, command):
    # Aggiungi il terminatore alla fine del comando
    command += '\r\n'

    # Invia il comando
    response = connection.send(command)

    # Controlla la risposta
    if command + "ACK" + '\r\n' in response:
        return f"Il comando {command} è stato impostato correttamente."
    else:
        return f"Si è verificato un errore durante l'impostazione del comando {command}."