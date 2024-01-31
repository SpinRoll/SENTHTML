import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    ip = config.get('Connection', 'ip')
    port = config.get('Connection', 'port')
    mac = config.get('Connection', 'mac')

    commands = [config.get('Command', key) for key in config['Command']]

    return ip, port, mac, commands