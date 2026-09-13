import pandas as pd


def load_careers():
    """Load career data."""

    return pd.read_csv("data/careers.csv")


def analyze_skill_gap(user_skills, selected_career):
    """
    Compare user skills with the skills required
    for a selected career.
    """

    careers = load_careers()

    career_data = careers[
        careers["career"].str.lower()
        == selected_career.lower()
    ]

    if career_data.empty:
        return {
            "error": "Career not found."
        }

    career = career_data.iloc[0]

    required_skills = [
        skill.strip()
        for skill in career["required_skills"].split(",")
    ]

    user_skills_lower = [
        skill.lower().strip()
        for skill in user_skills
    ]

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in user_skills_lower:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    match_percentage = round(
        (len(matched_skills) / len(required_skills)) * 100,
        1
    )

    return {
        "career": career["career"],
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }


def get_learning_priority(missing_skills):
    """
    Assign learning priorities to missing skills.
    """

    priorities = []

    for index, skill in enumerate(missing_skills):

        if index < 2:
            priority = "High"

        elif index < 4:
            priority = "Medium"

        else:
            priority = "Low"

        priorities.append({
            "skill": skill,
            "priority": priority
        })

    return priorities
