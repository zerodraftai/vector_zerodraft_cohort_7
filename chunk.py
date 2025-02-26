import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
# import boto3
# import json

nltk.download('punkt')

# ---------------- S3 Configuration ------------------- #
# AWS_ACCESS_KEY = "your-access-key"
# AWS_SECRET_KEY = "your-secret-key"
# SOURCE_BUCKET = "your-source-bucket"
# DEST_BUCKET = "your-destination-bucket"

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY
# )
# ----------------------------------------------------- #

def fixed_chunking(text: str, chunk_size: int = 500):
    words = word_tokenize(text)
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def semantic_chunking(text: str, max_chunk_size: int = 500):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = None  

    for sentence in sentences:
        if current_chunk is None:  
            current_chunk = sentence
        elif len(current_chunk) + len(sentence) + 1 < max_chunk_size:  
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

long_text = """I recently purchased this laptop, and I must say, it’s an excellent choice for both work and gaming. 
The battery life is impressive, lasting nearly 10 hours on a single charge. The keyboard feels premium, and the screen resolution is crisp. 
However, I did face some minor issues with the touchpad being a bit unresponsive at times. Overall, it's a solid device and well worth the price.
The sound quality is also fantastic, providing a deep bass experience. But the fan noise can get quite loud under heavy loads, which is a little annoying.
Customer support was helpful when I needed assistance with initial setup. I'd recommend this laptop to anyone looking for a powerful and affordable machine."""


chunks_1 = fixed_chunking(long_text, chunk_size=30)
chunks_2 = semantic_chunking(long_text, max_chunk_size=30)

for i, chunk in enumerate(chunks_1):
    print(f"Chunk {i+1}: {chunk}\n")

for i, chunk in enumerate(chunks_2):
    print(f"Chunk {i+1}: {chunk}\n")




# --------------------------- Read Text from S3 --------------------------- #
# def read_text_from_s3(bucket_name, file_key):
#     response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
#     return response['Body'].read().decode('utf-8')


# --------------------------- Store Chunks in S3 --------------------------- #
# def store_chunks_in_s3(bucket_name, file_key, chunks):
#     chunked_text = json.dumps(chunks)
#     s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=chunked_text.encode('utf-8'))
#     print(f"Chunks stored in S3: {bucket_name}/{file_key}")


# --------------------------- Process Text from S3 --------------------------- #
# def process_text_from_s3(file_key, chunking_type="fixed", chunk_size=500):
#     print(f"Processing {file_key} from {SOURCE_BUCKET}...")

    # Read text from S3
#     text = read_text_from_s3(SOURCE_BUCKET, file_key)

    # Choose chunking method
#     if chunking_type == "fixed":
#         chunks = fixed_chunking(text, chunk_size)
#     elif chunking_type == "semantic":
#         chunks = semantic_chunking(text, chunk_size)
#     else:
#         raise ValueError("Invalid chunking_type. Use 'fixed' or 'semantic'.")

    # Store the chunks back to S3
#     output_file_key = f"processed_chunks/{file_key.split('/')[-1].replace('.txt', '_chunks.json')}"
#     store_chunks_in_s3(DEST_BUCKET, output_file_key, chunks)

#     print(f"Processed {len(chunks)} chunks successfully!")


# --------------------------- Example Usage --------------------------- #
# process_text_from_s3("uploads/sample_text.txt", chunking_type="semantic", chunk_size=300)

