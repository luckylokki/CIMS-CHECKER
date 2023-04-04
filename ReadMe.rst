###############################################################################
                            SERVICES STATUS CHECKER
###############################################################################

This is a training project for checking statuses.

Getting started
===============

#. Download the code base
#. Make sure tha you have installed Python3.8, python3.8-venv

Preparing
===============
The project consist from two parts.

#. Server part
#. Client part

You need only one server runned.

The client part must be run on the servers you want to monitor

Server part
=====================
Edit config-server.ini:

.. code-block::

    [server-config]
    host = 0.0.0.0 #0.0.0.0 for run on all
    port = 9997 #port you want
    log_pwd = /var/log/ #folder where will be created folder with logs
    [allowed-hosts]
    host1 = IP #ip lcient, add your clients here
    host2 = IP #etc...
    [slack]
    url = https://hooks.slack.com/services/
    token = YOUR_SLACK_TOKEN

After finish edit config-server.ini, you must run
.. code-block::
    python3 install-serves.py

That's create all folders,copy program to /etc/cims-server, create Daemon and run it

Client part
=====================
Edit config-client.ini:

.. code-block::
    [agent-config]
    name = Client1 #Name of your client server
    log_pwd = /var/log/ #folder where will be created folder with logs
    [server-config]
    host = SERVER_IP #ip or domain adress of your server
    port = 9997 #port of your server
    log_pwd = /var/log/ #folder where will be folder with logs
    [services]
    service_name_0 = nginx #service you want monitor
    service_name_1 = zabbix-agent
    [slack]
    url = https://hooks.slack.com/services/
    token = YOUR_SLACK_TOKEN

You can add services as much as you like, just add new:
example: service_name_2 = MyService
You need copy "service_name" and change number, this all.
Services means that command will be look - systemctl status "YourService"

After finish edit config-server.ini, you must run
.. code-block::
    python3 install-client.py

That's create all folders,copy program to /etc/cims-client, create Daemon and run it.
