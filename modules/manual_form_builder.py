def build_manual_cv_data(personal, summary, experience, education, skills):
    """
    Combines manual form data into a structured format for the LaTeX generator.
    """
    return {
        "personal": personal,
        "summary": summary,
        "experience": experience,
        "education": education,
        "skills": skills
    }
