from modules.skill_extractor import extract_skills


def test_lowercase_terms_detected():
    assert extract_skills("python and sql") == ["python", "sql"]


def test_capitalised_terms_detected():
    # Regression test: the original prototype matched case-sensitively.
    assert extract_skills("Python, SQL, Git, Machine Learning") == [
        "git", "machine learning", "python", "sql"]


def test_unknown_terms_ignored():
    assert extract_skills("Cooking and gardening") == []


def test_sample_job_description_skills():
    text = open("data/sample_job_description.txt", encoding="utf-8").read()
    assert extract_skills(text) == [
        "communication", "data analysis", "git", "machine learning",
        "pandas", "python", "scikit-learn", "sql", "teamwork"]
