import openai
def promt_for_company_and_project_name(query):
    import openai
import json

# OpenAI API Key (Replace with actual key)
OPENAI_API_KEY = "your-api-key"

def read_input_text_from_s3(s3_client,bucket_name, file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    # import pdb;pdb.set_trace()
    # transcript_text = "\n".join([entry["raw_text"] for entry in response["transcript"]])
    json_content = response['Body'].read().decode('utf-8')
    return json.loads(json_content)

def extract_company_and_project(openai_client,s3_client,bucket_name, file_key):
    transcript_text = read_input_text_from_s3(s3_client,bucket_name, file_key)
    transcript_text = "\n".join([entry["raw_text"] for entry in transcript_text["transcript"]])
    # import pdb;pdb.set_trace()
    # prompt = f"""
    # You are an intelligent assistant helping with information extraction.
    # Extract the client company name and the project name from the given call transcript.
    # The discussion is about an SRED report being prepared by our company for a client.

    # Return the result in the following JSON format:
    # {{
    #     "Client Company": "client company name",
    #     "Project Name": "project name"
    # }}

    # Transcript:
    # {input_text}

    # JSON Output:
    # """
    prompt = f"""
    The attached text contains a conversation between two people.
    Extract the company name and project description from the interview transcript:

    {transcript_text}

    Return the output as JSON with the format:
    {{
        "company_name": "...",
        "project_description": "..."
    }}
    """

    response = openai_client.chat.completions.create(
        model="o1",
        messages=[{"role": "system", "content": "You are an AI assistant that extracts structured data from text."},
            {"role": "system", "content": prompt}],
    )

    extracted_info = response.choices[0].message.content.strip()
    print (extracted_info)
    try:
        return json.loads(extracted_info)  # Convert JSON string to Python dict
    except json.JSONDecodeError:
        return {"Error": "Failed to parse response"}



# # Example Call Transcript
# transcript = """
# Hello John, this is Alice from TechConsult. We are working on the SRED report for GreenTech Innovations.
# We need more details about the project named Solar Efficiency Study.




