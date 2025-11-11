# Simple smoke tests for backend modules without starting the server
import sys

# Ensure imports work
try:
    from backend.app import app  # noqa: F401
    from backend.routes import health
    from backend import nlp, model, answers
    from backend.auth import get_password_hash, verify_password, create_access_token
    from backend.database import SessionLocal, engine
    from backend.db_models import Base, User
except Exception as e:
    print(f"IMPORT_FAIL: {e}")
    sys.exit(1)

# Ensure DB tables exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"DB_INIT_FAIL: {e}")
    sys.exit(1)

# Health endpoint logic
try:
    h = health()
    assert h.get("status") == "ok"
    print("HEALTH_OK")
except Exception as e:
    print(f"HEALTH_FAIL: {e}")
    sys.exit(1)

# NLP normalize and entities
try:
    txt = "BTech fee structure for CSE boys hostel and placements"
    norm = nlp.normalize(txt)
    ents = nlp.extract_entities(norm)
    assert isinstance(norm, str) and isinstance(ents, dict)
    print("NLP_OK", ents)
except Exception as e:
    print(f"NLP_FAIL: {e}")
    sys.exit(1)

# Model vectorize and predict
try:
    vec = model.vectorizer.transform([nlp.normalize("btech fees")])
    proba = model.clf.predict_proba(vec)[0]
    assert proba.sum() > 0
    print("MODEL_OK", float(proba.max()))
except Exception as e:
    print(f"MODEL_FAIL: {e}")
    sys.exit(1)

# Answers builder for a few intents
try:
    for intent in ["admission_fees", "hostel_fees", "placement", "admission_process"]:
        ans = answers.build_answer(intent, "btech boys hostel fees and placement")
        assert isinstance(ans, str) and len(ans) > 10
    print("ANSWERS_OK")
except Exception as e:
    print(f"ANSWERS_FAIL: {e}")
    sys.exit(1)

# Auth hashing and token
try:
    pwd = "test1234!"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed)
    token = create_access_token({"sub": "tester"})
    assert isinstance(token, str) and len(token) > 10
    print("AUTH_OK")
except Exception as e:
    print(f"AUTH_FAIL: {e}")
    sys.exit(1)

# Minimal user roundtrip in DB
try:
    db = SessionLocal()
    # Cleanup any prior tester user
    db.query(User).filter(User.username == "tester").delete()
    db.commit()
    u = User(username="tester", email="tester@example.com", hashed_password=hashed)
    db.add(u)
    db.commit()
    db.refresh(u)
    assert u.id is not None
    print("DB_OK", u.id)
finally:
    db.close()

print("SMOKE_SUCCESS")
sys.exit(0)