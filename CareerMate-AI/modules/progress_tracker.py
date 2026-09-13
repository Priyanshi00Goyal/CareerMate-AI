import json
import os


DATA_FILE = "user_data/progress.json"


def default_profile():

    return {
        "name": "",
        "education": "",
        "career_goal": "",
        "completed_skills": []
    }


def load_progress():
    """Load saved user profile and progress."""

    if not os.path.exists(DATA_FILE):
        return default_profile()

    try:

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        profile = default_profile()
        profile.update(data)

        return profile

    except (json.JSONDecodeError, FileNotFoundError):

        return default_profile()


def save_progress(
    career_goal,
    completed_skills,
    name=None,
    education=None
):
    """Save user profile and learning progress."""

    existing_data = load_progress()

    data = {
        "name": (
            name
            if name is not None
            else existing_data.get("name", "")
        ),

        "education": (
            education
            if education is not None
            else existing_data.get("education", "")
        ),

        "career_goal": career_goal,

        "completed_skills": completed_skills
    }

    os.makedirs(
        os.path.dirname(DATA_FILE),
        exist_ok=True
    )

    with open(DATA_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


def calculate_progress(
    completed_skills,
    required_skills
):
    """Calculate learning progress percentage."""

    if not required_skills:
        return 0

    completed_lower = [
        skill.lower().strip()
        for skill in completed_skills
    ]

    completed_count = sum(
        skill.lower() in completed_lower
        for skill in required_skills
    )

    return round(
        (completed_count / len(required_skills)) * 100,
        1
    )


def get_learning_insights(progress_percentage):
    """Generate learning insights."""

    if progress_percentage == 0:

        return (
            "🌱 Your journey is just beginning. "
            "Start by learning your first required skill!"
        )

    elif progress_percentage < 30:

        return (
            "🚀 Great start! Keep building your foundation."
        )

    elif progress_percentage < 60:

        return (
            "🔥 You're making solid progress. "
            "Keep practicing consistently!"
        )

    elif progress_percentage < 90:

        return (
            "💪 Excellent progress! You're getting close "
            "to your career goal."
        )

    else:

        return (
            "🏆 Outstanding! You've completed most "
            "of your required skills."
        )