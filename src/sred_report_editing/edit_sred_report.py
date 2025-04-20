
def generate_edit_prompt(user_prompt, complete_sred_report, sred_thread, transcripts):
    prompt = f"""
You are an expert SR&ED (Scientific Research and Experimental Development) technical writer.

You have been given:
- The complete SR&ED report
- A specific section (thread) from the report that needs improvement
- Transcript excerpts related to the project
- A user comment giving feedback on how to revise the thread

Your task:
- Revise the given thread to address the user's comment
- Maintain technical accuracy and SR&ED compliance
- Use the information from the transcripts if relevant
- Ensure the revised thread stays consistent with the full SR&ED report
- Keep the writing clear, professional, and concise

---

**Complete SR&ED Report**:
{complete_sred_report}

**Original Thread**:
{sred_thread}

**Transcript Excerpts**:
{transcripts}

**User Comment / Feedback**:
{user_prompt}

---

**Instructions**:
Please rewrite the thread to incorporate the user's comment. If needed, correct inaccuracies, improve clarity, and add missing details based on the transcripts. The revision should fit naturally into the complete report.

Output ONLY the revised thread text, without any additional commentary.
"""
    return prompt

def edit_sred_report_main(user_prompt,complete_sred_report,sred_thread,open_ai_client,trancripts):
    """
    This function edits the SRED report based on the user's prompt,existing report and input transcripts.
    """

    try:
        prompt = generate_edit_prompt(user_prompt, complete_sred_report, sred_thread, trancripts)
    except Exception as e:
        print(f"Error generating prompt: {e}")
        return None
    response = open_ai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes SR&ED project descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()



