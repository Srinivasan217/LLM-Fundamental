
# Prompt Anti-Patterns and Improvements

These examples demonstrate how clearer instructions improve prompt design.
They are illustrative examples, not measured results from an LLM.

## Example 1: Too vague

**Bad prompt:**
Help with this customer ticket.

**Improved prompt:**
Classify the customer ticket into exactly one category: billing, technical, or account. Return only the lowercase category.

**Why it improves:**
The task and allowed categories are clear, and the output is consistent.

## Example 2: Missing context

**Bad prompt:**
Extract the person's skills.

**Improved prompt:**
Read the resume below. Extract only skills explicitly mentioned in the text. Return a JSON object with a `skills` array. Do not guess missing skills.

Resume: {resume_text}

**Why it improves:**
It supplies the input, specifies the output format, and prevents unsupported assumptions.

## Example 3: Ambiguous output

**Bad prompt:**
Tell me about this applicant.

**Improved prompt:**
Extract the applicant's name, skills, and years of experience from the resume. Return valid JSON with exactly these fields:
`name` (string), `skills` (array of strings), and `years_experience` (integer or null). Use null when experience is not stated. Do not invent information.

Resume: {resume_text}

**Why it improves:**
The field names, data types, and missing-information rule make the result easier to validate.

## Evaluation note

These examples show improvements in clarity and structure. A real performance improvement must be tested on the same inputs with a real language model and a fixed evaluation procedure.
