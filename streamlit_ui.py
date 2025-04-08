import streamlit as st
from main import main
from openai import OpenAI
import pandas as pd
import os
import boto3
import redis
import json
from dotenv import load_dotenv
load_dotenv()
from helper_function import write_input_text_file_to_s3, read_input_text_from_s3
from evaluate_sred_report import evaluate_sred_report_main
from edit_sred_report import edit_sred_report_main

input_text_file_key = 'Input_data/transcript_sample_1.json'
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_client = OpenAI(api_key=openai_api_key)
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
ec2_public_ip = "18.191.129.243"
# ---------------- Redis Configuration ------------------- #
    # host='clustercfg.vector-zerodraftai-collab-redis-vectordb.dkvbaf.memorydb.us-east-2.amazonaws.com',
redis_url = ec2_public_ip
redis_client = redis.StrictRedis(
    host=redis_url,
    port=6379,
    decode_responses=True,
    ssl=False
)
vector_index_value = 'my_vector_index_4'
# input_transcripts_text = read_input_text_from_s3(s3_client,aws_s3_bucket,input_text_file_key)
complete_sred_report = None

def generate_report(input_transcripts_text,input_file_name):
    ##Copy the contents of the AWS S3 bucket to a different folder.

    sred_report_scores_dict = None
    try:
        sred_report_scores_dict = main(input_transcripts_text,input_file_name)
    except Exception as e:
        raise(e)
        print("The function main failed due to ", e)
        import pdb;pdb.set_trace()
        raise(e)
    #convert dict to a list
    sred_report_scores_list = []
    for key, value in sred_report_scores_dict.items():
        thread = {
            "id": key,
            "content": value[0],
            "meteor_score": value[1],
            "llm_judge_score": value[2]
        }
        sred_report_scores_list.append(thread)
    sred_report_scores_list_content = ""
    for thread in sred_report_scores_list:
        sred_report_scores_list_content += f"Thread ID: {thread['id']}\n"
        sred_report_scores_list_content += f"Content: {thread['content']}\n"
    return sred_report_scores_list,sred_report_scores_list_content

# Dummy LLM revision logic (replace with actual LLM call)
# user_prompt,complete_sred_report,sred_thread,open_ai_client,redis_client,trancripts
def regenerate_thread_content(original, comment,complete_sred_report,open_ai_client,trancripts):
    try:
        # user_prompt,complete_sred_report,sred_thread,open_ai_client,trancripts
        revised_content = edit_sred_report_main(comment,complete_sred_report,original,open_ai_client,trancripts)
    except Exception as e:
        print("The function edit_sred_report_main failed due to ", e)
        import pdb;pdb.set_trace()
        raise(e)
    return revised_content

# Streamlit App UI
st.set_page_config(page_title="SR&ED Report Generator & Editor", layout="wide")
st.title("📄 SR&ED Report Generator + Editor")

# ---------------- NEW FILE UPLOAD SECTION ---------------- #
uploaded_file = st.file_uploader(
    "Upload the transcripts between Zerodraft and client company in JSON file",
    type="json"
)

# Initialize session state
if "report" not in st.session_state:
    st.session_state.report = None
if "regenerated" not in st.session_state:
    st.session_state.regenerated = {}
# Step 1: Button to generate report
if st.button("🧠 Generate SR&ED Report"):
    if uploaded_file is not None:
        input_transcripts_text = uploaded_file.read()
        input_file_name = uploaded_file.name
        uploaded_file_key = f"uploaded_current_transcripts/{uploaded_file.name}"
        # , bucket_name, file_key, content
        write_input_text_file_to_s3(s3_client,aws_s3_bucket,uploaded_file_key,input_transcripts_text)
        # st.session_state.input_transcripts_text = bytes_data.decode("utf-8")
        st.success("Transcript file uploaded and read successfully!")
    else:
        st.error("Please upload a JSON transcript file first.")
        st.stop()
    with st.spinner("Generating SR&ED report..."):
        sred_report_scores_list, sred_report_scores_list_content = generate_report(input_transcripts_text,input_file_name)
        st.session_state.report = sred_report_scores_list
        complete_sred_report = sred_report_scores_list_content
        st.success("Report generated! You can now review and edit each section.")

# Step 2: Display report editor UI
if st.session_state.report:
    st.markdown("## ✏️ Edit Report Threads")
    input_text_file_key = f"uploaded_current_transcripts/{uploaded_file.name}"
    input_transcripts_text = read_input_text_from_s3(s3_client,aws_s3_bucket,input_text_file_key)
    for idx,thread in enumerate(st.session_state.report):
        meteor_score = thread["meteor_score"]
        llm_judge_score = thread["llm_judge_score"]
        st.markdown("---")
        st.subheader(f"Section ID: {thread['id']}")

        current_content = st.session_state.regenerated.get(thread["id"], {}).get("content", thread["content"])
        current_meteor = st.session_state.regenerated.get(thread["id"], {}).get("meteor_score", thread["meteor_score"])
        current_llm_judge = st.session_state.regenerated.get(thread["id"], {}).get("llm_judge_score", thread["llm_judge_score"])

        # Show original or regenerated content
        # display_text = st.session_state.regenerated.get(thread["id"], thread["content"])
        st.markdown(f"**Content:**\n\n{current_content}")
        st.markdown(f"- METEOR Score: `{current_meteor}`")
        # current_llm_judge_df = display_json_as_table(llm_judge_score)
        st.markdown("**LLM-as-a-Judge Score:**")
        st.markdown(llm_judge_score)

        # Comment + Regeneration
        comment_key = f"comment_{thread['id']}"
        regenerate_key = f"regenerate_{thread['id']}"
        comment = st.text_area(f"💬 Add comment to revise this section:", key=comment_key)

        if st.button("🔁 Regenerate Section", key=regenerate_key):
            with st.spinner("Regenerating thread..."):
            # original, comment,complete_sred_report,open_ai_client,trancripts
                revised_content = regenerate_thread_content(current_content,comment,complete_sred_report,openai_api_client,input_transcripts_text)
                meteor_score, llm_judge_score = None, None
                meteor_score, llm_judge_score = evaluate_sred_report_main(thread['id'],s3_client,aws_s3_bucket,input_text_file_key,vector_index_value,revised_content,redis_client,openai_api_client,input_transcripts_text)
                st.session_state.regenerated[thread["id"]] = {
                    "content": revised_content,
                    "meteor_score": meteor_score,
                    "llm_judge_score": llm_judge_score
                }
                st.success(f"Thread {thread['id']} regenerated and re-evaluated!")
                st.experimental_rerun()


# Optional: Add export/save button
# if st.session_state.regenerated:
#     if st.button("📤 Export Revised Report"):
#         revised_report = {
#             thread["id"]: {
#                 "content": st.session_state.regenerated.get(thread["id"], {}).get("content", thread["content"]),
#                 "meteor_score": st.session_state.regenerated.get(thread["id"], {}).get("meteor_score", thread["meteor_score"]),
#                 "llm_judge_score": st.session_state.regenerated.get(thread["id"], {}).get("llm_judge_score", thread["llm_judge_score"]),
#             }
#             for thread in st.session_state.report
#         }
#         st.json(revised_report)
