import redis
import openai
import numpy as np
from langchain_redis import RedisVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
import os
load_dotenv()
# def search_vector(vector_index_name,redis_client,query_embedding: np.ndarray, top_k: int = 10):
#     query_vector = np.array(query_embedding,dtype=np.float32).tobytes()
#     try:
#             result = redis_client.execute_command(
#             "FT.SEARCH", vector_index_name, "*=>[KNN {} @embedding $vec AS score]".format(top_k),
#             "SORTBY", "score", "PARAMS", "2", "vec", query_vector, "RETURN", "2", "score", "text"
#         )
#     except redis.RedisError as e:
#         print(f"Error searching index: {e}")
#         import pdb;pdb.set_trace()
#     return result
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
def rewrite_query(query,openai_client):
    prompt = f"""
    You are an AI assistant helping to retrieve information from call transcripts between SRED consultant and a client company. The summarized output would be used for RAG
    The user asked: '{query}'.

    Rewrite the question to be more specific based on how a SRED consultant would ask the question that would help them to draft a SRED grant.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert at query refinement."},
                  {"role": "user", "content": prompt}]
    )
    # import pdb;pdb.set_trace()
    return response.choices[0].message.content

def generate_proj_desc_from_top_20_results(top_20_ranked_results, openai_client):
    combined_texts = "\n\n".join([f"Snippet {i+1}: {text}" for i, (k, (score, text)) in enumerate(top_20_ranked_results.items())])

    prompt = f"""
    You are a technical writer specializing in Canadian SR&ED (Scientific Research and Experimental Development) reports.

    Based on the following 20 transcript excerpts from discussions between a consultant and a third-party company, generate a concise **Project Description** suitable for inclusion in a SR&ED report. Your summary should cover:

    1. The technological or scientific objectives of the project
    2. The key problems or uncertainties addressed
    3. A high-level summary of the work performed (experiments, iterations, models, etc.)
    4. Any technological advancement or innovation attempted

    Avoid repeating the same points. Write clearly and in a professional tone suited for government reporting.

    Transcript Snippets:
    {combined_texts}

    SR&ED Project Description:
    """

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes SR&ED project descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def get_top_20_result(search_results,openai_client):
    if len(search_results) > 1:  # Ensure results exist
        # print (search_results)
        top_20_ranked_results = {}
        for i in range(1, len(search_results), 2):
            key = search_results[i]
            try:
                score = search_results[i + 1][1]
            except Exception as e:
                import pdb;pdb.set_trace()
            text = search_results[i + 1][3]
            top_20_ranked_results[key] = (score, text)

        #sort the dictionary based on the score
        # import pdb;pdb.set_trace()
        top_20_results = []
        # total_results = min(20, (len(search_results) - 1) // 2)
        # top_result_key = search_results[20]  # The first result key
        # score = search_results[2][1]  # Score is in ['score', value] format
        # print(f"✅ Top 1 Result: {top_result_key} (Score: {score})")
        # return top_20_ranked_results
    else:
        print("⚠️ No results found. Using backup retrieval.")
        return "No Project description found."

    if len(top_20_ranked_results.keys()) > 0:
        try:
            top_20_summarised_proj_desc = generate_proj_desc_from_top_20_results(top_20_ranked_results,openai_client)
        except Exception as e:
            print ("The function generate_proj_desc_from_top_20_results failed due to ", e)
        return top_20_summarised_proj_desc
    else:
        return "No Project description found."

def rag_pipeline_main(vector_index_name,redis_client, redis_index, openai_api_key,openai_client):
    openai.api_key = openai_api_key

    # Use the updated OpenAI Embeddings
    embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")

    # vectorstore = RedisVectorStore.from_existing_index(
    #     redis_url='redis://'+redis_url,
    #     index_name=redis_index,
    #     embedding=embedding_function
    # )

    query = "Describe the project in detail particularly the description"

    try:
        query = rewrite_query(query,openai_client)
    except Exception as e:
        print("The function rewrite_query failed due to ", e)
    # query_embedding = embedding_function(query)
    print ("\n The RAG pipeline rewritten query:\n" + query +"\n")
    query_embedding = embedding_function.embed_query(query)
    # Perform similarity search
    # retrieved_docs = vectorstore.similarity_search(query, k=5)
    results = search_vector(vector_index_name,redis_client,query_embedding)
    # retrieved_texts = [doc.page_content for doc in retrieved_docs]
    top_20_summarised_proj_desc = get_top_20_result(results,openai_client)
    # import pdb;pdb.set_trace()
    # print ("\n: results",top_20_summarised_proj_desc)

    # print("Retrieved Transcripts:", retrieved_texts)
    return top_20_summarised_proj_desc
