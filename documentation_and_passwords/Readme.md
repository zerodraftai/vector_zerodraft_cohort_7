Command to start socate for automatic forwarding of the port:
socat TCP-LISTEN:6379,fork,reuseaddr TCP:clustercfg.vector-zerodraftai-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com:6379


Finding process on a port:
sudo lsof -i :6379


Commands to start the redis-proxy service:
sudo systemctl daemon-reload
sudo systemctl enable redis-proxy
sudo systemctl start redis-proxy
sudo systemctl status redis-proxy

Location of the redis-proxy service:sudo nano /etc/systemd/system/redis-proxy.service


Removing the vectors present in the redis vector db:
redis-cli -h clustercfg.vector-zerodraftai-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com -p 6379 -a <password> FLUSHALL

Things to do
#implement mlflow and langsmith to log artifacts and experiments and even results.
#implement evaluation metrics for the models
#   - meteor score
#   - llm as a judge

postgres creds
postgres, postrgres
postgres endpoint
database-1.cp08y8cawkhj.us-east-2.rds.amazonaws.com