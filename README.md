# Description
This script will run a centralised logging server which will bind to an IP address and port detailed in the .env configuration.

The current version extends the standard Python logging library and will be familiar to any Python coder. 

If you do not want this server available to other servers over the network ensure that the loopback address (127.0.0.1) is used in the configuration.

Any script that wants to send logs to the server must use the same LOG_SVR_HASH_KEY as the server, the hash is checked by the server before adding the log data to the log file, and if there is a mismatch the log data is discarded.

# Install Supervisor

Supervisor will automatically start/stop python scripts.  It will also restart scripts if they terminate abnormally.

```
apt-get install supervisor -y
```

Create a Supervisor config for the logging server

```
sudo nano /etc/supervisor/conf.d/loggingserver.conf
```

Example config:

```
[program:loggingserver]
directory=/apps/loggingserver/appdata/
command=/apps/loggingserver/venv/bin/python3 main.py
autostart=true
autorestart=true
```

Tell Supervisor to check for new configs

```
sudo supervisorctl reread
```

Tell Supervisor to enact the changes

```
sudo supervisorctl update
```

# Python Version

```
3.10
```

# Install

```
rename .envtemplate to .env

pip install -r requirements.txt
```

# Configuration

| .env Variable    | Description                    | Default   |
|------------------|:-------------------------------|:----------|
| LOG_SVR_HASH_KEY | Key used to generate data hash | None      |
| LOG_SVR_FILE     | Log file path                  | None      |
| LOG_SVR_IP       | Logging server IP address      | localhost |
| LOG_SVR_MAX_SIZE | Max size of log file in bytes  | 200000    |
| LOG_SVR_PORT     | Logging server port            | 9020      |
| LOG_SVR_DEBUG    | Logging server debug           | False     |


# Example Client

The client directory shows how to use the logging server from a python script.  The main thing to note is that SocketHandlerHMAC needs to be imported for it to work.

```
from handler import SocketHandlerHMAC
```