import redis
import json
import boto3
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# redis_host = "localhost"
# redis_port = 6379
# redis_db = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=False)

def read_chunks_from_s3(s3_client,bucket_name,file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    chunked_text = response["Body"].read().decode("utf-8")
    chunks = json.loads(chunked_text)
    return chunks

def embed_chunks(vector_index_value,openai_api_client,chunks,model = 'text-embedding-ada-002'):
    embeddings = {}
    for i,chunk in enumerate(chunks):
        response = openai_api_client.embeddings.create(
            input=chunk,
            model=model
        )
        # import pdb;pdb.set_trace()
        embeddings[f"chunk_{vector_index_value}:{i}"] = response.data[0].embedding
    return embeddings

def store_embeddings_in_redis(embeddings,redis_client):
    for key, embedding in embeddings.items():
        redis_client.hset(
            key,
            mapping={"vector": np.array(embedding).tobytes()}
        )
    # for key, embedding in embeddings.items():
    #     print (key)
    #     redis_client.set(key, json.dumps(embedding))

def generate_and_store_embeddings_main(s3_client,aws_s3_bucket,s3_file_key,redis_client,openai_api_client,vector_index_value):
    try:
        chunks = read_chunks_from_s3(s3_client,aws_s3_bucket,s3_file_key)
    except Exception as e:
        print ("The function read_chunks_from_s3 failed due to ", e)
        # import pdb;pdb.set_trace()
    try:
        embeddings = embed_chunks(vector_index_value,openai_api_client,chunks)
    except Exception as e:
        print ("The function embed_chunks failed due to ", e)
        # import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    try:
        store_embeddings_in_redis(embeddings,redis_client)
    except Exception as e:
        print ("The function store_embeddings_in_redis failed due to ", e)


        # import pdb;pdb.set_trace()
# for id, embedding in zip(id, embeddings):
#     redis_db.hset(f"clinical_trial:{id}", mapping={"embedding": embedding.tobytes()})

# np.save("profile_descriptions.npy", profile_descriptions)