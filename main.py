from perform_chunking import perform_chunking_main
from generate_embeddings import generate_and_store_embeddings_main
from rag_pipeline_to_generate_proj_description import rag_pipeline_main
from sred_prompt_1 import generate_sred_report
from retrieve_company_and_project_name import extract_company_and_project
from evaluate_sred_report import evaluate_sred_report_main
from helper_function import write_input_text_file_to_s3
import streamlit as st
import os
import boto3
from openai import OpenAI
import json
import redis
def main(input_transcripts_text,input_file_name):
    print ("==============================")
    print ("Inside the main function")
    print ("==============================")

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
    ec2_public_ip = "18.222.184.174"
    # ---------------- Redis Configuration ------------------- #
        # host='clustercfg.vector-zerodraftai-collab-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com',
    redis_url = ec2_public_ip
    redis_client = redis.StrictRedis(
        host=redis_url,
        port=6379,
        decode_responses=True,
        ssl=False
    )
    vector_index_value = 'my_vector_index_3'

    def create_vector_index(redis_client, vector_index_name, embedding_dim=1536):
        existing_indexes = redis_client.execute_command("FT._LIST")

        if vector_index_name in existing_indexes:
            print(f"✅ Index '{vector_index_name}' already exists.")
            return

        # Proceed to create the index if it doesn't exist
        try:
            redis_client.execute_command(
                "FT.CREATE", vector_index_name, "ON", "HASH",
                "PREFIX", "1", "embedding:",  # Ensure stored keys match this pattern
                "SCHEMA",
                "embedding", "VECTOR", "FLAT", "6",
                "TYPE", "FLOAT32",
                "DIM", embedding_dim,
                "DISTANCE_METRIC", "COSINE",
                "text", "TEXT"
            )
            print(f"✅ Vector index '{vector_index_name}' created successfully.")
        except redis.RedisError as e:
            print(f"❌ Redis Error: {e}")

    # Try again
    create_vector_index(redis_client, vector_index_value)
    # print(redis_client.execute_command("FT._LIST"))

    # Run the function once to create the index
    # create_vector_index(redis_client,vector_index_value)


    # ---------------- Lambda Configuration ------------------- #
    lambda_client = boto3.client('lambda', region_name="us-east-2")


    # ---------------- OpenAI Configuration ------------------- #
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_client = OpenAI(api_key=openai_api_key)
    # OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    input_text_file_key = 'Input_data/{input_file_name}'
    output_chunk_file_key = f"Chunks/{input_text_file_key.split('/')[-1].replace('.txt', '_chunks.json')}"
    # print (input_chunk_file_key)
    try:
        print ("Performing chunking...")
        perform_chunking_main(s3_client,aws_s3_bucket,input_text_file_key,output_chunk_file_key, "semantic", chunk_size=300)
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
        top_20_summarised_proj_desc = rag_pipeline_main(vector_index_value,redis_client,'vector-zerodraftai-redis-vectordb-0001',openai_api_key,openai_api_client)
    except Exception as e:
        print ("The function rag_pipeline_main failed due to ", e)
        raise(e)
    # import pdb;pdb.set_trace()
    if top_20_summarised_proj_desc == "No Project description found.":
        print ("No project description found. Using the input transcripts text as the project description.")
        try:
            company_name_project_description = extract_company_and_project(openai_api_client,s3_client,aws_s3_bucket,input_text_file_key,)
            company_name = company_name_project_description['company_name']
            project_description = company_name_project_description['project_description']
        except Exception as e:
            print ("The function retrieve_company_and_project_name failed due to ", e)
        # print (company_name,project_description)
    else:
        project_description = top_20_summarised_proj_desc
    # import pdb;pdb.set_trace()
    print ("==============================")
    print ("Project description: ", project_description)
    print ("==============================")
    try:
        # company_name = "xyz tech company"
        sred_report = generate_sred_report(openai_api_client,project_description)
    except Exception as e:
        print ("The function generate_sred_report failed due to ", e)
    sred_report_text = ""
    for key, value in sred_report.items():
        sred_report_text = sred_report_text + key + ": " + value + "\n\n"

    #write the sred report and input file to a text file and upload it to S3

    try:
        write_input_text_file_to_s3(s3_client,aws_s3_bucket,f'sred_reports/SRED_report_{input_file_name}.txt',sred_report_text)
        print("SRED report written to S3 bucket")
    except Exception as e:
        print ("Failed to write the report to S3 due to ", e)
        import pdb;pdb.set_trace()
    try:
        write_input_text_file_to_s3(s3_client,aws_s3_bucket,input_text_file_key,input_transcripts_text)
        print("Input transcripts written to S3 bucket")
    except Exception as e:
        print ("Failed to write the input transcripts to S3 due to ", e)
        import pdb;pdb.set_trace()
    try:
        with open('sred_report.txt', 'w') as f:
            f.write(sred_report_text)
        print("SRED report written to sred_report.txt")
    except Exception as e:
        print ("Failed to write the report to a text file due to ", e)
        import pdb;pdb.set_trace()

    #Evaluate the generated SRED report
    sred_report_scores_dict = {}
    counter = 0
    for key,value in sred_report.items():
        if key == "project_candidates":
            # import pdb;pdb.set_trace()
            value_json = json.loads(value)
            value = value_json['projects'][0]['description'] + "\n" + value_json['projects'][0]['description']
        # counter += 1
        # if counter >2:
        #     break
        sred_report_thread = key + ": " + value
        current_thread = key
        meteor_score = None
        llm_as_judge_score = None
        try:
            print ("Evaluating the generated SRED report...")
            # current_thread,s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,generated_sred_report,vector_db,open_ai_client,transcript_text
            meteor_score, llm_as_judge_score = evaluate_sred_report_main(current_thread,s3_client,aws_s3_bucket,input_text_file_key,vector_index_value,sred_report_thread,redis_client,openai_api_client,input_transcripts_text)
        except Exception as e:
            print ("The function evaluate_sred_report_main failed due to ", e)
            raise(e)
            import pdb;pdb.set_trace()
        sred_report_scores_dict[key] = [value, meteor_score, llm_as_judge_score]
    return sred_report_scores_dict
# if __name__ == "__main__":
#     # Run the main function
#     result = main()
#     print(result)




