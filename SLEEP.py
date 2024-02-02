def sleep_channel(connection, button, channel_number, send_command, type_orx_selected):
    # Controlla lo stato attuale del pulsante
    if button.text() == "W":
        # Se è "OFF", invia il comando appropriato, cambia il testo in "ON" e il colore in verde
        if type_orx_selected:
            command = f"SLEEPORX{channel_number}+CR+LF"
        else:
            command = f"SLEEPOTX{channel_number}+CR+LF"
        connection.send(command)
        print(command)

        button.setText("S")
        button.setStyleSheet("background-color: lightyellow")
    else:
        # Se è "ON", invia il comando appropriato, cambia il testo in "OFF" e il colore in rosso
        if type_orx_selected:
            command = f"WAKEORX{channel_number}+CR+LF"
        else:
            command = f"WAKEOTX{channel_number}+CR+LF"
        connection.send(command)
        print(command)

        button.setText("W")
        button.setStyleSheet("background-color: lightblue")
