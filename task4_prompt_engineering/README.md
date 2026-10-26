# Task 4: Prompt Engineering Toolkit

## 1. Objective

This project explores prompt engineering techniques for classification, reasoning, structured data extraction, and sampling. It compares different prompt designs and demonstrates how output formatting and validation affect results.

**Important:** The experiments in this project run locally and do not call a hosted language model. Results are deterministic demonstrations or simulations, not measurements of real LLM performance.

## 2. Project Structure

```text
task4_prompt_engineering/
├── README.md
├── classification/
│   └── evaluate_prompts.py
├── datasets/
│   ├── support_tickets.json
│   ├── resume_paragraphs.json
│   └── expected_resume_data.json
├── extraction/
│   ├── schemas.py
│   ├── extract_resume_data.py
│   └── compare_json_modes.py
├── prompts/
│   ├── classification_v1.txt
│   ├── classification_v2.txt
│   ├── classification_v3.txt
│   ├── resume_extraction.txt
│   └── bad_prompts.md
├── reasoning/
│   └── chain_of_thought_test.py
├── sampling/
│   └── temperature_top_p_test.py
└── results/
    ├── classification_results.csv
    ├── extraction_results.csv
    ├── reasoning_results.csv
    └── sampling_results.csv
```

## 3. Requirements

Python 3.10 or newer is recommended.

Install the required Pydantic package:

```powershell
python -m pip install pydantic
```

The scripts use Python's built-in modules for CSV, JSON, file handling, mathematics, and random sampling.

## 4. Experiments

### Experiment 1: Prompt Classification

**Script:** `classification/evaluate_prompts.py`

The experiment uses 15 labeled support tickets across three required categories:

- Billing
- Technical
- Account

Each ticket also has a priority label.

Three prompt versions are maintained:

- **v1 — Basic:** A simple classification instruction.
- **v2 — Structured:** A role, task, constraints, and output-format instruction.
- **v3 — Few-shot:** A classification instruction with three examples.

The evaluation script produces 45 rows: 15 tickets for each of the three prompt versions.

The current script uses the same offline keyword classifier for all versions. Therefore, its scores cannot establish whether one prompt is better than another.

**Run:**

```powershell
python .\task4_prompt_engineering\classification\evaluate_prompts.py
```

**Output:** `results/classification_results.csv`

### Experiment 2: Reasoning Evaluation

**Script:** `reasoning/chain_of_thought_test.py`

Five arithmetic word problems are tested under two conditions:

1. Without a step-by-step instruction.
2. With a step-by-step instruction and a short reasoning summary.

The script writes ten rows, containing the answer, expected answer, correctness, and condition.

This is a deterministic Python simulation. It does not measure the effect of reasoning instructions on an actual language model.

**Run:**

```powershell
python .\task4_prompt_engineering\reasoning\