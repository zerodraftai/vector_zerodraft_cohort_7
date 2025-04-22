import openai

guideline_text = {}

# -----------------------------------------
# GUIDELINES & SAMPLES
# -----------------------------------------

guideline_text["candidates_guideline"] = """
You are given a set of threads (technological or scientific uncertainties) along with their evaluations. Your task is to group these threads into one or more SR&ED project(s). Each SR&ED project must:

1. Contain at least three threads, if possible.
2. Have a clear, cohesive technological objective tying the threads together.
3. If there are insufficient threads to form multiple distinct projects, place them all into one project.

Return your results as a single JSON object containing an array called "projects".
Each element in "projects" must be an object with exactly three keys:
- "title": A concise, descriptive title for the project.
- "description": A brief summary (1–2 sentences) explaining the common SR&ED focus.
- "thread_ids": A list of the thread IDs included in the project.

**Important**:
- Do not include any explanation, commentary, or extra text outside of the JSON object.
- Only produce valid JSON.

**Example JSON output**:

{
  "projects": [
    {
      "title": "High-Precision Sensor Calibration Project",
      "description": "A set of SR&ED activities aiming to reduce sensor noise and improve calibration techniques.",
      "thread_ids": [1, 3, 5]
    },
    {
      "title": "Advanced Data Processing Pipeline",
      "description": "Work on new algorithms and data structures to handle large-scale streaming data in real time.",
      "thread_ids": [2, 4, 6]
    }
  ]
}
"""


guideline_text["part_1"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Technological Uncertainty" portion for Section B Project descriptions
Box 242 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.

SR&ED Project Guidelines - Section B Project Descriptions - Technological Uncertainties

--What scientific or technological uncertainties did you attempt to overcome?--

General description of what the project was about. For example: <The main technological objective of this project was to>. In the course of the project, the following technological uncertainties were encountered:
A numbered list of uncertainties the company resolved or tried to resolve in the course of the project.Each uncertainty should state what the issue was and why that issue could not be resolved by conventional means.
At the end it should say something like: <It was unknown what means we could employ to resolve the above issue.>
The company failed to do a. The conventional means to resolve this issue would be b. However, we couldn’t because c.
It was unknown what means we could employ to resolve the above issue.

"""

guideline_text["part_2"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Work Done" portion for Section B Project descriptions
Box 244 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.

SR&ED Project Guidelines - Section B Project Descriptions - Work Done

--What work did you perform in the tax year to overcome the scientific or technological uncertainties described?--
(the systematic investigation or search)

Numbered paragraphs corresponding with the numbered list in the Technological Uncertainties section. Each paragraph includes the following:
a) Description of a hypothesis the company formulated to resolve the uncertainty (approach, idea, assumption) can be one or more per uncertainty
b) Description of a prototype that was designed and manufactured/implemented to verify the correctness of the hypothesis, can be one or more per hypothesis
c) Description of the prototype tests/trials and their results (good, not good enough, not good at all, fixed one problem but created another, etc.) – can be one or more than one per prototype
d) “Bottom line”: either the issue (uncertainty) was resolved, or the efforts were abandoned (failure), or the efforts will continue in the future.

Either
The project was _____________ completed.
The project will continue in the next fiscal year in order to ***
The project was abandoned
"""

guideline_text["part_3"] = """
You are a SR&ED consultant and writer. Given the provided uncertainties and context, write the "Technological Advancements" portion for Section B Project descriptions
Box 246 of the T661 form. Follow the guideline and use the sample project writing as a reference for the structure.

SR&ED Project Guidelines - Section B Project Descriptions - Technological Advancements

--What scientific or technological advancements did you achieve or attempt to achieve as a result of the work described?--

The the results of the project. The focus is on what the company learned to do so that it can do the same or similar thing in the future without redoing the R&D described.
As a result of this project, <Company> gained practical knowledge and experience in <whatever>. In the course of the project, the team achieved the following technological advancements:
A numbered list of technological advancements the company sought to achieve where each advancement’s number corresponds to an uncertainty number and a number of a paragraph in the Work Done section.
Each advancement must state the following: a)	what the company sought to achieve (with emphasis on “generic”, reusable solutions).b) 	how the advancement was fully or partially achieved (by what technological means) or how the company failed to achieve it

"""

# Additional full guideline text if we need them:

guideline_text["project_samples_part_1"] = """
---SAMPLES BEGIN ---

-SAMPLE 1-
[Technological Uncertainties text sample...]

-SAMPLE 2-
[Technological Uncertainties text sample...]

---SAMPLES END---
"""

guideline_text["project_samples_part_2"] = """
---SAMPLES BEGIN ---

-SAMPLE 1-
[Work Done text sample...]

-SAMPLE 2-
[Work Done text sample...]

---SAMPLES END---
"""

guideline_text["project_samples_part_3"] = """
---SAMPLES BEGIN ---

-SAMPLE 1-
[Technological Advancements text sample...]

-SAMPLE 2-
[Technological Advancements text sample...]

---SAMPLES END---
"""

guideline_text["project_guideline"] = """SR&ED Project Guidelines - Section B Project Descriptions

--Technological Uncertainties--
[Content of overarching guideline...]

--Work Done--
[Content of overarching guideline...]

--Technological Advancements--
[Content of overarching guideline...]
"""

guideline_text["project_sample_tech_1"] = """
--SAMPLE BEGIN--
[Large sample text for a project #1...]
--SAMPLE END--
"""

guideline_text["project_sample_tech_2"] = """
--SAMPLE BEGIN--
[Large sample text for a project #2...]
--SAMPLE END--
"""

guideline_text["project_sample_tech_3"] = """
--SAMPLE BEGIN--
[Large sample text for a project #3...]
--SAMPLE END--
"""

guideline_text["project_sample_mech_eng_1"] = """
--SAMPLE BEGIN--
[Mechanical Engineering sample text...]
--SAMPLE END--
"""

# -----------------------------------------
# OPENAI HELPER FUNCTION
# -----------------------------------------
def call_openai_api(openai_client,prompt, model="gpt-4", temperature=0.7):
    """
    Helper function to call the OpenAI ChatCompletion endpoint with the given prompt.
    Adjust the model name and temperature as desired.
    """
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You are an expert in drafting SR&ED reports."},
                  {"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content
    # return response.choices[0].message.content.strip()

# -----------------------------------------
# MAIN SR&ED REPORT GENERATION FUNCTION
# -----------------------------------------
def generate_sred_report(openai_client,project_description):
    """
    This function orchestrates the steps to generate an SR&ED-style report:
      1. Identify candidate SR&ED projects (if multiple).
      2. Generate the 'Technological Uncertainty' section.
      3. Generate the 'Work Done' section.
      4. Generate the 'Technological Advancements' section.

    :param project_description: A textual description or context about the project or uncertainties.
    :return: A dictionary containing:
        - 'project_candidates': JSON-formatted string of potential SR&ED project groupings
        - 'technological_uncertainties': Draft text for Box 242
        - 'work_done': Draft text for Box 244
        - 'technological_advancements': Draft text for Box 246
    """
    # Step 1: Identify project candidates (threads grouping)
    prompt_candidates = f"""
    {guideline_text['candidates_guideline']}
    Given the following project description:
    {project_description}
    Identify and return JSON-formatted project groups.
    """
    project_candidates = call_openai_api(openai_client,prompt_candidates)

    # Step 2: Generate technological uncertainties
    prompt_uncertainties = f"""
    {guideline_text['part_1']}
    Based on the project description:
    {project_description}
    Generate the technological uncertainties.
    """
    uncertainties = call_openai_api(openai_client,prompt_uncertainties)

    # Step 3: Generate work done
    prompt_work_done = f"""
    {guideline_text['part_2']}
    Given the identified technological uncertainties:
    {uncertainties}
    Generate the work done in response to these uncertainties.
    """
    work_done = call_openai_api(openai_client,prompt_work_done)

    # Step 4: Generate technological advancements
    prompt_advancements = f"""
    {guideline_text['part_3']}
    Given the work done:
    {work_done}
    Generate the technological advancements achieved.
    """
    advancements = call_openai_api(openai_client,prompt_advancements)

    return {
        "project_candidates": project_candidates,
        "technological_uncertainties": uncertainties,
        "work_done": work_done,
        "technological_advancements": advancements
    }

# -----------------------------------------
# EXAMPLE USAGE
# -----------------------------------------
# if __name__ == "__main__":
#     example_project_description = "Developing a novel machine learning model for predictive maintenance in manufacturing."
#     report = generate_sred_report(example_project_description)
#     print("Project Candidates (JSON):")
#     print(report["project_candidates"])
#     print("\n--- Technological Uncertainties ---\n", report["technological_uncertainties"])
#     print("\n--- Work Done ---\n", report["work_done"])
#     print("\n--- Technological Advancements ---\n", report["technological_advancements"])
