#Command to start socate for automatic forwarding of the port:
socat TCP-LISTEN:6379,fork,reuseaddr TCP:clustercfg.vector-zerodraftai-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com:6379


#Finding process on a port:
sudo lsof -i :6379


#Commands to start the redis-proxy service:
sudo systemctl daemon-reload
sudo systemctl enable redis-proxy
sudo systemctl start redis-proxy
sudo systemctl status redis-proxy

#Location of the redis-proxy service:
sudo nano /etc/systemd/system/redis-proxy.service

#Postgres database connection details
postgres creds
postgres, postrgres
postgres endpoint
database-1.cp08y8cawkhj.us-east-2.rds.amazonaws.com


[Unit]
Description=Redis proxy using socat
After=network.target

[Service]
User=ubuntu
Restart=always
ExecStart=/usr/bin/socat TCP-LISTEN:6379,reuseaddr,fork TCP:clustercfg.vector-zerodraftai-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com:6379

[Install]
WantedBy=multi-user.target
