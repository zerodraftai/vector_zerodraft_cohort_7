from perform_chunking import perform_chunking_main
from generate_embeddings import generate_and_store_embeddings_main
import os
import boto3
from openai import OpenAI
import json
import redis

# ---------------- AWS Configuration ------------------- #
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# ---------------- S3 Configuration ------------------- #
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
aws_s3_bucket = 'vector-zerodraftai-collab-s3'
# ---------------- Redis Configuration ------------------- #
    # host='clustercfg.vector-zerodraftai-collab-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com',
redis_client = redis.StrictRedis(
    host='3.12.123.12',
    port=6379,
    decode_responses=True,
    ssl=False
)
# ---------------- OpenAI Configuration ------------------- #
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_client = OpenAI(api_key=openai_api_key)
# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
input_text_file_key = 'Input_data/transcript_sample_1.json'
output_chunk_file_key = f"Chunks/{input_text_file_key.split('/')[-1].replace('.txt', '_chunks.json')}"
# print (input_chunk_file_key)
try:
    perform_chunking_main(s3_client,aws_s3_bucket,input_text_file_key,output_chunk_file_key, "fixed", chunk_size=300)
except Exception as e:
    print ("The function perform_chunking_main failed due to ", e)
    import pdb;pdb.set_trace()

try:
    generate_and_store_embeddings_main(s3_client,aws_s3_bucket,output_chunk_file_key,redis_client,openai_api_client)
except Exception as e:
    print ("The function generate_and_store_embeddings_main failed due to ", e)
    import pdb;pdb.set_trace()

