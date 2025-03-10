import redis
# host='clustercfg.vector-zerodraftai-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com',
redis_client = redis.StrictRedis(
    host = '3.12.123.12',
    port=6379,
    decode_responses=True,
    ssl=False
)
# clustercfg.vector-zerodraftai-collab-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com:6379
try:
    print("Pinging Redis...")
    response = redis_client.ping()
    print("Connected to Redis:", response)
except Exception as e:
    print("Connection failed:", e)
redis_client.set("test_key", "Redis is working on AWS!")
value = redis_client.get("test_key")

print("Redis Test Success:", value)

# clustercfg.vector-zerodraftai-collab-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com:6379