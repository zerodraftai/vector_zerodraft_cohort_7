import redis
import json
import boto3
import numpy as np
import os


# redis_host = "localhost"
# redis_port = 6379
# redis_db = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=False)

def read_chunks_from_s3(s3_client,bucket_name,file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    chunked_text = response["Body"].read().decode("utf-8")
    chunks = json.loads(chunked_text)
    chunks_dict = {}
    chunks_dict = {f"chunk_{i}": chunk for i, chunk in enumerate(chunks)}
    return chunks_dict

def embed_chunks(vector_index_value,openai_api_client,chunks_dict,model = 'text-embedding-ada-002'):
    embeddings = {}
    for chunk_index,chunk_value in chunks_dict.items():
        response = openai_api_client.embeddings.create(
            input=chunk_value,
            model=model
        )
        # import pdb;pdb.set_trace()
        embeddings[chunk_index] = response.data[0].embedding
    # import pdb;pdb.set_trace()
    return embeddings

def store_embeddings_in_redis(embeddings, chunks_dict,redis_client, vector_index_name):
    for chunk_index, embedding in embeddings.items():
        redis_key = f"embedding:{chunk_index}"

        redis_client.hset(
            redis_key,
            mapping={"embedding": np.array(embedding, dtype=np.float32).tobytes(),
                     "text": chunks_dict[chunk_index]}
        )

    print(f"Stored {len(embeddings)} vectors in Redis under the '{vector_index_name}' index.")



def generate_and_store_embeddings_main(s3_client,aws_s3_bucket,s3_file_key,redis_client,openai_api_client,vector_index_value):
    try:
        chunks_dict = read_chunks_from_s3(s3_client,aws_s3_bucket,s3_file_key)
    except Exception as e:
        print ("The function read_chunks_from_s3 failed due to ", e)

    try:
        embeddings = embed_chunks(vector_index_value,openai_api_client,chunks_dict)
    except Exception as e:
        print ("The function embed_chunks failed due to ", e)

    # import pdb;pdb.set_trace()
    try:
        store_embeddings_in_redis(embeddings,chunks_dict,redis_client,vector_index_value)
    except Exception as e:
        print ("The function store_embeddings_in_redis failed due to ", e)


        # import pdb;pdb.set_trace()
# for id, embedding in zip(id, embeddings):
#     redis_db.hset(f"clinical_trial:{id}", mapping={"embedding": embedding.tobytes()})

# np.save("profile_descriptions.npy", profile_descriptions)