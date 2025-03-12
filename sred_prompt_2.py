import openai
import os
import numpy as np

openai.api_key = "openai-api-key"  
# openai.api_key = os.getenv("OPENAI_API_KEY")

# =========================================
# Knowledge Base and Embeddings Setup
# =========================================

knowledge_base = [
    "SR&ED is a Government of Canada program that offers tax incentives for R&D.",
    "Projects must show technological advancement, work done, and uncertainties.",
    "Keep in mind that strong claims usually have at least 3 uncertainties to form a project."
]

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
    """Fetch embeddings from OpenAI for the given text."""
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response['data'][0]['embedding']

# Precompute and store embeddings for each document in the knowledge base
knowledge_embeddings = [get_embedding(doc) for doc in knowledge_base]

def retrieve_relevant_documents(query: str, top_k: int = 2) -> list:
    """
    Find the top_k most relevant documents from knowledge_base
    based on cosine similarity or dot product. 
    """
    query_emb = get_embedding(query)
    
    # Compute dot product (could do full cosine similarity for more precision)
    similarities = []
    for idx, kb_emb in enumerate(knowledge_embeddings):
        sim_score = np.dot(query_emb, kb_emb)
        similarities.append((idx, sim_score))
    
    # Sort by descending similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k documents
    top_docs = [knowledge_base[idx] for (idx, _) in similarities[:top_k]]
    return top_docs

def retrieve_and_augment_prompt(prompt: str, top_k: int = 2) -> str:
    """
    Append the top_k relevant knowledge base docs to the prompt
    as 'Relevant Context'.
    """
    top_docs = retrieve_relevant_documents(prompt, top_k=top_k)
    context_text = "\n\nRelevant Context:\n" + "\n".join(top_docs) + "\n"
    return prompt + context_text

# =========================================
# Guidelines Text
# =========================================
guideline_text = {}

guideline_text["candidates_guideline"] = """ 
Given a list of threads(uncertainties) and their evaluations, identify which threads are candidates for a SR&ED project and group them, ensure that each group of threads(uncertainties) is sufficiently strong enough for a SR&ED project. 
Ideally no less than 3 threads per project. Return groups of threads that would make the strongest project claims with a project title, project description, and project thread ids. 
If there is not enough thread information to make multiple projects, return one project with all the threads.
Only return a single JSON object with an array of projects. Each project should have a title, description, and thread_ids, which is a list of the associated thread ids.
"""

guideline_text["part_1"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Technological Uncertainty" portion for Section B Project descriptions
Box 242 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.
"""

guideline_text["part_2"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Work Done" portion for Section B Project descriptions
Box 244 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.
"""

guideline_text["part_3"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Technological Advancements" portion for Section B Project descriptions
Box 246 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.
"""

# =========================================
# Helper to Call OpenAI Chat
# =========================================
def call_openai_api(prompt, model="gpt-4", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in drafting SR&ED reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

# =========================================
# Main Function with RAG Integration
# =========================================
def generate_sred_report(company_name, project_description):
    """
    Main function to generate the SR&ED report sections
    with RAG-based context augmentation for each stage.
    """
    
    # -------------------------
    # Step 1: Identify project candidates
    # -------------------------
    prompt_candidates = f"""
    {guideline_text['candidates_guideline']}
    Given the following project description:
    {project_description}
    Identify and return JSON-formatted project groups.
    """
    # Retrieve context & augment prompt
    prompt_candidates_aug = retrieve_and_augment_prompt(prompt_candidates, top_k=2)
    project_candidates = call_openai_api(prompt_candidates_aug)
    print("Project Candidates:\n", project_candidates)
    
    # -------------------------
    # Step 2: Generate technological uncertainties
    # -------------------------
    prompt_uncertainties = f"""
    {guideline_text['part_1']}
    Based on the project description:
    {project_description}
    Generate the technological uncertainties.
    """
    # Retrieve context & augment prompt
    prompt_uncertainties_aug = retrieve_and_augment_prompt(prompt_uncertainties, top_k=2)
    uncertainties = call_openai_api(prompt_uncertainties_aug)
    print("Technological Uncertainties:\n", uncertainties)
    
    # -------------------------
    # Step 3: Generate work done
    # -------------------------
    prompt_work_done = f"""
    {guideline_text['part_2']}
    Given the identified technological uncertainties:
    {uncertainties}
    Generate the work done in response to these uncertainties.
    """
    # Retrieve context & augment prompt
    prompt_work_done_aug = retrieve_and_augment_prompt(prompt_work_done, top_k=2)
    work_done = call_openai_api(prompt_work_done_aug)
    print("Work Done:\n", work_done)
    
    # -------------------------
    # Step 4: Generate technological advancements
    # -------------------------
    prompt_advancements = f"""
    {guideline_text['part_3']}
    Given the work done:
    {work_done}
    Generate the technological advancements achieved.
    """
    # Retrieve context & augment prompt
    prompt_advancements_aug = retrieve_and_augment_prompt(prompt_advancements, top_k=2)
    advancements = call_openai_api(prompt_advancements_aug)
    print("Technological Advancements:\n", advancements)
    
    return {
        "project_candidates": project_candidates,
        "technological_uncertainties": uncertainties,
        "work_done": work_done,
        "technological_advancements": advancements
    }

# =========================================
# Example 
# =========================================
if __name__ == "__main__":
    company = "TechCorp AI"
    project = "Developing a novel machine learning model for predictive maintenance in manufacturing."
    report = generate_sred_report(company, project)
    
    print("\n\n===== Final SR&ED Report Sections =====\n")
    print("Project Candidates (JSON):", report["project_candidates"])
    print("Technological Uncertainties:", report["technological_uncertainties"])
    print("Work Done:", report["work_done"])
    print("Technological Advancements:", report["technological_advancements"])
