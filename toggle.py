def toggle_channel(connection, button, channel_number, send_command, type_orx_selected):
    # Controlla lo stato attuale del pulsante
    if button.text() == "OFF":
        # Se è "OFF", invia il comando appropriato, cambia il testo in "ON" e il colore in verde
        if type_orx_selected:
            command = f"ENORX{channel_number}+CR+LF"
        else:
            command = f"ENOTX{channel_number}+CR+LF"
        connection.send(command)
        print(command)

        button.setText("ON")
        button.setStyleSheet("background-color: lightgreen")
    else:
        # Se è "ON", invia il comando appropriato, cambia il testo in "OFF" e il colore in rosso
        if type_orx_selected:
            command = f"DISORX{channel_number}+CR+LF"
        else:
            command = f"DISOTX{channel_number}+CR+LF"
        connection.send(command)
        print(command)

        button.setText("OFF")
        button.setStyleSheet("")
