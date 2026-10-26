
"""Data model and parser for resume extraction examples."""

from dataclasses import asdict, dataclass
import re


@dataclass
class ResumeData:
    name: str | None
    email: str | None
    experience_years: int | None
    skills: list[str]
    education: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_resume_data(text: str) -> ResumeData:
    email_match = re.search(
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text
    )

    experience_match = re.search(
        r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
        r"\s+years?\s+of\s+experience",
        text,
        re.IGNORECASE,
    )

    name_match = re.match(
        r"\s*([A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*)*)"
        r"(?:\s+is\b|,)",
        text,
    )

    education_match = re.search(
        r"(?:holds?\s+(?:a|an)|earned\s+(?:a|an))\s+"
        r"(.+?)(?=\s+(?:from|at)\s+[^.]+|[.]|$)",
        text,
        re.IGNORECASE,
    )

    skill_names = (
        "Python", "SQL", "Tableau",
        "JavaScript", "React", "PostgreSQL",
    )

    skills = [
        skill for skill in skill_names
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)
    ]

    years = experience_match.group(1).lower() if experience_match else None

    year_values = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    }

    experience_years = None
    if years:
        experience_years = (
            int(years) if years.isdigit() else year_values[years]
        )

    return ResumeData(
        name=name_match.group(1).strip() if name_match else None,
        email=email_match.group(0) if email_match else None,
        experience_years=experience_years,
        skills=skills,
        education=education_match.group(1).strip() if education_match else None,
    )
