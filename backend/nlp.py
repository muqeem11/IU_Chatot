from typing import List, Dict, Optional, Tuple
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data if not present (lazy load)
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    WordNetLemmatizer().lemmatize('test')
except LookupError:
    nltk.download('wordnet')

STOP_WORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()

# Hindi/Hinglish mapping patterns to normalize tokens
HI_MAP_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\b(फीस|फ़ीस|शुल्क|fees|fee)\b", re.I), " fees "),
    (re.compile(r"\b(प्रवेश|दाखिला|admission|admit)\b", re.I), " admission "),
    (re.compile(r"\b(होस्टल|छात्रावास|hostel)\b", re.I), " hostel "),
    (re.compile(r"\b(प्लेसमेंट|नौकरी|जॉब|placement|job|package|pkg)\b", re.I), " placement "),
    (re.compile(r"\b(औसत\s*पैकेज|औसत|average|avg)\b", re.I), " average "),
    # genders
    (re.compile(r"\b(लड़के|लड़के|ladke|male|men)\b", re.I), " boys "),
    (re.compile(r"\b(लड़कियां|लडकियां|लड़कियां|ladkiyon|ladki|female|women)\b", re.I), " girls "),
    # programs
    (re.compile(r"\b(बीटेक|b\s*tech|btech)\b", re.I), " btech "),
    (re.compile(r"\b(एमटेक|m\s*tech|mtech)\b", re.I), " mtech "),
    (re.compile(r"\b(एमबीए|mba)\b", re.I), " mba "),
    (re.compile(r"\b(बीबीए|bba)\b", re.I), " bba "),
    (re.compile(r"\b(बीफार्म|बी\s*फार्म|b\s*pharm|bpharm)\b", re.I), " bpharm "),
    (re.compile(r"\b(कंप्यूटर\s*साइंस|कम्प्यूटर\s*साइंस|cse|comp\s*sci)\b", re.I), " cse "),
    (re.compile(r"\b(इलेक्ट्रॉनिक्स(\s*एंड\s*कम्युनिकेशन)?|ece)\b", re.I), " ece "),
    (re.compile(r"\b(सिविल|civil)\b", re.I), " civil "),
    (re.compile(r"\b(मैकेनिकल|यांत्रिक|mech|mechanical|me)\b", re.I), " mechanical "),
    (re.compile(r"\b(बायोटेक|बायोटेक्नोलॉजी|biotech)\b", re.I), " biotech "),
    (re.compile(r"\b(एमबीबीएस|mbbs|medicine|medical)\b", re.I), " mbbs "),
    (re.compile(r"\b(बीडीएस|bds|dentistry|dental)\b", re.I), " bds "),
    (re.compile(r"\b(डिप्लोमा|diploma)\b", re.I), " diploma "),
    (re.compile(r"\b(बीएससी|bsc|bachelor of science)\b", re.I), " bsc "),
    (re.compile(r"\b(बीसीए|bca|bachelor of computer applications)\b", re.I), " bca "),
]

_non_alnum_english = re.compile(r"[^a-z0-9\s]")

PROGRAM_ALIASES: Dict[str, List[str]] = {
    "btech": ["btech", "b tech", "bachelor of technology", "ug engineering", "बीटेक"],
    "mtech": ["mtech", "m tech", "master of technology", "एमटेक"],
    "cse": ["cse", "computer science", "computer science engineering", "कंप्यूटर साइंस", "कम्प्यूटर साइंस"],
    "ece": ["ece", "electronics", "electronics and communication", "इलेक्ट्रॉनिक्स", "इलेक्ट्रॉनिक्स एंड कम्युनिकेशन"],
    "mba": ["mba", "master of business administration", "एमबीए"],
    "bba": ["bba", "bachelor of business administration", "बीबीए"],
    "bpharm": ["bpharm", "b pharm", "bachelor of pharmacy", "बीफार्म", "बी फार्म"],
    "civil": ["civil", "civil engineering", "ce", "सिविल"],
    "mechanical": ["mechanical", "me", "mech", "mechanical engineering", "मैकेनिकल", "यांत्रिक"],
    "biotech": ["biotech", "biotechnology", "bio tech", "बायोटेक", "बायोटेक्नोलॉजी"],
    "mbbs": ["mbbs", "m b b s", "bachelor of medicine", "bachelor of medicine and bachelor of surgery", "एमबीबीएस", "medicine"],
    "bds": ["bds", "b d s", "bachelor of dental surgery", "बीडीएस", "dentistry", "dental"],
    "diploma": ["diploma", "डिप्लोमा"],
    "bsc": ["bsc", "b s c", "bachelor of science", "बीएससी"],
    "bca": ["bca", "b c a", "bachelor of computer applications", "बीसीए"],
}

HOSTEL_GENDER_ALIASES: Dict[str, List[str]] = {
    "boys": ["boys", "boy", "male", "men", "लड़के", "लड़के"],
    "girls": ["girls", "girl", "female", "women", "लड़कियां", "लडकियां", "लड़कियां", "लड़कियों", "लड़कियों"],
}

PROGRAM_PATTERNS: List[Tuple[str, re.Pattern]] = [
    (canon, re.compile(r"\b(" + r"|".join(map(re.escape, aliases)) + r")\b"))
    for canon, aliases in PROGRAM_ALIASES.items()
]
HOSTEL_PATTERNS: List[Tuple[str, re.Pattern]] = [
    (canon, re.compile(r"\b(" + r"|".join(map(re.escape, aliases)) + r")\b"))
    for canon, aliases in HOSTEL_GENDER_ALIASES.items()
]


def apply_hi_mapping(text: str) -> str:
    for pat, rep in HI_MAP_PATTERNS:
        text = pat.sub(rep, text)
    return text


def normalize(text: str) -> str:
    text = apply_hi_mapping(text)
    text = text.lower()
    text = _non_alnum_english.sub(" ", text)
    # Tokenize, remove stop words, lemmatize
    tokens = text.split()
    tokens = [LEMMATIZER.lemmatize(word) for word in tokens if word not in STOP_WORDS]
    text = " ".join(tokens)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_entities(text: str) -> Dict[str, Optional[str]]:
    program: Optional[str] = None
    for canon, pat in PROGRAM_PATTERNS:
        if pat.search(text):
            program = canon
            break
    hostel_gender: Optional[str] = None
    for canon, pat in HOSTEL_PATTERNS:
        if pat.search(text):
            hostel_gender = canon
            break
    return {"program": program, "hostel_gender": hostel_gender}