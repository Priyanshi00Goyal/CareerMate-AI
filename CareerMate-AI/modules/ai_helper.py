import os

from dotenv import load_dotenv
from google import genai


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# GEMINI CLIENT
# ==================================================

def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Check your .env file."
        )

    api_key = api_key.strip()

    return genai.Client(
        api_key=api_key
    )


# ==================================================
# GENERAL AI RESPONSE
# ==================================================

def get_ai_response(prompt):

    try:

        client = get_client()

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response.text:

            return response.text

        return "AI did not return any text."

    except Exception as e:

        return f"AI Error: {str(e)}"


# ==================================================
# RESUME FEEDBACK
# ==================================================

def get_resume_feedback(resume_text):

    prompt = f"""
You are an expert career counselor and professional
resume reviewer.

Analyze the following resume and provide constructive,
practical feedback.

RESUME:
----------------
{resume_text}
----------------

Return your response using exactly these sections:

## Overall Assessment

Give a short overall assessment.

## Strengths

List the strongest aspects of the resume.

## Areas for Improvement

List specific areas that should be improved.

## Missing or Weak Information

Mention important information that appears missing
or weak.

## Action Plan

Give 5 clear and practical steps to improve the resume.

Be encouraging, specific, and professional.

Do not invent information that is not present
in the resume.
"""

    return get_ai_response(prompt)


# ==================================================
# CAREER ROADMAP
# ==================================================

def generate_career_roadmap(
    career_goal,
    current_skills,
    missing_skills
):

    prompt = f"""
You are CareerMate AI, an expert career mentor.

Create a practical and personalized learning roadmap.

Career Goal:
{career_goal}

Current Skills:
{
    ", ".join(current_skills)
    if current_skills
    else "No skills provided"
}

Skills to Learn:
{
    ", ".join(missing_skills)
    if missing_skills
    else "None"
}

Create a roadmap using exactly these sections:

## 🎯 Career Goal

Briefly explain the target role.

## 📍 Current Position

Explain how the user's current skills help them.

## 🛣️ Phase 1: Foundation

List the first skills and concepts to focus on.

## 🛣️ Phase 2: Skill Development

Explain what to learn next.

## 🛣️ Phase 3: Projects and Practice

Suggest 3 practical portfolio projects.

## 🛣️ Phase 4: Career Preparation

Explain how to prepare for internships or jobs.

## 📅 Suggested Timeline

Provide a realistic phase-by-phase timeline.

## 🚀 Next Best Steps

Give 5 clear actions the user should take next.

Make the roadmap practical, structured, encouraging,
and suitable for a student or beginner.
"""

    return get_ai_response(prompt)


# ==================================================
# CAREER ASSESSMENT
# ==================================================

def generate_career_assessment(
    interests,
    strengths,
    work_preference,
    work_style,
    career_priority,
    current_skills
):

    prompt = f"""
You are CareerMate AI, an expert career counselor.

Analyze the following student's career assessment.

INTERESTS:
{interests}

STRENGTHS:
{strengths}

PREFERRED WORK:
{work_preference}

WORK STYLE:
{work_style}

CAREER PRIORITY:
{career_priority}

CURRENT TECHNICAL SKILLS:
{
    ", ".join(current_skills)
    if current_skills
    else "Not provided"
}

Provide a personalized career assessment.

Use exactly these sections:

## 🎯 Top Career Matches

Recommend the 3 most suitable career paths.

For each career include:

- Career name
- Why it matches
- Relevant skills
- Skills to develop

## 🥇 Best Match

Identify the single strongest career option
and explain why.

## 🧠 Skill Development

List the most important skills the student
should develop.

## 🛠️ Recommended Projects

Suggest 3 projects that would help explore
and prepare for the recommended careers.

## 🚀 Next Steps

Give 5 practical actions the student can take.

Do not guarantee that any career is perfect.

Base recommendations only on the information provided.

Be encouraging, realistic, and suitable for a student.
"""

    return get_ai_response(prompt)


# ==================================================
# LEARNING PLAN
# ==================================================

def generate_learning_plan(
    career_goal,
    current_skills,
    missing_skills
):

    prompt = f"""
You are CareerMate AI, an expert technical learning mentor.

Create a personalized learning plan for a student.

CAREER GOAL:
{career_goal}

CURRENT SKILLS:
{
    ", ".join(current_skills)
    if current_skills
    else "None"
}

MISSING SKILLS:
{
    ", ".join(missing_skills)
    if missing_skills
    else "None"
}

Create a practical learning plan.

For every important missing skill, explain:

1. What the skill is
2. Important concepts to learn
3. What to practice
4. A small project or exercise
5. A milestone to know when the skill is understood

Use exactly these sections:

## 🎯 Learning Goal

Explain what the student is working toward.

## 📚 Skill-by-Skill Plan

For each missing skill include:

### Skill Name

**What to Learn**

- Concept 1
- Concept 2
- Concept 3

**Practice**

- Practice idea 1
- Practice idea 2

**Mini Project**

- One practical project

**Milestone**

- A clear condition that indicates progress.

## 🛠️ Portfolio Projects

Suggest 3 projects that combine multiple skills.

For each project include:

- Project idea
- Skills used
- Main features

## 📅 Suggested Schedule

Create a realistic weekly learning sequence.

## 🚀 Final Milestones

Give 5 milestones that show the student is
progressing toward the career goal.

Keep the plan practical and suitable for a student.

Do not assume the student already knows skills
listed as missing.
"""

    return get_ai_response(prompt)