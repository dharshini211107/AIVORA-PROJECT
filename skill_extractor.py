import re
import spacy
from spacy.pipeline import EntityRuler

# Starter skill vocabulary. Extend this list for your target job domains.
SKILL_TERMS = [
    "python", "java", "c++", "c", "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "natural language processing", "nlp",
    "data analysis", "data visualization", "statistics", "excel", "power bi",
    "tableau", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "spacy", "sentence-transformers", "bert", "git", "github", "docker",
    "kubernetes", "aws", "azure", "google cloud", "html", "css", "javascript",
    "react", "node.js", "flask", "streamlit", "fastapi", "communication",
    "problem solving", "project management", "teamwork", "leadership",
    "computer vision", "data structures", "algorithms", "linux", "api"
]

def _build_nlp():
    nlp = spacy.blank("en")
    # LOWER makes matching case-insensitive, so "Python" and "python" both match.
    ruler = nlp.add_pipe("entity_ruler", config={"phrase_matcher_attr": "LOWER"})
    patterns = [{"label": "SKILL", "pattern": term} for term in SKILL_TERMS]
    ruler.add_patterns(patterns)
    return nlp

_NLP = _build_nlp()

def extract_skills(text: str) -> list[str]:
    """Rule-based NER using spaCy EntityRuler and a transparent skill vocabulary."""
    doc = _NLP(text)
    return sorted({ent.text.lower() for ent in doc.ents if ent.label_ == "SKILL"})
