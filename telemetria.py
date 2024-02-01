import struct

#-----------------------------from
import random
import string
def generate_payload(length=160):
    # Genera una stringa casuale di una lunghezza specificata
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
#-----------------------------to

def request_data(connection):
    # Invia la richiesta
    command = 'ORXCHSDATA\r\n'
    #connection.send(command.encode())
#-----------------------------from
    payload = generate_payload()
    data = 'ORXCHSDATA' + payload + '\r\n'
    response = data
#-----------------------------to

    #response = connection.receive()

    # Estrai il payload dalla risposta
    if response.startswith('ORXCHSDATA') and response.endswith('\r\n'):
        payload = response[len('ORXCHSDATA'):-len('\r\n')]

        # Estrai i valori dai byte del payload
        values = struct.unpack('>' + 'H'*80, payload.encode())  # Usa 'H' per 2 byte (unsigned short)

        # Organizza i valori in gruppi di 5 (TOTCURR, LNACURR, PDCURR, BRDTEMP)
        data = [values[i:i+5] for i in range(0, len(values), 5)]

        return data

    else:
        print(f"Risposta non valida: {response}")
        return None
