import connessione
def toggle_channel(connection, button, channel_number, send_command):
    # Controlla lo stato attuale del pulsante
    if button.text() == "OFF":
        # Se è "OFF", invia il comando "ENOTX+m+CR+LF", cambia il testo in "ON" e il colore in verde
        connection.send(f"ENOTX{channel_number}+CR+LF")
        print(f"ENOTX{channel_number}+CR+LF")

        button.setText("ON")
        button.setStyleSheet("background-color: lightgreen")
    else:
        # Se è "ON", invia il comando "DISOTX+m+CR+LF", cambia il testo in "OFF" e il colore in rosso
        connection.send(f"DISOTX{channel_number}+CR+LF")
        print(f"DISOTX{channel_number}+CR+LF")

        button.setText("OFF")
        button.setStyleSheet("")
