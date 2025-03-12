import redis
import openai
import numpy as np
from langchain_redis import RedisVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
import os
load_dotenv()
def search_vector(vector_index_name,redis_client,query_embedding: np.ndarray, top_k: int = 5):
    query_vector = query_embedding.tobytes()

    result = redis_client.execute_command(
        "FT.SEARCH", vector_index_name, "*=>[KNN {} @vector $vec AS score]".format(top_k),
        "SORTBY", "score", "PARAMS", "2", "vec", query_vector, "RETURN", "1", "score"
    )

    return result

def embed_chunks(openai_api_client,chunks,model = 'text-embedding-ada-002'):
    embeddings = {}
    for i,chunk in enumerate(chunks):
        response = openai_api_client.embeddings.create(
            input=chunk,
            model=model
        )
        # import pdb;pdb.set_trace()
        embeddings[f"chunk:{i}"] = response.data[0].embedding
    return embeddings

def rewrite_query(query,openai_client):
    prompt = f"""
    You are an AI assistant helping to retrieve information from call transcripts between SRED consultant and a client company.
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

def rag_pipeline_main(redis_url, redis_index, openai_api_key,openai_client):
    openai.api_key = openai_api_key

    # Use the updated OpenAI Embeddings
    embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")

    # vectorstore = RedisVectorStore.from_existing_index(
    #     redis_url='redis://'+redis_url,
    #     index_name=redis_index,
    #     embedding=embedding_function
    # )

    query = "Describe the project in detail."

    try:
        query = rewrite_query(query,openai_client)
    except Exception as e:
        print("The function rewrite_query failed due to ", e)
    query_embedding = embedding_function(query)
    # Perform similarity search
    # retrieved_docs = vectorstore.similarity_search(query, k=5)
    results = search_vector(query_embedding)
    # retrieved_texts = [doc.page_content for doc in retrieved_docs]
    import pdb;pdb.set_trace()
    print ("\n: results",results)

    # print("Retrieved Transcripts:", retrieved_texts)
    return results
