from typing import Dict, Any
import os
import json

# --- Defaults (can be overridden by data/faqs.json) ---
DEFAULT_BASE_ANSWERS: Dict[str, str] = {
    "admission_fees": (
        "Admission fees vary by program. For example: B.Tech ~ INR 1.2–1.6L per year, MBA ~ INR 1.4–2.0L per year. "
        "Please verify the latest fee structure on the official site or with the Admissions Office."
    ),
    "hostel_fees": (
        "Hostel is available for boys and girls. Typical annual charges range ~ INR 70k–1.2L depending on room type and "
        "mess plan. Contact the Hostel Office for updated details."
    ),
    "placement": (
        "Integral University offers placements across many programs. Average package varies by program/year; "
        "CSE tends to be higher among UG programs. Check the Training & Placement Cell for current stats."
    ),
    "admission_process": (
        "Apply online via the Integral University admissions portal: register, fill the form, upload documents, pay fee, "
        "and track merit/counseling updates. Deadlines and required tests vary by program."
    ),
}

DEFAULT_PROGRAM_FEE_HINTS: Dict[str, str] = {
    "btech": "B.Tech fees are typically around INR 1.2–1.6L per year (approx).",
    "mtech": "M.Tech fees are typically around INR 1.0–1.5L per year (approx).",
    "cse": "CSE (B.Tech) fees fall under the B.Tech range (approx INR 1.2–1.6L per year).",
    "ece": "ECE (B.Tech) fees fall under the B.Tech range (approx INR 1.2–1.6L per year).",
    "mba": "MBA fees are typically around INR 1.4–2.0L per year (approx).",
    "bba": "BBA fees are typically around INR 0.8–1.2L per year (approx).",
    "bpharm": "B.Pharm fees are typically around INR 1.0–1.4L per year (approx).",
    "civil": "Civil (B.Tech) fees fall under the B.Tech range (approx INR 1.2–1.6L per year).",
    "mechanical": "Mechanical (B.Tech) fees fall under the B.Tech range (approx INR 1.2–1.6L per year).",
    "biotech": "Biotechnology (B.Tech/BSc) fees vary by program; typically ~ INR 1.0–1.6L per year (approx).",
}

DEFAULT_PROGRAM_PLACEMENT_HINTS: Dict[str, str] = {
    "cse": "CSE often sees higher average packages among UG programs.",
    "ece": "ECE placements vary by year and recruiting companies.",
    "btech": "Engineering programs have varied placements depending on discipline.",
    "mtech": "M.Tech placements depend on specialization and research/industry roles.",
    "mba": "MBA placements vary by specialization; check current recruiters and roles.",
    "bba": "BBA placements depend on domain and internships.",
    "bpharm": "Pharmacy placements often include pharma and healthcare roles.",
    "civil": "Civil placements depend on infra/construction cycles and recruiters.",
    "mechanical": "Mechanical placements vary across manufacturing, automotive, and core roles.",
    "biotech": "Biotech placements include pharma, research, and healthcare domains.",
}

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "faqs.json")


def load_faqs(path: str) -> Dict[str, Any]:
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


_FAQS = load_faqs(DATA_FILE)
BASE_ANSWERS: Dict[str, str] = {**DEFAULT_BASE_ANSWERS, **_FAQS.get("base_answers", {})}
PROGRAM_FEE_HINTS: Dict[str, str] = {**DEFAULT_PROGRAM_FEE_HINTS, **_FAQS.get("program_fee_hints", {})}
PROGRAM_PLACEMENT_HINTS: Dict[str, str] = {**DEFAULT_PROGRAM_PLACEMENT_HINTS, **_FAQS.get("program_placement_hints", {})}