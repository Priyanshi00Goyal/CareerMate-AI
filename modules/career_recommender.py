import pandas as pd


CAREER_FILE = "data/careers.csv"


def load_careers():

    return pd.read_csv(
        CAREER_FILE
    )


def recommend_careers(user_skills):

    careers = load_careers()

    user_skills_lower = {
        skill.strip().lower()
        for skill in user_skills
    }

    recommendations = []

    for _, career in careers.iterrows():

        required_skills = [
            skill.strip()
            for skill in career["required_skills"].split(",")
        ]

        required_lower = {
            skill.lower()
            for skill in required_skills
        }

        matched_skills = (
            user_skills_lower
            & required_lower
        )

        if required_lower:

            match_percentage = round(
                (
                    len(matched_skills)
                    / len(required_lower)
                ) * 100
            )

        else:

            match_percentage = 0

        recommendations.append({

            "career": career["career"],

            "category": career["category"],

            "description": career["description"],

            "match_percentage": match_percentage,

            "matched_skills": list(
                matched_skills
            ),

            "required_skills": required_skills,

            "tools": career["tools"].split(","),

            "projects": career["projects"].split(","),

            "difficulty": career["difficulty"]
        })

    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations
