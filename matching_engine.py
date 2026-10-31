from functools import lru_cache
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from modules.skill_extractor import extract_skills

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer(MODEL_NAME)

def match_resume_to_job(resume_text: str, job_description: str) -> dict:
    if not resume_text.strip() or not job_description.strip():
        raise ValueError("Both resume text and job description are required.")

    model = load_model()
    embeddings = model.encode([resume_text, job_description], normalize_embeddings=True)
    similarity = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    semantic_pct = max(0.0, min(100.0, similarity * 100.0))

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    coverage = (len(matched) / len(job_skills) * 100.0) if job_skills else 0.0

    # Prototype weighting: 60% semantic similarity + 40% detected skill coverage.
    # This is a design choice for demonstration, not a trained/validated hiring model.
    overall = 0.60 * semantic_pct + 0.40 * coverage

    return {
        "match_score": round(overall, 2),
        "semantic_similarity": round(semantic_pct, 2),
        "skill_coverage": round(coverage, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
    }
