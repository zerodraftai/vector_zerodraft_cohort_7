from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
from langchain_openai import OpenAIEmbeddings
import json
import re
import redis
import numpy as np

def read_input_text_from_s3(s3_client,bucket_name, file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')
def build_prompt_for_llm_judge(transcript_text, generated_summary):
    return f"""
    You are an expert SR&ED evaluator for the CRA.

    Given:
    1. A raw transcript between a consultant and a company.
    2. A generated SR&ED summary report.

    Your task is to evaluate how well the generated summary reflects the key elements present in the transcript, using the official SR&ED criteria:
    - Technological Uncertainty
    - Conventional Means
    - Hypothesis
    - Prototype
    - Test Methodology
    - Test Results

    For each criterion:
    - Assign a score from 0 to 5 (as per CRA rubric)
    - Justify the score with clear evidence from the transcript
    - Flag any hallucinations or missing details
    - Note if anything important in the transcript was ignored or misrepresented

    --- Transcript ---
    {transcript_text}

    --- Generated SR&ED Summary ---
    {generated_summary}

    Return your answer in this JSON format strictly:

    {{
    "technological_uncertainty": {{ "score": X, "reason": "..." }},
    "conventional_means": {{ "score": X, "reason": "..." }},
    "hypothesis": {{ "score": X, "reason": "..." }},
    "prototype": {{ "score": X, "reason": "..." }},
    "test_methodology": {{ "score": X, "reason": "..." }},
    "test_results": {{ "score": X, "reason": "..." }},
    "hallucination_check": "None" or "Yes, explain what was hallucinated",
    "missing_info_check": "None" or "Yes, explain what was missing",
    "overall_summary": "How well does the generated report align with the transcript?"
    }}
    """
def search_vector(vector_index_name, redis_client, query_embedding: np.ndarray, top_k: int = 10):
    query_vector = np.array(query_embedding, dtype=np.float32).tobytes()

    try:
        result = redis_client.execute_command(
            "FT.SEARCH", vector_index_name,
            "*=>[KNN {} @embedding $vec AS score]".format(top_k),  # Ensure @embedding matches your stored field name
            "SORTBY", "score",
            "PARAMS", "2", "vec", query_vector,
            "RETURN", "2", "score", "text"  # Retrieve both score and text
        )
        return result
    except redis.RedisError as e:
        print(f"Error searching index: {e}")
        return None
def generate_ground_truth_text(s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,vector_db,generated_sred_report,openai_client,query_embedding):
    system_prompt = "You are an expert SR&ED consultant."
    # retrieved_chunks = vector_db.search(query=generated_sred_report, top_k=5)
    # import pdb;pdb.set_trace()
    try:
        retrieved_chunks = search_vector(vector_index_name, vector_db, query_embedding)
    except Exception as e:
        print ("The function search_vector failed due to ", e)
        pass
    if retrieved_chunks is None:
        print ("The function search_vector failed to retrieve any chunks")
        context = read_input_text_from_s3(s3_client,aws_s3_bucket,input_text_file_key)
    else:
        context = ''
        for index_chunk in range(2,len(retrieved_chunks),2):
            # import pdb;pdb.set_trace()
            context += retrieved_chunks[index_chunk][3]
    user_prompt = (
        "Given the following transcript between a company and a consultant, extract the most "
        "relevant details that would go into an official SR&ED report section. Summarize only "
        "what would likely be written in the final report. Output a clean paragraph in professional report style.\n\n"
        f"Transcript:\n{context}"
    )
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
def rewrite_query(query,openai_client):
    prompt = f"""
    You are an AI assistant helping to summarize information from call transcripts between SRED consultant and a client company. The summarized output would be used for RAG
    The user asked: '{query}'.

    Rewrite the question to a summarized version.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert at query refinement."},
                  {"role": "user", "content": prompt}]
    )
    # import pdb;pdb.set_trace()
    return response.choices[0].message.content
def evaluate_using_meteor(s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,generated_sred_report,openai_client,vector_db):
    """
    Evaluate ground text (using RAG) and the generated SRED report using METEOR score.

    Args:
        reference (str): The ground text.
        hypothesis (str): The hypothesis text to evaluate.

    Returns:
        float: The METEOR score.
    """
    ground_text_data = None
    embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")
    # import pdb;pdb.set_trace()
    # query = " ".join([v for k,v in generated_sred_report.items()])
    query = generated_sred_report
    try:
        rewritten_query = rewrite_query(query,openai_client)
    except Exception as e:
        print ("The function rewrite_query failed due to ", e)
    query_embedding = embedding_function.embed_query(rewritten_query)
    try:
        ground_text_data=generate_ground_truth_text(s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,vector_db,generated_sred_report,openai_client,query_embedding)
    except Exception as e:
        print ("The function generate_ground_truth_text failed due to ", e)
        pass
    if ground_text_data is None:
        print ("Evaluation using METEOR failed due to missing ground truth data")
        return None
    print (f"\nGround text data: \n {ground_text_data}\n")
    # print (f"Generated SRED report: {generated_sred_report}")
    print (f"\n Rewritten query: \n {rewritten_query}\n")
    reference_tokens = word_tokenize(ground_text_data)
    hypothesis_tokens = word_tokenize(rewritten_query)
    return meteor_score([reference_tokens], hypothesis_tokens)
def fix_and_load_sred_json(output_text):
    output_text = re.sub(r"^```(?:json)?\n|\n```$", "", output_text.strip())
    output_text = re.sub(r"\{\{", "{", output_text)
    output_text = re.sub(r"\}\}", "}", output_text)
    return json.loads(output_text)
def evaluate_using_llm_as_judge(transcript_text,generated_sred_report,openai_client,):
    try:
        prompt = build_prompt_for_llm_judge(transcript_text, generated_sred_report)
    except Exception as e:
        print ("The function build_prompt_for_llm_judge failed due to ", e)
    response = openai_client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    output_text = response.choices[0].message.content.strip()
    try:
        result = json.loads(output_text)
        return result
    except json.JSONDecodeError:
        try:
            json_result = fix_and_load_sred_json(output_text)
            return json_result
        except Exception as e:
            import pdb;pdb.set_trace()
            print("⚠️ Failed to parse JSON. Here's the raw output:\n")
            # print(output_text)
        return None

def evaluate_sred_report_main(s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,generated_sred_report,vector_db,open_ai_client,transcript_text):
    # Example reference and hypothesis texts
    reference_text = "The quick brown fox jumps over the lazy dog."
    hypothesis_text = "A fast brown fox leaps over a lazy dog."
    # Calculate METEOR score
    try:
        meteor_score = evaluate_using_meteor(s3_client,aws_s3_bucket,input_text_file_key,vector_index_name,generated_sred_report, open_ai_client,vector_db)
    except Exception as e:
        print ("The function evaluate_using_meteor failed due to ", e)

    try:
        llm_judge_score = evaluate_using_llm_as_judge(transcript_text,generated_sred_report,open_ai_client)
    except Exception as e:
        print ("The function evaluate_using_llm_as_judge failed")
    print(f"METEOR Score: {meteor_score}")
    print (f"LLM Judge Score: {llm_judge_score}")
    return meteor_score, llm_judge_score