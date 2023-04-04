import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config-server.ini')
log_dir = config['server-config']['log_pwd']
subprocess.call("mkdir cims-server", shell=True, cwd='/etc/')
subprocess.call("mkdir cims-server", shell=True, cwd=log_dir)
subprocess.call("cp -r cims-server.service /etc/systemd/system/", shell=True)
subprocess.call("cp -r * /etc/cims-server", shell=True)
subprocess.call("rm -f /etc/cims-server/install-server.py", shell=True)
subprocess.call("python3 -m venv venv", shell=True, cwd='/etc/cims-server/')
cmd = 'source /etc/cims-server/venv/bin/activate; pip install -r requirements.txt; deactivate'
subprocess.call(cmd, shell=True, executable='/bin/bash')
subprocess.call("systemctl enable cims-server", shell=True)
subprocess.call("systemctl daemon-reload", shell=True)
subprocess.call("systemctl start cims-server", shell=True)
