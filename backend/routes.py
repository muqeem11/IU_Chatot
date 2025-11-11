from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from .schemas import ChatRequest, ChatResponse
from .nlp import normalize
from .model import vectorizer, clf
from .answers import build_answer
from .auth_router import get_current_user
from .db_models import User

router = APIRouter()

@router.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, current_user: User = Depends(get_current_user)) -> ChatResponse:
    text = normalize(req.message)
    vec = vectorizer.transform([text])
    proba = clf.predict_proba(vec)[0]
    classes = clf.classes_
    # Primary intent (highest probability)
    order = proba.argsort()[::-1]
    best_idx = int(order[0])
    intent = classes[best_idx]
    confidence = float(proba[best_idx])

    # Select multiple intents (top-3 above threshold)
    selected: List[str] = []
    for idx in order[:3]:
        if float(proba[idx]) >= 0.25:  # threshold for additional intents
            selected.append(classes[int(idx)])
    if intent not in selected:
        selected.insert(0, intent)

    # Build combined answer
    parts: List[str] = []
    seen = set()
    for it in selected:
        if it in seen:
            continue
        seen.add(it)
        parts.append(build_answer(it, text))

    answer = "\n\n".join(parts)
    # Append official university link once
    answer_with_link = f"{answer}\n\nFor official details, visit: https://www.iul.ac.in"
    return ChatResponse(intent=intent, answer=answer_with_link, confidence=confidence)