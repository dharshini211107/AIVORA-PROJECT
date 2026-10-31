"""Command-line demo: rank the sample resumes against the sample job description.

Usage:  python demo.py
        python demo.py --job path/to/job.txt --resumes path/to/folder
"""
import argparse
from pathlib import Path

from modules.matching_engine import match_resume_to_job


def main():
    ap = argparse.ArgumentParser(description="AIVORA command-line demo")
    ap.add_argument("--job", default="data/sample_job_description.txt")
    ap.add_argument("--resumes", default="data/sample_resumes")
    args = ap.parse_args()

    job = Path(args.job).read_text(encoding="utf-8")
    rows = []
    for f in sorted(Path(args.resumes).glob("*.txt")):
        r = match_resume_to_job(f.read_text(encoding="utf-8"), job)
        rows.append((f.name, r))
    rows.sort(key=lambda x: x[1]["match_score"], reverse=True)

    print(f"{'Rank':<5}{'Resume':<18}{'Overall':>9}{'Semantic':>10}{'Coverage':>10}")
    for i, (name, r) in enumerate(rows, 1):
        print(f"{i:<5}{name:<18}{r['match_score']:>9.1f}{r['semantic_similarity']:>10.1f}{r['skill_coverage']:>10.1f}")
        print(f"     matched: {', '.join(r['matched_skills']) or '-'}")
        print(f"     missing: {', '.join(r['missing_skills']) or '-'}")
    print("\nScores support human review; they are not hiring decisions.")


if __name__ == "__main__":
    main()
