import streamlit as st
import pandas as pd

from modules.resume_analyzer import analyze_resume
from modules.career_recommender import recommend_careers, load_careers
from modules.skill_analyzer import (
    analyze_skill_gap,
    get_learning_priority
)
from modules.progress_tracker import (
    load_progress,
    save_progress,
    calculate_progress,
    get_learning_insights
)
from modules.ai_helper import (
    get_ai_response,
    get_resume_feedback,
    generate_career_roadmap,
    generate_career_assessment,
    generate_learning_plan
)
from modules.ui import (
    load_css,
    hero_section,
    info_card
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareerMate AI",
    page_icon="🚀",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user_skills" not in st.session_state:
    st.session_state.user_skills = []

if "resume_result" not in st.session_state:
    st.session_state.resume_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 CareerMate AI")

st.sidebar.markdown(
    """
    ### Your AI Career Mentor

    📄 Analyze your resume  
    🎯 Discover careers  
    🧠 Find skill gaps  
    📈 Track progress  
    🤖 Get AI guidance
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 My Profile",
        "📄 Resume Analyzer",
        "🎯 Career Explorer",
        "🧠 Career Assessment",
        "🧠 Skill Gap",
        "🛣️ Career Roadmap",
        "📚 Learning Plan",
        "📈 Progress Tracker",
        "📊 Career Analytics",
        "🤖 AI Career Mentor"
    ]
)


# ==================================================
# HOME DASHBOARD 2.0
# ==================================================

if page == "🏠 Home":

    profile = load_progress()

    hero_section()

    # ----------------------------------------------
    # PROFILE DATA
    # ----------------------------------------------

    user_name = profile.get("name", "").strip()

    career_goal = profile.get(
        "career_goal",
        ""
    )

    completed_skills = profile.get(
        "completed_skills",
        []
    )

    user_skills = st.session_state.user_skills

    # ----------------------------------------------
    # WELCOME MESSAGE
    # ----------------------------------------------

    if user_name:

        st.subheader(
            f"Welcome back, {user_name}! 👋"
        )

    else:

        st.subheader(
            "Welcome to your career journey! 👋"
        )

    st.write(
        """
        CareerMate AI brings your career profile,
        skills, resume, learning journey, and AI
        guidance together in one place.
        """
    )

    st.divider()

    # ----------------------------------------------
    # CAREER STATUS
    # ----------------------------------------------

    st.subheader("🎯 Your Career Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Career Goal",
            career_goal
            if career_goal
            else "Not Set"
        )

    with col2:

        st.metric(
            "💻 Skills",
            len(user_skills)
        )

    with col3:

        resume_score = 0

        if st.session_state.resume_result:

            resume_score = st.session_state.resume_result.get(
                "score",
                0
            )

        st.metric(
            "📄 Resume Score",
            f"{resume_score}/100"
        )

    with col4:

        progress_percentage = 0

        if career_goal:

            careers = load_careers()

            career_data = careers[
                careers["career"] == career_goal
            ]

            if not career_data.empty:

                required_skills = [
                    skill.strip()
                    for skill in career_data.iloc[0][
                        "required_skills"
                    ].split(",")
                ]

                progress_percentage = calculate_progress(
                    completed_skills,
                    required_skills
                )

        st.metric(
            "📈 Progress",
            f"{progress_percentage}%"
        )

    st.divider()

    # ----------------------------------------------
    # PROFILE COMPLETENESS
    # ----------------------------------------------

    st.subheader("👤 Profile Overview")

    profile_fields = [
        bool(profile.get("name")),
        bool(profile.get("education")),
        bool(user_skills),
        bool(career_goal)
    ]

    profile_completion = (
        sum(profile_fields) / len(profile_fields)
    ) * 100

    st.progress(
        profile_completion / 100
    )

    st.caption(
        f"Profile completeness: "
        f"{profile_completion:.0f}%"
    )

    st.divider()

    # ----------------------------------------------
    # TOP CAREER MATCHES
    # ----------------------------------------------

    st.subheader("🏆 Top Career Matches")

    if user_skills:

        recommendations = recommend_careers(
            user_skills
        )

        top_matches = recommendations[:3]

        for index, career in enumerate(top_matches):

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.write(
                    f"**{index + 1}. "
                    f"{career['career']}**"
                )

                st.caption(
                    career["description"]
                )

            with col2:

                st.metric(
                    "Match",
                    f"{career['match_percentage']}%"
                )

    else:

        st.info(
            "Add your skills in My Profile or "
            "Resume Analyzer to see career matches."
        )

    st.divider()

    # ----------------------------------------------
    # NEXT ACTION
    # ----------------------------------------------

    st.subheader("🚀 Recommended Next Action")

    if not user_name:

        st.info(
            "👤 Complete your profile first so "
            "CareerMate can personalize your experience."
        )

    elif not user_skills:

        st.info(
            "💻 Add your technical skills or upload "
            "your resume to begin career analysis."
        )

    elif not career_goal:

        st.info(
            "🎯 Choose a career goal to unlock "
            "your personalized roadmap."
        )

    elif progress_percentage < 50:

        st.info(
            "📚 Focus on your missing skills and "
            "continue your learning plan."
        )

    else:

        st.success(
            "🔥 You're making great progress! "
            "Keep building projects and preparing "
            "for real-world opportunities."
        )


# ==================================================
# MY PROFILE
# ==================================================

elif page == "👤 My Profile":

    st.title("👤 My Career Profile")

    st.write(
        "Create your profile so CareerMate can personalize "
        "your career recommendations."
    )

    profile = load_progress()

    st.subheader("Personal Information")

    name = st.text_input(
        "Your Name",
        value=profile.get("name", "")
    )

    education = st.text_input(
        "Education",
        value=profile.get("education", ""),
        placeholder="B.Tech CSE"
    )

    st.subheader("💻 Your Skills")

    skills_input = st.text_area(
        "Enter your current skills",
        value=", ".join(
            st.session_state.user_skills
        ),
        placeholder="Python, C++, SQL, Git"
    )

    st.subheader("🎯 Career Goal")

    careers = load_careers()

    career_list = careers["career"].tolist()

    current_goal = profile.get(
        "career_goal",
        ""
    )

    default_index = (
        career_list.index(current_goal)
        if current_goal in career_list
        else 0
    )

    career_goal = st.selectbox(
        "Select your target career",
        career_list,
        index=default_index
    )

    if st.button("💾 Save My Profile"):

        skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        st.session_state.user_skills = skills

        save_progress(
            career_goal,
            profile.get(
                "completed_skills",
                []
            ),
            name=name,
            education=education
        )

        st.success(
            "🎉 Your CareerMate profile has been saved!"
        )

        st.rerun()

    st.divider()

    # ----------------------------------------------
    # PROFILE COMPLETENESS
    # ----------------------------------------------

    filled_fields = sum([
        bool(name.strip()),
        bool(education.strip()),
        bool(skills_input.strip()),
        bool(career_goal)
    ])

    profile_completion = (
        filled_fields / 4
    ) * 100

    st.subheader("📊 Profile Completeness")

    st.progress(
        profile_completion / 100
    )

    st.metric(
        "Profile Complete",
        f"{profile_completion:.0f}%"
    )


# ==================================================
# RESUME ANALYZER
# ==================================================

elif page == "📄 Resume Analyzer":

    st.title("📄 AI Resume Analyzer")

    st.write(
        """
        Upload your resume and CareerMate AI will analyze
        your resume structure, skills, score, career matches,
        and skill gaps.
        """
    )

    st.divider()

    # ----------------------------------------------
    # UPLOAD RESUME
    # ----------------------------------------------

    uploaded_file = st.file_uploader(
        "📤 Upload your resume",
        type=["pdf"],
        help="Upload your resume as a PDF file."
    )

    if uploaded_file:

        st.success(
            f"📄 {uploaded_file.name} uploaded successfully!"
        )

        if st.button(
            "🔍 Analyze My Resume"
        ):

            with st.spinner(
                "CareerMate AI is analyzing your resume..."
            ):

                # ----------------------------------
                # LOAD SKILL DATABASE
                # ----------------------------------

                try:

                    skills_data = pd.read_csv(
                        "data/skills.csv"
                    )

                    skill_list = (
                        skills_data["skill"]
                        .dropna()
                        .tolist()
                    )

                except Exception as e:

                    st.error(
                        f"Could not load skill database: {e}"
                    )

                    st.stop()


                # ----------------------------------
                # ANALYZE RESUME
                # ----------------------------------

                result = analyze_resume(
                    uploaded_file,
                    skill_list
                )


            # --------------------------------------
            # ERROR
            # --------------------------------------

            if not result["success"]:

                st.error(
                    result["error"]
                )

            else:

                # Save result
                st.session_state.resume_result = result

                detected_skills = result[
                    "skills"
                ]

                detected_sections = result[
                    "sections"
                ]

                resume_score = result[
                    "score"
                ]

                resume_text = result[
                    "resume_text"
                ]

                # ----------------------------------
                # OVERVIEW
                # ----------------------------------

                st.subheader(
                    "📊 Resume Overview"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Resume Score",
                        f"{resume_score}/100"
                    )

                with col2:

                    st.metric(
                        "Skills Detected",
                        len(detected_skills)
                    )

                with col3:

                    st.metric(
                        "Words",
                        result["word_count"]
                    )

                st.divider()

                # ----------------------------------
                # DETECTED SKILLS
                # ----------------------------------

                st.subheader(
                    "🧠 Detected Skills"
                )

                if detected_skills:

                    # Save skills globally
                    st.session_state.user_skills = (
                        detected_skills
                    )

                    skill_columns = st.columns(4)

                    for index, skill in enumerate(
                        detected_skills
                    ):

                        with skill_columns[
                            index % 4
                        ]:

                            st.info(
                                f"💻 {skill}"
                            )

                else:

                    st.warning(
                        "No known technical skills "
                        "were detected."
                    )

                st.divider()

                # ----------------------------------
                # RESUME SECTIONS
                # ----------------------------------

                st.subheader(
                    "📑 Resume Sections"
                )

                if detected_sections:

                    for section in (
                        detected_sections
                    ):

                        st.success(
                            f"✓ {section}"
                        )

                else:

                    st.warning(
                        "No standard resume sections "
                        "were detected."
                    )

                st.divider()

                # ----------------------------------
                # CAREER MATCHING
                # ----------------------------------

                st.subheader(
                    "🎯 Career Matches"
                )

                if detected_skills:

                    recommendations = (
                        recommend_careers(
                            detected_skills
                        )
                    )

                    # Save recommendations
                    st.session_state.career_recommendations = (
                        recommendations
                    )

                    for career in (
                        recommendations[:5]
                    ):

                        with st.expander(
                            f"🎯 "
                            f"{career['career']} — "
                            f"{career['match_percentage']}%"
                        ):

                            st.write(
                                career[
                                    "description"
                                ]
                            )

                            st.write(
                                f"**Category:** "
                                f"{career['category']}"
                            )

                            st.write(
                                f"**Difficulty:** "
                                f"{career['difficulty']}"
                            )

                            st.write(
                                "**Matching Skills:** "
                                + (
                                    ", ".join(
                                        career[
                                            "matched_skills"
                                        ]
                                    )
                                    if career[
                                        "matched_skills"
                                    ]
                                    else "None"
                                )
                            )

                            st.write(
                                "**Tools:** "
                                + ", ".join(
                                    career["tools"]
                                )
                            )

                else:

                    st.info(
                        "Add skills to your resume "
                        "to generate career matches."
                    )

                st.divider()

                # ----------------------------------
                # BEST CAREER + SKILL GAP
                # ----------------------------------

                if detected_skills:

                    recommendations = (
                        st.session_state.get(
                            "career_recommendations",
                            []
                        )
                    )

                    if recommendations:

                        best_career = (
                            recommendations[0]
                        )

                        st.subheader(
                            "🧠 Skill Gap Analysis"
                        )

                        st.write(
                            f"### 🥇 Best Match: "
                            f"{best_career['career']}"
                        )

                        gap_result = (
                            analyze_skill_gap(
                                detected_skills,
                                best_career["career"]
                            )
                        )

                        if "error" not in gap_result:

                            col1, col2 = st.columns(2)

                            with col1:

                                st.metric(
                                    "Current Match",
                                    f"{gap_result['match_percentage']}%"
                                )

                            with col2:

                                st.metric(
                                    "Skills to Develop",
                                    len(
                                        gap_result[
                                            "missing_skills"
                                        ]
                                    )
                                )

                            missing_skills = (
                                gap_result[
                                    "missing_skills"
                                ]
                            )

                            if missing_skills:

                                st.write(
                                    "### 📚 Skills to Learn"
                                )

                                for skill in (
                                    missing_skills
                                ):

                                    st.warning(
                                        f"📌 {skill}"
                                    )

                            else:

                                st.success(
                                    "🎉 You already have "
                                    "all required skills!"
                                )

                st.divider()

                # ----------------------------------
                # AI RESUME FEEDBACK
                # ----------------------------------

                st.subheader(
                    "🤖 AI Resume Review"
                )

                st.write(
                    "Get detailed feedback from "
                    "CareerMate AI."
                )

                if st.button(
                    "✨ Get AI Resume Feedback"
                ):

                    with st.spinner(
                        "CareerMate AI is reviewing "
                        "your resume..."
                    ):

                        feedback = (
                            get_resume_feedback(
                                resume_text
                            )
                        )

                    st.markdown(
                        feedback
                    )


# ==================================================
# CAREER EXPLORER
# ==================================================

elif page == "🎯 Career Explorer":

    st.title("🎯 Career Explorer")

    st.write(
        "Discover careers that match your current skills."
    )

    skills_input = st.text_area(
        "💻 Enter your skills",
        value=", ".join(
            st.session_state.user_skills
        ),
        placeholder="Python, SQL, Pandas, Git"
    )

    if st.button("🔍 Find My Career Matches"):

        user_skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        st.session_state.user_skills = user_skills

        if not user_skills:

            st.warning(
                "Please enter at least one skill."
            )

        else:

            recommendations = recommend_careers(
                user_skills
            )

            st.subheader("🏆 Your Career Matches")

            for career in recommendations:

                with st.expander(
                    f"🎯 {career['career']} — "
                    f"{career['match_percentage']}%"
                ):

                    st.write(
                        career["description"]
                    )

                    st.write(
                        f"**Category:** "
                        f"{career['category']}"
                    )

                    st.write(
                        f"**Difficulty:** "
                        f"{career['difficulty']}"
                    )

                    st.subheader(
                        "🧠 Matching Skills"
                    )

                    if career["matched_skills"]:

                        st.write(
                            ", ".join(
                                career["matched_skills"]
                            )
                        )

                    else:

                        st.write(
                            "No matching skills yet."
                        )

                    st.subheader(
                        "🛠️ Recommended Tools"
                    )

                    st.write(
                        ", ".join(
                            career["tools"]
                        )
                    )

                    st.subheader(
                        "🚀 Portfolio Projects"
                    )

                    for project in career["projects"]:

                        st.write(
                            f"• {project}"
                        )


# ==================================================
# CAREER ASSESSMENT
# ==================================================

elif page == "🧠 Career Assessment":

    st.title("🧠 AI Career Assessment")

    st.write(
        """
        Answer a few questions about your interests,
        strengths, and goals. CareerMate AI will analyze
        your responses and suggest suitable career paths.
        """
    )

    st.divider()

    # ----------------------------------------------
    # INTERESTS
    # ----------------------------------------------

    interests = st.multiselect(
        "💡 What are you interested in?",
        [
            "Building software",
            "Artificial Intelligence",
            "Data and Analytics",
            "Web Development",
            "Cybersecurity",
            "Databases",
            "Problem Solving",
            "Research",
            "Automation",
            "Creative Technology"
        ]
    )

    # ----------------------------------------------
    # STRENGTHS
    # ----------------------------------------------

    strengths = st.multiselect(
        "🧩 What are your strongest areas?",
        [
            "Logical Thinking",
            "Mathematics",
            "Programming",
            "Communication",
            "Creativity",
            "Problem Solving",
            "Teamwork",
            "Research",
            "Learning Quickly",
            "Attention to Detail"
        ]
    )

    # ----------------------------------------------
    # WORK PREFERENCE
    # ----------------------------------------------

    work_preference = st.radio(
        "🛠️ What type of work sounds most interesting?",
        [
            "Building applications",
            "Working with data",
            "Creating AI systems",
            "Designing websites",
            "Securing systems",
            "Managing databases",
            "Research and experimentation"
        ]
    )

    # ----------------------------------------------
    # WORK STYLE
    # ----------------------------------------------

    work_style = st.radio(
        "📊 Which work environment do you prefer?",
        [
            "Independent work",
            "Collaborative teams",
            "A mix of both",
            "I am still exploring"
        ]
    )

    # ----------------------------------------------
    # CAREER PRIORITY
    # ----------------------------------------------

    career_priority = st.selectbox(
        "🎯 What matters most to you?",
        [
            "Building strong technical skills",
            "Getting an internship",
            "Getting a job",
            "High-growth career",
            "Entrepreneurship",
            "Exploring different fields"
        ]
    )

    # ----------------------------------------------
    # CURRENT SKILLS
    # ----------------------------------------------

    assessment_skills = st.text_area(
        "💻 Your Current Skills",
        value=", ".join(
            st.session_state.user_skills
        ),
        placeholder="Python, C++, SQL, Git"
    )

    # ----------------------------------------------
    # GENERATE ASSESSMENT
    # ----------------------------------------------

    if st.button("🚀 Analyze My Career Profile"):

        if not interests or not strengths:

            st.warning(
                "Please select at least one interest "
                "and one strength."
            )

        else:

            current_skills = [
                skill.strip()
                for skill in assessment_skills.split(",")
                if skill.strip()
            ]

            st.session_state.user_skills = current_skills

            with st.spinner(
                "CareerMate AI is analyzing your profile..."
            ):

                assessment = generate_career_assessment(
                    interests,
                    strengths,
                    work_preference,
                    work_style,
                    career_priority,
                    current_skills
                )

            st.success(
                "🎉 Your personalized career assessment is ready!"
            )

            st.divider()

            st.markdown(assessment)


# ==================================================
# SKILL GAP ANALYZER
# ==================================================

elif page == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analyzer")

    careers = load_careers()

    career_list = careers["career"].tolist()

    selected_career = st.selectbox(
        "Select Your Dream Career",
        career_list
    )

    skills_input = st.text_area(
        "Your Current Skills",
        value=", ".join(st.session_state.user_skills)
    )

    if st.button("🔍 Analyze My Skill Gap"):

        user_skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        st.session_state.user_skills = user_skills

        result = analyze_skill_gap(
            user_skills,
            selected_career
        )

        if "error" in result:

            st.error(result["error"])

        else:

            st.metric(
                "Skill Match",
                f"{result['match_percentage']}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Skills You Have")

                for skill in result["matched_skills"]:
                    st.success(skill)

            with col2:

                st.subheader("📚 Skills to Learn")

                for skill in result["missing_skills"]:
                    st.warning(skill)

            st.subheader("🛣️ Learning Priority")

            priorities = get_learning_priority(
                result["missing_skills"]
            )

            priority_df = pd.DataFrame(priorities)

            if not priority_df.empty:
                st.dataframe(
                    priority_df,
                    use_container_width=True
                )


# ==================================================
# CAREER ROADMAP
# ==================================================

elif page == "🛣️ Career Roadmap":

    st.title("🛣️ Your Personalized Career Roadmap")

    st.write(
        "Create an AI-powered learning roadmap based on "
        "your current skills and career goal."
    )

    careers = load_careers()

    career_list = careers["career"].tolist()

    selected_career = st.selectbox(
        "🎯 Select Your Career Goal",
        career_list
    )

    skills_input = st.text_area(
        "🧠 Your Current Skills",
        value=", ".join(st.session_state.user_skills),
        placeholder="Python, SQL, Pandas, Git"
    )

    if st.button("🚀 Generate My Career Roadmap"):

        current_skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        st.session_state.user_skills = current_skills

        with st.spinner(
            "CareerMate AI is creating your personalized roadmap..."
        ):

            skill_result = analyze_skill_gap(
                current_skills,
                selected_career
            )

            if "error" in skill_result:

                st.error(skill_result["error"])

            else:

                roadmap = generate_career_roadmap(
                    selected_career,
                    current_skills,
                    skill_result["missing_skills"]
                )

                st.success(
                    "Your personalized roadmap is ready! 🚀"
                )

                st.divider()

                st.markdown(roadmap)


# ==================================================
# LEARNING PLAN
# ==================================================

elif page == "📚 Learning Plan":

    st.title("📚 Personalized Learning Plan")

    st.write(
        """
        Turn your skill gaps into an actionable learning plan.
        CareerMate AI will organize what you need to learn,
        practice, build, and achieve.
        """
    )

    st.divider()

    careers = load_careers()

    career_list = careers["career"].tolist()

    selected_career = st.selectbox(
        "🎯 Select Your Career Goal",
        career_list
    )

    skills_input = st.text_area(
        "🧠 Your Current Skills",
        value=", ".join(
            st.session_state.user_skills
        ),
        placeholder="Python, SQL, Pandas, Git"
    )

    if st.button("🔍 Analyze Skill Gap"):

        current_skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        st.session_state.user_skills = current_skills

        result = analyze_skill_gap(
            current_skills,
            selected_career
        )

        if "error" in result:

            st.error(result["error"])

        else:

            st.session_state.learning_gap = result

            st.subheader("📊 Your Skill Gap")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Skill Match",
                    f"{result['match_percentage']}%"
                )

            with col2:

                st.metric(
                    "Skills You Have",
                    len(result["matched_skills"])
                )

            with col3:

                st.metric(
                    "Skills to Learn",
                    len(result["missing_skills"])
                )

            st.divider()

            st.subheader("📚 Skills You Need")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:

                    st.warning(
                        f"📌 {skill}"
                    )

            else:

                st.success(
                    "🎉 You already have all required skills!"
                )


    # ----------------------------------------------
    # GENERATE PLAN
    # ----------------------------------------------

    if "learning_gap" in st.session_state:

        result = st.session_state.learning_gap

        st.divider()

        if st.button(
            "🚀 Generate My Learning Plan"
        ):

            with st.spinner(
                "CareerMate AI is building your learning plan..."
            ):

                plan = generate_learning_plan(
                    result["career"],
                    result["matched_skills"],
                    result["missing_skills"]
                )

            st.success(
                "🎉 Your personalized learning plan is ready!"
            )

            st.divider()

            st.markdown(plan)


# ==================================================
# PROGRESS TRACKER
# ==================================================

elif page == "📈 Progress Tracker":

    st.title("📈 Career Progress Tracker")

    careers = load_careers()

    career_list = careers["career"].tolist()

    saved_progress = load_progress()

    selected_goal = st.selectbox(
        "Select Your Career Goal",
        career_list,
        index=(
            career_list.index(saved_progress["career_goal"])
            if saved_progress["career_goal"] in career_list
            else 0
        )
    )

    career_data = careers[
        careers["career"] == selected_goal
    ].iloc[0]

    required_skills = [
        skill.strip()
        for skill in career_data["required_skills"].split(",")
    ]

    completed_skills = st.multiselect(
        "Select Skills You Have Completed",
        required_skills,
        default=[
            skill
            for skill in saved_progress["completed_skills"]
            if skill in required_skills
        ]
    )

    if st.button("💾 Save Progress"):

        save_progress(
            selected_goal,
            completed_skills
        )

        st.success("Progress saved successfully!")

    progress_percentage = calculate_progress(
        completed_skills,
        required_skills
    )

    st.progress(progress_percentage / 100)

    st.metric(
        "Career Progress",
        f"{progress_percentage}%"
    )

    st.info(
        get_learning_insights(progress_percentage)
    )

    st.subheader("📚 Required Skills")

    for skill in required_skills:

        if skill in completed_skills:
            st.success(f"✓ {skill}")

        else:
            st.warning(f"○ {skill}")


# ==================================================
# CAREER ANALYTICS
# ==================================================

elif page == "📊 Career Analytics":

    st.title("📊 Career Analytics Dashboard")

    st.write(
        "Visualize your career matches, skill progress, "
        "and learning journey."
    )

    import plotly.express as px


    # ----------------------------------------------
    # CAREER MATCH ANALYSIS
    # ----------------------------------------------

    st.subheader("🎯 Career Match Comparison")

    if not st.session_state.user_skills:

        st.warning(
            "Add your skills first in the Career Explorer "
            "to view personalized analytics."
        )

    else:

        recommendations = recommend_careers(
            st.session_state.user_skills
        )

        chart_data = pd.DataFrame(
            recommendations
        )

        fig = px.bar(
            chart_data,
            x="career",
            y="match_percentage",
            title="Career Match Percentage",
            text="match_percentage"
        )

        fig.update_layout(
            xaxis_title="Career",
            yaxis_title="Match Percentage"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ----------------------------------------------
    # SKILL PROGRESS ANALYSIS
    # ----------------------------------------------

    st.divider()

    st.subheader("🧠 Skills Progress")

    saved_progress = load_progress()

    if saved_progress["career_goal"]:

        careers = load_careers()

        career_data = careers[
            careers["career"]
            == saved_progress["career_goal"]
        ]

        if not career_data.empty:

            required_skills = [
                skill.strip()
                for skill in career_data.iloc[0][
                    "required_skills"
                ].split(",")
            ]

            completed_skills = [
                skill
                for skill in required_skills
                if skill in saved_progress["completed_skills"]
            ]

            remaining_skills = [
                skill
                for skill in required_skills
                if skill not in completed_skills
            ]

            progress_data = pd.DataFrame({
                "Status": [
                    "Completed",
                    "Remaining"
                ],

                "Skills": [
                    len(completed_skills),
                    len(remaining_skills)
                ]
            })

            fig = px.pie(
                progress_data,
                names="Status",
                values="Skills",
                title=(
                    f"Skill Progress for "
                    f"{saved_progress['career_goal']}"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            progress_percentage = calculate_progress(
                saved_progress["completed_skills"],
                required_skills
            )

            st.metric(
                "Overall Career Progress",
                f"{progress_percentage}%"
            )

    else:

        st.info(
            "Set a career goal in the Progress Tracker "
            "to see your learning analytics."
        )


# ==================================================
# AI CAREER MENTOR
# ==================================================

elif page == "🤖 AI Career Mentor":

    st.title("🤖 CareerMate AI Mentor")

    st.write(
        "Ask questions about careers, skills, projects, "
        "internships, resumes, and learning paths."
    )

    col1, col2 = st.columns([4, 1])

    with col1:
        st.caption(
            "💡 Your AI-powered personal career guide"
        )

    with col2:
        if st.button("🗑️ Clear Chat"):

            st.session_state.chat_history = []

            st.rerun()


    # ----------------------------------------------
    # DISPLAY CHAT HISTORY
    # ----------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # ----------------------------------------------
    # CHAT INPUT
    # ----------------------------------------------

    user_question = st.chat_input(
        "Ask CareerMate anything about your career..."
    )

    if user_question:

        # Save and display user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):

            st.markdown(user_question)


        # Build conversation context
        conversation = ""

        for message in st.session_state.chat_history[-6:]:

            role = message["role"]

            content = message["content"]

            conversation += (
                f"{role.upper()}: {content}\n\n"
            )


        prompt = f"""
You are CareerMate AI, a friendly, practical,
and encouraging AI career mentor.

The user's known skills are:
{", ".join(st.session_state.user_skills)
 if st.session_state.user_skills else "Not provided yet"}

Conversation so far:
{conversation}

Respond to the user's latest message.

Give practical and personalized guidance.
Use headings and bullet points when useful.
Keep answers clear and suitable for a student.
"""


        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner("CareerMate is thinking..."):

                response = get_ai_response(prompt)

            st.markdown(response)


        # Save AI response
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )