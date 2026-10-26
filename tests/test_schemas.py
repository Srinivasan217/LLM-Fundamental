import unittest

from task4_prompt_engineering.extraction.schemas import extract_resume_data


class ResumeSchemaTests(unittest.TestCase):
    def test_extracts_fields_from_sample_sentence(self):
        result = extract_resume_data(
            "Jordan Lee is a data analyst with five years of experience. "
            "Jordan uses Python and SQL, and holds a Bachelor of Science "
            "in Statistics from North Valley University. "
            "Contact: jordan.lee@example.com."
        )
        self.assertEqual(result.name, "Jordan Lee")
        self.assertEqual(result.email, "jordan.lee@example.com")
        self.assertEqual(result.experience_years, 5)
        self.assertEqual(result.skills, ["Python", "SQL"])
        self.assertEqual(result.education, "Bachelor of Science in Statistics")

    def test_missing_fields_are_not_inferred(self):
        result = extract_resume_data("A short profile with no structured details.")
        self.assertIsNone(result.email)
        self.assertIsNone(result.experience_years)
        self.assertEqual(result.skills, [])


if __name__ == "__main__":
    unittest.main()
