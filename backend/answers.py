from typing import Dict
from backend.nlp import extract_entities
from backend.data import BASE_ANSWERS, PROGRAM_FEE_HINTS, PROGRAM_PLACEMENT_HINTS


def build_answer(intent: str, text: str) -> str:
    ents = extract_entities(text)
    program = ents.get("program")
    gender = ents.get("hostel_gender")

    if intent == "admission_fees":
        if program and program in PROGRAM_FEE_HINTS:
            return (
                f"For {program.upper()}, {PROGRAM_FEE_HINTS[program]} "
                "Please confirm the latest fee structure on the official site or with the Admissions Office."
            )
        return BASE_ANSWERS[intent]

    if intent == "hostel_fees":
        if gender:
            return (
                f"Yes, {gender} hostel is available. Annual charges are typically ~ INR 70k–1.2L depending on room type and mess plan. "
                "Please contact the Hostel Office for current rates and availability."
            )
        return BASE_ANSWERS[intent]

    if intent == "placement":
        if program and program in PROGRAM_PLACEMENT_HINTS:
            return (
                f"Placement info for {program.upper()}: {PROGRAM_PLACEMENT_HINTS[program]} "
                "Please see the Training & Placement Cell for verified, year-wise statistics."
            )
        return BASE_ANSWERS[intent]

    if intent == "admission_process":
        if program:
            return (
                f"Admission process for {program.upper()}: register on the admissions portal, complete the form, upload documents, pay fees, and track merit/counseling. "
                f"Eligibility and test requirements vary by program—please check the official notification for {program.upper()}."
            )
        return BASE_ANSWERS[intent]

    # Handle new intents for university details and chatbot introduction
    if intent in ["university_overview", "facilities", "rankings", "contact_info", "programs_offered", "campus_life"]:
        return f"I am the Integral University Chatbot. {BASE_ANSWERS[intent]}"
    if intent == "chatbot_intro":
        return BASE_ANSWERS[intent]

    return "Sorry, I don't have that information yet."