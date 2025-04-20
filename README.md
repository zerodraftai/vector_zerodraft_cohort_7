# 📘 Zerodraft AI * Vector - AI-Powered SRED report generation.
## 📝 Description
This project is a result of the Vector MLA cohort 7. The purpose of this project is to develop an AI agent that can assist in generation of SRED reports.

## 📂 Repository Structure
```
vector_zerodraft_cohort_7/
│
├── sample_input/                   # Input data files
├── src/                            # Source code
│   ├──chunking_and_embedding/
│   │   ├── perform_chunking.py
│   │   ├── generate_embeddings.py
│   ├──sred_report_generation/
│   │   ├── rag_pipeline_to_generate_proj_description.py
│   │   ├── sred_prompt_1.py
│   ├──sred_report_evaluation/
│   │   ├── evaluate_sred_report.py
│   ├──sred_report_editing/
│   │   ├── edit_sred_report.py
│   ├──helper_functions/
│   │   ├── helper_function.py
│   │   ├── delete_redis_vectors.py
│   │   ├── prompts.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9
- `pip install -r requirements.txt`

### Run the Project

```bash
python -m streamlit run streamlit_ui.py
```

### Environment Variables

List any required environment variables here:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
OPENAI_API_KEY

## 🧠 Core Modules
- `chunking_and_embedding`: Handles chunking and embedding of input data.
- `sred_report_generation`: Contains the logic for generating SRED reports.
- `sred_report_evaluation`: Evaluates the generated SRED reports using LLM as a judge model and METEOR score.
- `sred_report_editing`: Provides functionality to edit the generated SRED reports.

## 🤝 Acknowledgments

Arjun Sridharkumar and Mohammad Syed.
