import redis
import json
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
import os

# ---------------- AWS Configuration ------------------- #
# AWS_ACCESS_KEY = "your-access-key"
# AWS_SECRET_KEY = "your-secret-key"
# SOURCE_BUCKET = "your-source-bucket"
# DEST_BUCKET = "your-destination-bucket"

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY
# )

# redis_client = redis.Redis(
#     host="your-redis-endpoint",  # AWS ElastiCache Redis endpoint
#     port=6379,  # Default Redis port
#     decode_responses=True  # Ensures stored values are human-readable
# )


#redis_host =
# ----------------------------------------------------- #

# ---------------- OpenAI Configuration ------------------- #
openai_api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")


redis_host = "localhost"
redis_port = 6379
redis_db = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=False)


def read_chunks_from_s3(bucket_name, file_key):
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    chunked_text = response["Body"].read().decode("utf-8")
    chunks = json.loads(chunked_text)
    return chunks

def embed_chunks(chunks,model = 'text-embedding-ada-002'):
    embeddings = []
        for chunk in chunks:
            response = openai.Embedding.create(
                input=chunk,
                model=model
            )
            embeddings[f"chunk:{i}"] = response["data"][0]["embedding"]
        return embeddings

def store_embeddings_in_redis(embeddings):
    for key, embedding in embeddings.items():
        redis_client.set(key, json.dumps(embedding))


bucket_name = "your-bucket-name"
file_key = "path/to/chunks.json"

try:
    chunks = read_chunks_from_s3(bucket_name, file_key)
except Exception as e:
    print ("The function read_chunks_from_s3 failed due to ", e)
    import pdb;pdb.set_trace()
try:
    embeddings = embed_chunks(chunks)
except Exception as e:
    print ("The function embed_chunks failed due to ", e)
    import pdb;pdb.set_trace()
try:
    store_embeddings_in_redis(embeddings)
except Exception as e:
    print ("The function store_embeddings_in_redis failed due to ", e)
    import pdb;pdb.set_trace()
# for id, embedding in zip(id, embeddings):
#     redis_db.hset(f"clinical_trial:{id}", mapping={"embedding": embedding.tobytes()})

# np.save("profile_descriptions.npy", profile_descriptions)