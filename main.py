from perform_chunking import perform_chunking_main
from generate_embeddings import generate_and_store_embeddings_main
from rag_pipeline_to_generate_proj_description import rag_pipeline_main
from sred_prompt_1 import generate_sred_report
from retrieve_company_and_project_name import extract_company_and_project
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
redis_url = '3.145.98.52'
redis_client = redis.StrictRedis(
    host=redis_url,
    port=6379,
    decode_responses=True,
    ssl=False
)
vector_index_value = 'my_vector_index_18'
def create_vector_index(redis_client):
    redis_client.execute_command(
        "FT.CREATE", vector_index_value, "ON", "HASH",
        "PREFIX", "1", "embedding:",
        "SCHEMA",
        "vector", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "1536",  # Set your embedding dimension
        "DISTANCE_METRIC", "COSINE"
    )

# Run the function once to create the index
create_vector_index(redis_client)


# ---------------- Lambda Configuration ------------------- #
lambda_client = boto3.client('lambda', region_name="us-east-2")


# ---------------- OpenAI Configuration ------------------- #
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_client = OpenAI(api_key=openai_api_key)
# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
input_text_file_key = 'Input_data/transcript_sample_1.json'
output_chunk_file_key = f"Chunks/{input_text_file_key.split('/')[-1].replace('.txt', '_chunks.json')}"
# print (input_chunk_file_key)
try:
    print ("Performing chunking...")
    perform_chunking_main(s3_client,aws_s3_bucket,input_text_file_key,output_chunk_file_key, "fixed", chunk_size=300)
except Exception as e:
    print ("The function perform_chunking_main failed due to ", e)
    import pdb;pdb.set_trace()

try:
    print ("Generating and storing embeddings...")
    generate_and_store_embeddings_main(s3_client,aws_s3_bucket,output_chunk_file_key,redis_client,openai_api_client,vector_index_value)
except Exception as e:
    print ("The function generate_and_store_embeddings_main failed due to ", e)
    import pdb;pdb.set_trace()

try:
    print ("Running RAG pipeline...")
    retrieved_texts = rag_pipeline_main(redis_url,'vector-zerodraftai-redis-vectordb-0001',openai_api_key,openai_api_client)
except Exception as e:
    print ("The function rag_pipeline_main failed due to ", e)

# try:
#     company_name_project_description = extract_company_and_project(openai_api_client,s3_client,aws_s3_bucket,input_text_file_key,)
#     company_name = company_name_project_description['company_name']
#     project_description = company_name_project_description['project_description']
# except Exception as e:
#     print ("The function retrieve_company_and_project_name failed due to ", e)
# print (company_name,project_description)
# try:
#     sred_report = generate_sred_report(company_name,project_description)
# except Exception as e:
#     print ("The function generate_sred_report failed due to ", e)


