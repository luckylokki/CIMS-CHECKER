import subprocess

class MyService():

    def __init__(self, service):
        self.service = service

    def get_service(self):
        return self.service

    def check_service_status(self):

        status = subprocess.call('sudo systemctl status ' + self.service + ' > /dev/null', shell=True)

        if status == 0:
            return str(self.service), True
        else:
            return str(self.service), False
