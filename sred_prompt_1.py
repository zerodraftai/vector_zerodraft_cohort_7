import openai

guideline_text = {}

guideline_text["candidates_guideline"] = """ Given a list of threads(uncertainties) and their evaluations, identify which threads are candidates for a SR&ED project and group them, ensure that each group of threads(uncertainties) is sufficiently strong enough for a SR&ED project.
Ideally no less than 3 threads per project. Return groups of threads that would make the strongest project claims with a project title, project description, and project thread ids. If there is not enough thread information to make multiple projects, return one project with all the threads.
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

def call_openai_api(prompt, model="gpt-4", temperature=0.7):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You are an expert in drafting SR&ED reports."},
                  {"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content

def generate_sred_report(company_name, project_description):
    # Step 1: Identify project candidates
    prompt_candidates = f"""
    {guideline_text['candidates_guideline']}
    Given the following project description:
    {project_description}
    Identify and return JSON-formatted project groups.
    """
    project_candidates = call_openai_api(prompt_candidates)
    print("Project Candidates:\n", project_candidates)

    # Step 2: Generate technological uncertainties
    prompt_uncertainties = f"""
    {guideline_text['part_1']}
    Based on the project description:
    {project_description}
    Generate the technological uncertainties.
    """
    uncertainties = call_openai_api(prompt_uncertainties)
    print("Technological Uncertainties:\n", uncertainties)

    # Step 3: Generate work done
    prompt_work_done = f"""
    {guideline_text['part_2']}
    Given the identified technological uncertainties:
    {uncertainties}
    Generate the work done in response to these uncertainties.
    """
    work_done = call_openai_api(prompt_work_done)
    print("Work Done:\n", work_done)

    # Step 4: Generate technological advancements
    prompt_advancements = f"""
    {guideline_text['part_3']}
    Given the work done:
    {work_done}
    Generate the technological advancements achieved.
    """
    advancements = call_openai_api(prompt_advancements)
    print("Technological Advancements:\n", advancements)

    return {
        "project_candidates": project_candidates,
        "technological_uncertainties": uncertainties,
        "work_done": work_done,
        "technological_advancements": advancements
    }

# Example usage
# company = "TechCorp AI"
# project_description = "Developing a novel machine learning model for predictive maintenance in manufacturing."
# report = generate_sred_report(company, project_description)