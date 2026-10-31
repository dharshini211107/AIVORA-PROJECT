# AIVORA — Intelligent Resume-to-Job Matching

AIVORA is a student mini project (Department of Artificial Intelligence and Data Science, KPR Institute of Engineering and Technology, 2026–2027) that matches resumes to job descriptions using NLP and semantic similarity.

**Team:** Elakkiya R (25AD042), Dharshini A (25AD036), Bhavana A (25AD024) · **Guide:** Ms. S. P. Kavya

## Features
- **Recruiter workspace:** upload several PDF/DOCX/TXT resumes, rank them, download a CSV shortlist.
- **Candidate workspace:** upload one resume and get a matched / missing skill report.
- Rule-based skill extraction with spaCy `EntityRuler` (51-term starter vocabulary, **case-insensitive**).
- Semantic similarity with Sentence-BERT (`all-MiniLM-L6-v2`) and cosine similarity.
- Explainable results: matched, missing and detected skills.

## Score
`Overall = 0.60 × semantic similarity + 0.40 × skill coverage`

The weights are a demonstration choice, not a validated hiring model. Scores support human review and are not hiring decisions.

## Run in Google Colab
1. Upload `notebooks/AIVORA_Colab.ipynb` to [colab.research.google.com](https://colab.research.google.com) (File → Upload notebook), or open it from GitHub (File → Open notebook → GitHub tab).
2. Set `REPO_URL` in the first cell to your repository URL (or leave it empty and upload `AIVORA.zip`).
3. Run the cells in order. Cell 5 prints a temporary public link for the web app.

## Run locally
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q tests       # unit tests
python demo.py                  # command-line demo on the sample data
streamlit run app.py            # web app at http://localhost:8501
```
The first run downloads the Sentence-BERT model (internet required).

## Project structure
```
AIVORA/
├── app.py                      Streamlit interface
├── demo.py                     command-line demo
├── modules/
│   ├── resume_parser.py        PDF / DOCX / TXT text extraction
│   ├── skill_extractor.py      spaCy EntityRuler skill extraction
│   └── matching_engine.py      embeddings, similarity, coverage, score
├── data/                       sample job description and resumes
├── tests/                      unit tests for the skill extractor
├── notebooks/AIVORA_Colab.ipynb
└── requirements.txt
```

## Known limitations
- Skill detection uses a small hand-maintained vocabulary; synonyms, abbreviations and hyphenated forms (e.g. "problem-solving") are not recognised.
- Scanned (image-only) PDFs need OCR; only embedded text is read.
- The 60/40 weighting has not been evaluated on labelled resume–job pairs, and no fairness testing has been done.

## Publish to GitHub
```bash
git init
git add .
git commit -m "AIVORA: intelligent resume-to-job matching"
git branch -M main
git remote add origin https://github.com/<your-username>/AIVORA.git
git push -u origin main
```
(Create the empty repository `AIVORA` on github.com first. Do not tick "Add a README".)
