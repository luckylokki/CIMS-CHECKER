import socket
import configparser
from modules import MyService
import time
import urllib3
import json
import traceback
from datetime import datetime

config = configparser.ConfigParser()
config.read('config-client.ini')
host = config['server-config']['host']
port = int(config['server-config']['port'])
name = config['agent-config']['name']
webhook_url = config['slack']['url'] + config['slack']['token']
log_dir = config['agent-config']['log_pwd']
log_name = log_dir + 'cims-client/' + datetime.today().strftime('%d-%m-%Y') + '.log'
service_list = []


def log_write(file, data):
    with open(file, 'a') as log:
        log.write(data)


def slack_notification(who, message, color):
    try:
        slack_data = {
            "attachments": [
                {
                    "color": color,
                    "fields": [
                        {
                            "title": who,
                            "value": message,
                        }
                    ]
                }
            ]
        }
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body=json.dumps(slack_data),
                                headers={'Content-Type': 'application/json'},
                                retries=False)
    except:
        traceback.print_exc()

    return True


def check_services():
    for key in config['services']:
        service_list.append(MyService(config['services'][key]).check_service_status())
    return service_list


def date_now_log():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


sock = socket.socket()
sock.connect((host, port))
connected = True

slack_notification(f'{name}', f'{date_now_log()} Connected to server {host}:{port}', '#36a64f')
print(f'[!] {date_now_log()} Connected to server {host}:{port}')
log_write(log_name, str(f'[!] {date_now_log()} Connected to server {host}:{port}\n'))
while True:
    try:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        service_list.clear()
        data = str([date_now, name, check_services()])
        print(f'[+] {date_now_log()} Send {data}')
        sock.send(data.encode("utf-8"))
        time.sleep(2)
    except socket.error:
        connected = False
        sock.close()
        slack_notification(f'{name}', f'{date_now_log()} Connection with {host}:{port} lost!!!Try reconnecting...',
                           '#e01e5a')
        print(f'[!] {date_now_log()} Connection with {host}:{port} lost!!!Try reconnecting...')
        log_write(log_name, str(f'[!] {date_now_log()} Connection with {host}:{port} lost!!!Try reconnecting...\n'))
        while not connected:
            sock = socket.socket()
            try:
                sock.connect((host, port))
                connected = True
                slack_notification(f'{name}', f'{date_now_log()} {name} Re-connected successful', '#f2c744')
                print(f'[!] {date_now_log()} {name} Re-connected to {host}:{port} successful')
                log_write(log_name, str(f'[!] {date_now_log()} {name} Re-connected to {host}:{port} successful\n'))
            except socket.error:
                time.sleep(2)
sock.close()
