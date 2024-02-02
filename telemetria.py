import struct
import random
import string

def generate_payload(length):
    # Genera una stringa casuale di una lunghezza specificata
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def request_data(connection, type_orx_selected):
    # Invia la richiesta
    if type_orx_selected:
        command = 'ORXCHSDATA\r\n'
        payload_length = 160
        gruppi = 4
    else:
        command = 'OTXCHSDATA\r\n'
        payload_length = 140
        gruppi = 5
    print(command)
    print(payload_length)

    #connection.send(command.encode())

    payload = generate_payload(payload_length)
    data = command.strip() + payload + '\r\n'
    response = data
    print(response)
    #response = connection.receive()

    # Estrai il payload dalla risposta
    if response.startswith(command.strip()) and response.endswith('\r\n'):
        payload = response[len(command.strip()):-len('\r\n')]

        # Estrai i valori dai byte del payload
        values = struct.unpack('>' + 'H'*(payload_length//2), payload.encode())  # Usa 'H' per 2 byte (unsigned short)

        # Organizza i valori in gruppi di 5 (TOTCURR, LNACURR, PDCURR, BRDTEMP)
        data = [values[i:i+gruppi] for i in range(0, len(values), gruppi)]

        return data

    else:
        print(f"Risposta non valida: {response}")
        return None
