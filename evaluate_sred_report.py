from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
import json

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

Return your answer in this JSON format:

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

def generate_ground_truth_text(vector_db,generated_sred_report,openai_client):
    system_prompt = "You are an expert SR&ED consultant."
    retrieved_chunks = vector_db.search(query=generated_sred_report, top_k=5)
    context = "\n".join(chunk['text'] for chunk in retrieved_chunks)
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

def evaluate_using_meteor(generated_sred_report,openai_client,vector_db):
    """
    Evaluate ground text (using RAG) and the generated SRED report using METEOR score.

    Args:
        reference (str): The ground text.
        hypothesis (str): The hypothesis text to evaluate.

    Returns:
        float: The METEOR score.
    """
    ground_text_data = None
    try:
        ground_text_data=generate_ground_truth_text(vector_db,generated_sred_report,openai_client)
    except Exception as e:
        print ("The function generate_ground_truth_text failed due to ", e)
        pass
    if ground_text_data is None:
        print ("Evaluation using METEOR failed due to missing ground truth data")
        return None

    reference_tokens = word_tokenize(ground_text_data)
    hypothesis_tokens = word_tokenize(generated_sred_report)
    return meteor_score([reference_tokens], hypothesis_tokens)

def evaluate_using_llm_as_judge(vector_db,transcript_text,generated_sred_report,openai_client,):
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
        print("⚠️ Failed to parse JSON. Here's the raw output:\n")
        print(output_text)
        return None

def evaluate_sred_report_main(generated_sred_report,vector_db,open_ai_client,transcript_text):
    # Example reference and hypothesis texts
    reference_text = "The quick brown fox jumps over the lazy dog."
    hypothesis_text = "A fast brown fox leaps over a lazy dog."


    # Calculate METEOR score
    score = evaluate_using_meteor(generated_sred_report, open_ai_client,vector_db)
    score = evaluate_using_llm_as_judge(vector_db,transcript_text,generated_sred_report,open_ai_client)
    print(f"METEOR Score: {score}")