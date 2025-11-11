from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from backend.nlp import normalize

# Training data (expanded for better accuracy)
TRAIN_DATA = [
    # Admission Fees
    ("what are the admission fees for btech", "admission_fees"),
    ("btech fee structure", "admission_fees"),
    ("how much is mba fees", "admission_fees"),
    ("fee for cse program", "admission_fees"),
    ("mtech tuition fees", "admission_fees"),
    ("civil engineering fees", "admission_fees"),
    ("mechanical fees per year", "admission_fees"),
    ("biotech fee structure", "admission_fees"),
    ("ece fees", "admission_fees"),
    ("bba cost", "admission_fees"),
    ("bpharm charges", "admission_fees"),
    ("annual fees for btech", "admission_fees"),
    ("cost of mba program", "admission_fees"),
    ("btech ki fees kitni hai", "admission_fees"),
    ("mba ka shulk kya hai", "admission_fees"),
    ("fees for biotechnology", "admission_fees"),

    # Hostel Fees
    ("hostel fee for boys", "hostel_fees"),
    ("girls hostel charges", "hostel_fees"),
    ("is hostel available and what cost", "hostel_fees"),
    ("ladkiyon ka hostel fees", "hostel_fees"),
    ("boys hostel rent", "hostel_fees"),
    ("hostel cost for cse students", "hostel_fees"),
    ("ladkon ke hostel ki charges", "hostel_fees"),
    ("girls accommodation fees", "hostel_fees"),
    ("annual hostel charges", "hostel_fees"),

    # Placement
    ("placements for cse", "placement"),
    ("average package cse", "placement"),
    ("placement record mba", "placement"),
    ("mechanical placement average", "placement"),
    ("civil placements stats", "placement"),
    ("biotech placement opportunities", "placement"),
    ("cse ka average package", "placement"),
    ("mba placement packages", "placement"),
    ("ece job placements", "placement"),
    ("highest package in btech", "placement"),
    ("placement stats for mechanical", "placement"),
    ("biotech career prospects", "placement"),

    # Admission Process
    ("admission process btech", "admission_process"),
    ("how to apply for ug", "admission_process"),
    ("mba admission procedure", "admission_process"),
    ("biotech admission process", "admission_process"),
    ("steps to admit in cse", "admission_process"),
    ("application process for btech", "admission_process"),
    ("how to get admission in mba", "admission_process"),
    ("admission requirements for civil", "admission_process"),
    ("btech admission kaise kare", "admission_process"),
    ("mba mein kaise apply kare", "admission_process"),

    # University Overview
    ("what is integral university", "university_overview"),
    ("tell me about integral university", "university_overview"),
    ("integral university overview", "university_overview"),
    ("about the university", "university_overview"),
    ("university history", "university_overview"),
    ("when was integral university established", "university_overview"),
    ("integral university location", "university_overview"),
    ("university ka brief batao", "university_overview"),
    ("integral university ke bare mein", "university_overview"),

    # Facilities
    ("what facilities are available", "facilities"),
    ("campus facilities", "facilities"),
    ("library and labs", "facilities"),
    ("hostel and sports", "facilities"),
    ("university infrastructure", "facilities"),
    ("facilities in integral university", "facilities"),
    ("available amenities", "facilities"),
    ("campus features", "facilities"),
    ("suidad aur sahuliyat", "facilities"),
    ("university ki facilities", "facilities"),

    # Rankings
    ("university rankings", "rankings"),
    ("integral university rank", "rankings"),
    ("nirf ranking", "rankings"),
    ("how is the university ranked", "rankings"),
    ("ranking of integral university", "rankings"),
    ("university ki ranking", "rankings"),
    ("integral university position in rankings", "rankings"),

    # Contact Info
    ("contact details", "contact_info"),
    ("university address", "contact_info"),
    ("phone number", "contact_info"),
    ("email id", "contact_info"),
    ("how to contact", "contact_info"),
    ("university contact", "contact_info"),
    ("contact information", "contact_info"),
    ("sampark details", "contact_info"),
    ("university ka address", "contact_info"),

    # Programs Offered
    ("what programs are offered", "programs_offered"),
    ("courses available", "programs_offered"),
    ("btech programs", "programs_offered"),
    ("available courses", "programs_offered"),
    ("university programs", "programs_offered"),
    ("faculties and programs", "programs_offered"),
    ("degree programs", "programs_offered"),
    ("courses in integral university", "programs_offered"),
    ("konsi courses hai", "programs_offered"),
    ("university mein kya padhaya jata hai", "programs_offered"),

    # Campus Life
    ("campus life", "campus_life"),
    ("student activities", "campus_life"),
    ("clubs and societies", "campus_life"),
    ("extracurricular activities", "campus_life"),
    ("sports and events", "campus_life"),
    ("nss ncc", "campus_life"),
    ("cultural events", "campus_life"),
    ("university life", "campus_life"),
    ("campus mein kya hota hai", "campus_life"),
    ("student life in university", "campus_life"),

    # Chatbot Introduction
    ("tell me about you", "chatbot_intro"),
    ("who are you", "chatbot_intro"),
    ("what is your name", "chatbot_intro"),
    ("introduce yourself", "chatbot_intro"),
    ("what can you do", "chatbot_intro"),
    ("about you", "chatbot_intro"),
    ("tum kaun ho", "chatbot_intro"),
    ("tumhara naam kya hai", "chatbot_intro"),
    ("apne bare mein batao", "chatbot_intro"),
    ("tum kya karte ho", "chatbot_intro"),
]

X_train: List[str] = [normalize(t) for t, _ in TRAIN_DATA]
Y_train: List[str] = [y for _, y in TRAIN_DATA]

vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
X_vec = vectorizer.fit_transform(X_train)
clf = SVC(probability=True, kernel='linear', C=1.0)  # Linear SVM for text, with probability estimates
clf.fit(X_vec, Y_train)