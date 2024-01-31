def set_ip(connection, ip1, ip2, ip3, ip4):
    # Crea il payload
    payload = f"{ip1}.{ip2}.{ip3}.{ip4}"
    #print(payload)

    # Crea il comando
    command = f"IPADDSET{payload}" + '\r\n'
    #print(command)

    # Invia il comando
    response = connection.send(command)

    # Controlla la risposta
    if response == "IPSETACK" + '\r\n':
        #print("L'indirizzo IP è stato impostato correttamente.")
        return "L'indirizzo IP è stato impostato correttamente."
    else:
        #print("Si è verificato un errore durante l'impostazione dell'indirizzo IP.")
        return "Si è verificato un errore durante l'impostazione dell'indirizzo IP."
