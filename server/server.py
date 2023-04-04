import socket
from threading import Thread
import configparser
import urllib3
import json
import traceback
from datetime import datetime

config = configparser.ConfigParser()
config.read('config-server.ini')
host = config['server-config']['host']
port = int(config['server-config']['port'])
webhook_url = config['slack']['url'] + config['slack']['token']
log_dir = config['server-config']['log_pwd']
log_name = log_dir + 'cims-server/' + datetime.today().strftime('%d-%m-%Y') + '.log'

client_sockets = set()
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5)


def log_write(file, data):
    with open(file, 'a') as log:
        if data is not None:
            log.write(data)


def date_now_log():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def check_allowed_adress(check_adress):
    for val in config['allowed-hosts']:
        if check_adress == config['allowed-hosts'][val]:
            return True


def slack_notification(who, message, color):
    try:
        slack_data = {
            "attachments": [
                {
                    "title": who,
                    "color": color,
                    "fields": [
                        {
                            "value": message,
                        }
                    ]
                }
            ]
        }

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body=json.dumps(slack_data),
                                headers={'Content-Type': 'application/json'},
                                retries=False)
    except:
        traceback.print_exc()

    return True


def listen_agent(client_socket):
    down_server = 0
    while True:
        try:
            if check_allowed_adress(client_address[0]):
                if down_server == 0:
                    client_data = client_socket.recv(1024).decode("utf-8")
                    if client_data:
                        client_data = eval(client_data)
                        print(f'\n [Server]: {date_now_log()} Receive from: [{client_data[1]}]')
                        if len(client_data) >= 3:
                            if len(client_data[2]) == 0:
                                log_write(log_name,
                                          str(f"[SERVER]: {date_now_log()} client {client_address[0]} havn't services data\n"))
                                print(f"[SERVER]: {date_now_log()} client {client_address[0]} havn't services data")
                                slack_notification(f'SERVER',
                                                   f'{date_now_log()} client {client_address[0]} havnt services data',
                                                   '#f2c744')
                                log_write(log_name,
                                          str(f'[SERVER]: {date_now_log()} Stop receive data from {client_address[0]} while no data\n'))
                                print(
                                    f'[SERVER]: {date_now_log()} Stop receive data from {client_address[0]} while no data')
                                slack_notification(f'SERVER',
                                                   f'{date_now_log()} Stop receive data from {client_address[0]} while no data',
                                                   '#f2c744')
                                break
                            else:
                                for c_data in client_data[2]:

                                    if c_data[1] == False:
                                        down_server = 1
                                        print(f'SERVER',
                                              f'[{client_data[1]}]: {c_data[0]} service is DOWN({c_data[1]})')
                                        slack_notification(f'SERVER',
                                                           f'[{client_data[1]}]: {c_data[0]} service is DOWN({c_data[1]})',
                                                           '#e01e5a')
                                        log_write(log_name,
                                                  str(f'SERVER [{client_data[1]}]: {c_data[0]} service is DOWN({c_data[1]})\n'))
                        else:
                            log_write(log_name,
                                      str(f"[SERVER]: {date_now_log()} client {client_address[0]} havn't services data\n"))
                            print(f"[SERVER]: {date_now_log()} client {client_address[0]} havn't services data")
                            slack_notification(f'SERVER',
                                               f'{date_now_log()} client {client_address[0]} havnt services data',
                                               '#f2c744')

                            log_write(log_name,
                                      str(f'[SERVER]: {date_now_log()} Stop receive data from {client_address[0]} while no data\n'))
                            print(
                                f'[SERVER]: {date_now_log()} Stop receive data from {client_address[0]} while no data')
                            slack_notification(f'SERVER',
                                               f'{date_now_log()} Stop receive data from {client_address[0]} while no data',
                                               '#f2c744')
                            break
                    if not client_data:
                        # if we lose connect with client - stop receive
                        log_write(log_name,
                                  str(f'[SERVER]: {date_now_log()} Lose connection with client {client_address[0]}\n'))
                        print(f'[SERVER]: {date_now_log()} Lose connection with client {client_address[0]}')
                        slack_notification(f'SERVER',
                                           f'{date_now_log()} Lose connection with client {client_address[0]}',
                                           '#e01e5a')
                        break
                else:
                    # Stop receive data from client where one service is False(down)
                    log_write(log_name,
                              str(f'[SERVER]: {date_now_log()} Stop receive data from {client_data[1]} while service Down\n'))
                    print(f'[SERVER]: {date_now_log()} Stop receive data from {client_data[1]} while service Down')
                    slack_notification(
                        f'SERVER', f'{date_now_log()} Stop receive data from {client_data[1]} while service Down',
                        '#f2c744')
                    break
            else:
                log_write(log_name,
                          str(f'[SERVER]: {date_now_log()} Unconfirmed {client_address} try to connect. Rejected\n'))
                print(f'[SERVER]: {date_now_log()} Unconfirmed {client_address} try to connect. Rejected')
                break
        except Exception as err:
            log_write(log_name, str(f'[SERVER]: {date_now_log()} Error: {err}\n'))
            print(f'[SERVER]: {date_now_log()} Error: {err}')
            slack_notification(f'SERVER', f'{date_now_log()} Error: {err}', '#e01e5a')
            client_sockets.remove(client_socket)


log_write(log_name, str(f'[SERVER]: {date_now_log()} Listening as {host}:{port}\n'))
print(f'[SERVER]: {date_now_log()} Listening as {host}:{port}')
slack_notification(f'SERVER', f'{date_now_log()} Listening as {host}:{port}', '#36a64f')

while True:
    client_socket, client_address = sock.accept()
    log_write(log_name, str(f'[SERVER]: {date_now_log()} Allowed {client_address} connected.\n'))
    print(f'[SERVER]: {date_now_log()} Allowed  {client_address} connected.')
    slack_notification(f'SERVER', f'{date_now_log()} Allowed  {client_address} connected.', '#36a64f')
    client_sockets.add(client_socket)
    t = Thread(target=listen_agent, args=(client_socket,))
    t.daemon = True
    t.start()

sock.close()
