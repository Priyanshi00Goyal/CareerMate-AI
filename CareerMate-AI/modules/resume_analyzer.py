import re
from pypdf import PdfReader


# ==================================================
# COMMON TECHNICAL SKILLS
# ==================================================

COMMON_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "React",
    "Node.js",
    "Streamlit",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Structures",
    "Git",
    "GitHub",
    "Docker",
    "MySQL",
    "MongoDB",
    "AWS",
    "Firebase"
]


# ==================================================
# EXTRACT TEXT FROM PDF
# ==================================================

def extract_text_from_pdf(uploaded_file):

    """
    Extract text from an uploaded PDF resume.
    """

    try:

        # Reset file position
        uploaded_file.seek(0)

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        return f"Error reading PDF: {str(e)}"


# ==================================================
# EXTRACT SKILLS
# ==================================================

def extract_skills(resume_text):

    """
    Find known technical skills in the resume.
    """

    found_skills = []

    for skill in COMMON_SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            resume_text,
            re.IGNORECASE
        ):

            found_skills.append(skill)

    return found_skills


# ==================================================
# EXTRACT SKILLS USING CUSTOM SKILL LIST
# ==================================================

def extract_resume_skills(
    resume_text,
    skill_list
):

    """
    Detect skills using the project's skill database.
    """

    detected_skills = []

    resume_text_lower = resume_text.lower()

    for skill in skill_list:

        skill = str(skill).strip()

        if not skill:
            continue

        # Use word-boundary matching
        pattern = r"\b" + re.escape(
            skill.lower()
        ) + r"\b"

        if re.search(
            pattern,
            resume_text_lower
        ):

            detected_skills.append(skill)

    return detected_skills


# ==================================================
# DETECT RESUME SECTIONS
# ==================================================

def detect_sections(resume_text):

    """
    Detect common sections available in the resume.
    """

    sections = {

        "Contact Information": [
            "email",
            "phone",
            "contact",
            "linkedin",
            "github"
        ],

        "Education": [
            "education",
            "university",
            "college",
            "degree"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Experience": [
            "experience",
            "internship",
            "work experience",
            "employment"
        ],

        "Certifications": [
            "certifications",
            "certificates",
            "certification"
        ],

        "Achievements": [
            "achievements",
            "awards"
        ]

    }

    found_sections = []

    resume_text_lower = resume_text.lower()

    for section, keywords in sections.items():

        if any(
            keyword in resume_text_lower
            for keyword in keywords
        ):

            found_sections.append(section)

    return found_sections


# ==================================================
# CALCULATE RESUME SCORE
# ==================================================

def calculate_resume_score(
    skills,
    sections
):

    """
    Calculate a basic resume completeness score.
    """

    score = 0

    # ----------------------------------------------
    # Section score
    # ----------------------------------------------

    score += min(
        len(sections) * 10,
        60
    )

    # ----------------------------------------------
    # Skills score
    # ----------------------------------------------

    score += min(
        len(skills) * 4,
        40
    )

    return min(
        score,
        100
    )


# ==================================================
# COMPLETE RESUME ANALYSIS
# ==================================================

def analyze_resume(
    uploaded_file,
    skill_list=None
):

    """
    Complete resume analysis pipeline.

    Compatible with:

        analyze_resume(uploaded_file)

    and:

        analyze_resume(uploaded_file, skill_list)
    """

    # ----------------------------------------------
    # Extract resume text
    # ----------------------------------------------

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    # ----------------------------------------------
    # Check extraction error
    # ----------------------------------------------

    if resume_text.startswith(
        "Error reading PDF"
    ):

        return {
            "success": False,
            "error": resume_text
        }

    # ----------------------------------------------
    # Check empty PDF
    # ----------------------------------------------

    if not resume_text.strip():

        return {
            "success": False,
            "error": (
                "No readable text was found "
                "in the uploaded PDF."
            )
        }

    # ----------------------------------------------
    # Determine skills
    # ----------------------------------------------

    if skill_list:

        skills = extract_resume_skills(
            resume_text,
            skill_list
        )

    else:

        skills = extract_skills(
            resume_text
        )

    # ----------------------------------------------
    # Detect sections
    # ----------------------------------------------

    sections = detect_sections(
        resume_text
    )

    # ----------------------------------------------
    # Calculate score
    # ----------------------------------------------

    score = calculate_resume_score(
        skills,
        sections
    )

    # ----------------------------------------------
    # Word count
    # ----------------------------------------------

    word_count = len(
        resume_text.split()
    )

    # ----------------------------------------------
    # Return result
    # ----------------------------------------------

    return {

        "success": True,

        "resume_text": resume_text,

        "skills": skills,

        "sections": sections,

        "score": score,

        "word_count": word_count

    }