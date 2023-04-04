import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config-client.ini')
log_dir = config['agent-config']['log_pwd']
subprocess.call("mkdir cims-client", shell=True, cwd='/etc/')
subprocess.call("mkdir cims-client", shell=True, cwd=log_dir)
subprocess.call("cp -r cims-client.service /etc/systemd/system/", shell=True)
subprocess.call("cp -r * /etc/cims-client", shell=True)
subprocess.call("rm -f /etc/cims-client/install-client.py", shell=True)
subprocess.call("python3 -m venv venv", shell=True, cwd='/etc/cims-client/')
cmd = 'source /etc/cims-client/venv/bin/activate; pip install -r requirements.txt; deactivate'
subprocess.call(cmd, shell=True, executable='/bin/bash')
subprocess.call("systemctl enable cims-client", shell=True)
subprocess.call("systemctl daemon-reload", shell=True)
subprocess.call("systemctl start cims-client", shell=True)
