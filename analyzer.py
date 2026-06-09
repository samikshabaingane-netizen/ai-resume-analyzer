import PyPDF2

# ---------------- SKILLS DATABASE ---------------- #

skills_db = [

    'python',
    'java',
    'sql',
    'machine learning',
    'power bi',
    'excel',
    'communication',
    'flask',
    'django'
]

# ---------------- CAREER DATABASE ---------------- #

career_data = {

    'Data Analyst': [
        'python',
        'sql',
        'excel',
        'power bi'
    ],

    'Web Developer': [
        'python',
        'flask',
        'django'
    ],

    'Software Developer': [
        'python',
        'java',
        'sql'
    ]
}

# ---------------- PDF TEXT EXTRACTION ---------------- #

def extract_text(pdf_path):

    text = ""

    with open(pdf_path, 'rb') as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text

# ---------------- SKILL DETECTION ---------------- #

def detect_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_db:

        if skill in text:

            found_skills.append(skill)

    return found_skills

# ---------------- CAREER SUGGESTION ---------------- #

def suggest_career(skills):

    best_match = ""

    max_match = 0

    missing_skills = []

    for career, required_skills in career_data.items():

        matched = len(set(skills) & set(required_skills))

        if matched > max_match:

            max_match = matched

            best_match = career

            missing_skills = list(
                set(required_skills) - set(skills)
            )

    return best_match, missing_skills

# ---------------- RESUME SCORE ---------------- #

def calculate_score(skills):

    score = len(skills) * 10

    if score > 100:

        score = 100

    return score