
"""Extract resume fields, validate them, and compare with expected data."""

import csv
import json
import re
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "datasets" / "resume_paragraphs.json"
EXPECTED_FILE = ROOT / "datasets" / "expected_resume_data.json"
OUTPUT_FILE = ROOT / "results" / "extraction_results.csv"


class ResumeData(BaseModel):
    name: str = Field(min_length=1)
    skills: list[str]
    years_experience: int = Field(ge=0)


def extract_resume_data(text: str) -> dict:
    """Extract the required fields from a resume paragraph."""

    name_match = re.match(
        r"\s*([A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*)*)"
        r"(?:\s+is\b|,\s*)",
        text,
     )
    years_match = re.search(
        r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
        r"\s+years?\s+of\s+experience",
        text,
        re.IGNORECASE,
    )

    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    }

    years = years_match.group(1).lower() if years_match else None
    experience = (
        int(years) if years and years.isdigit()
        else number_words.get(years) if years else None
    )

    skill_names = [
        "Python", "SQL", "Tableau",
        "JavaScript", "React", "PostgreSQL",
    ]
    skills = [
        skill for skill in skill_names
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)
    ]

    return {
        "name": name_match.group(1) if name_match else None,
        "skills": skills,
        "years_experience": experience,
    }


def main() -> None:
    with DATA_FILE.open(encoding="utf-8") as file:
        resumes = json.load(file)

    with EXPECTED_FILE.open(encoding="utf-8") as file:
        expected = {item["resume_id"]: item for item in json.load(file)}

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    invalid_count = 0
    correct_count = 0

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        fields = [
            "resume_id", "name", "skills",
            "years_experience", "valid", "matches_expected",
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for resume in resumes:
            extracted = extract_resume_data(resume["text"])

            try:
                validated = ResumeData.model_validate(extracted)
                extracted = validated.model_dump()
                valid = True
            except ValidationError:
                invalid_count += 1
                valid = False

            expected_item = expected[resume["id"]]
            matches = (
                valid
                and extracted == {
                    "name": expected_item["name"],
                    "skills": expected_item["skills"],
                    "years_experience": expected_item["years_experience"],
                }
            )

            if matches:
                correct_count += 1

            writer.writerow({
                "resume_id": resume["id"],
                "name": extracted["name"] or "",
                "skills": ";".join(extracted["skills"]),
                "years_experience": extracted["years_experience"],
                "valid": valid,
                "matches_expected": matches,
            })

    print(f"Resume records: {len(resumes)}")
    print(f"Invalid outputs: {invalid_count}")
    print(f"Matches expected: {correct_count}/{len(resumes)}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
