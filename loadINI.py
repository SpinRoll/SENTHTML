import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    ip = config.get('Connection', 'ip')
    port = config.get('Connection', 'port')
    mac = config.get('Connection', 'mac')
    set_ip = config.get('Set-IP', 'ip')

    commands = [config.get('Command', key) for key in config['Command']]

    otx_thresholds = {key: [float(x) for x in config.get('Soglie-OTX', key).split(';')] for key in config['Soglie-OTX']}
    orx_thresholds = {key: [float(x) for x in config.get('Soglie-ORX', key).split(';')] for key in config['Soglie-ORX']}

    return ip, port, mac, commands, set_ip, otx_thresholds, orx_thresholds