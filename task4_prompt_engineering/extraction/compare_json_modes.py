
"""Compare plain-text and JSON-formatted extraction offline.

This is a simulation, not a test of a real LLM's JSON mode.
"""

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILE = ROOT / "datasets" / "expected_resume_data.json"


class ResumeData(BaseModel):
    name: str = Field(min_length=1)
    skills: list[str]
    years_experience: int = Field(ge=0)


def main():
    with EXPECTED_FILE.open(encoding="utf-8") as file:
        expected_records = json.load(file)

    plain_invalid = 0
    json_invalid = 0

    for record in expected_records:
        # Simulate ordinary text that includes the extracted fields.
        plain_output = (
            f"Name: {record['name']}; "
            f"Skills: {', '.join(record['skills'])}; "
            f"Experience: {record['years_experience']} years"
        )

        try:
            # Plain text is not a JSON object, so JSON parsing should fail.
            parsed_plain = json.loads(plain_output)
            ResumeData.model_validate(parsed_plain)
        except (json.JSONDecodeError, ValidationError):
            plain_invalid += 1

        # Simulate a structured JSON response.
        json_output = json.dumps({
            "name": record["name"],
            "skills": record["skills"],
            "years_experience": record["years_experience"],
        })

        try:
            parsed_json = json.loads(json_output)
            ResumeData.model_validate(parsed_json)
        except (json.JSONDecodeError, ValidationError):
            json_invalid += 1

    print("Resumes tested:", len(expected_records))
    print("Plain-text invalid outputs:", plain_invalid)
    print("JSON-formatted invalid outputs:", json_invalid)
    print("Note: Both formats are simulated locally; no LLM was called.")


if __name__ == "__main__":
    main()
