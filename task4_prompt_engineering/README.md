# Task 4: Prompt Engineering Toolkit

## 1. Objective

This project demonstrates prompt engineering techniques for classification, reasoning, sampling, and structured data extraction.

**Important limitation:** All current experiments run locally. They use keyword rules, deterministic logic, or toy probability distributions. They do not call a real language model. Therefore, the results demonstrate the concepts but do not measure real LLM performance.

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

Install Pydantic if needed:

```powershell
python -m pip install pydantic
```

The experiments use Python's built-in modules for file handling, JSON, CSV, mathematics, and sampling.

## 4. Experiments

### Experiment 1: Classification Prompts

**Script:** `classification/evaluate_prompts.py`

The dataset contains 15 support tickets with expected categories and priorities. The required categories are Billing, Technical, and Account.

Three prompt files represent:

- **v1 — Basic:** A simple classification instruction.
- **v2 — Structured:** Instructions organized by role, task, constraints, and output format.
- **v3 — Few-shot:** A prompt containing three classification examples.

The script generates 45 records: 15 tickets for each prompt version.

**Run:**

```powershell
python -m task4_prompt_engineering.classification.evaluate_prompts
```

**Output:** `results/classification_results.csv`

The current script uses an offline keyword-based classifier. The previously observed results were 13/15 correct for each version (86.7%). These are baseline results, not measurements of LLM prompt accuracy. The script does not establish whether the three prompt designs improve model performance.

### Experiment 2: Reasoning Instructions

**Script:** `reasoning/chain_of_thought_test.py`

Five arithmetic word problems are tested under two conditions:

1. Without the instruction to think step by step.
2. With a step-by-step instruction.

The script generates ten records.

**Run:**

```powershell
python -m task4_prompt_engineering.reasoning.chain_of_thought_test
```

**Output:** `results/reasoning_results.csv`

The current implementation is a deterministic offline simulation. It does not measure the effect of reasoning instructions on a real language model.

### Experiment 3: Temperature and Top-p Sampling

**Script:** `sampling/temperature_top_p_test.py`

The experiment produces:

- Five samples at temperature 0.
- Five samples at temperature 0.7.
- Five samples at temperature 1.2.
- Five samples at top-p 0.3.
- Five samples at top-p 0.95.

This gives 25 records.

**Run:**

```powershell
python -m task4_prompt_engineering.sampling.temperature_top_p_test
```

**Output:** `results/sampling_results.csv`

The script samples from a toy probability distribution rather than generating text with an LLM. It illustrates sampling settings but does not represent real model generations.

### Experiment 4: Resume Extraction and Structured Output

**Files:**

- `datasets/resume_paragraphs.json`
- `datasets/expected_resume_data.json`
- `prompts/resume_extraction.txt`
- `extraction/schemas.py`
- `extraction/extract_resume_data.py`
- `extraction/compare_json_modes.py`

The required output fields are:

- `name`: string
- `skills`: array of strings
- `years_experience`: integer or null

The extraction script processes five resume records and compares its outputs with the expected data.

**Run:**

```powershell
python -m task4_prompt_engineering.extraction.extract_resume_data
```

The observed local results were five records processed, zero invalid outputs, and five matches out of five. These results come from the local implementation, not from a real model extracting information from resumes.

The JSON comparison script illustrates plain-text and JSON-formatted output validation.

**Run:**

```powershell
python -m task4_prompt_engineering.extraction.compare_json_modes
```

The observed simulation reported five invalid plain-text outputs and zero invalid JSON-formatted outputs. These are illustrative counts, not actual LLM API results.

Pydantic can validate the structure and types of extracted data. Validation does not, by itself, guarantee that the extracted information is factually correct.

### Experiment 5: Bad-Prompt Improvements

**File:** `prompts/bad_prompts.md`

The file contains three deliberately weak prompts and improved versions.

The improvements demonstrate how to:

1. Specify the task and allowed categories.
2. Provide context and explicit extraction rules.
3. Define exact JSON fields, data types, and missing-value behavior.

These examples demonstrate prompt-design principles. Their performance improvement has not been measured with a real language model.

## 5. Concepts Demonstrated

### System prompts

System instructions establish the model's role, behavior, and constraints. Clear instructions can help keep responses aligned with the requested task.

### Zero-shot prompting

Zero-shot prompting asks the model to perform a task without providing examples.

### Few-shot prompting

Few-shot prompting includes examples of the desired input and output. These examples can help communicate the expected pattern.

### Step-by-step reasoning instructions

Asking a model to work through a problem step by step may change its response. The effect must be evaluated using the same problems and a consistent scoring method. This project has not measured that effect on a real model.

### Temperature

Temperature controls the randomness of token selection. Lower values generally make sampling more predictable, while higher values generally allow more variation.

### Top-p sampling

Top-p sampling restricts token selection to a set of likely candidates whose cumulative probability reaches the selected threshold. Lower thresholds generally narrow the candidate set.

### Structured output and Pydantic

Structured output requests data in a defined format, such as JSON. Pydantic checks whether parsed data conforms to a specified schema. Schema validity and factual accuracy are separate concerns.

## 6. Results Summary

| Experiment | Local result | Limitation |
|---|---|---|
| Classification | 45 records; 13/15 correct per version in the observed output | Keyword baseline, not LLM accuracy |
| Reasoning | 5 problems and 10 records | Deterministic simulation |
| Sampling | 25 records | Toy probability distribution |
| Resume extraction | 5 records; 5/5 expected matches; 0 invalid outputs | Local extraction logic |
| JSON comparison | 5 simulated plain-text invalid outputs; 0 simulated JSON invalid outputs | No model-generated outputs |

## 7. Conclusion

This project organizes a small prompt engineering toolkit and demonstrates classification prompts, reasoning instructions, sampling concepts, structured extraction, and schema validation.

The local scripts run without paid API access. However, the results should not be reported as real LLM measurements. A future model-based evaluation would need to run each prompt against the same test examples, record model settings and outputs, calculate accuracy and invalid-output counts, and document the evaluation method.

The illustrative expected accuracy figures in the assignment are examples, not required results. Actual results should be reported honestly.
