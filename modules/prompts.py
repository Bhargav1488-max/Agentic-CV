TAILOR_CV_PROMPT = """
You are an expert ATS-optimized CV writer.
I have a Master CV and a target Job Description.

Please process the CV according to these specific section rules:
- CV Title (Modify: {modify_title}): If True, completely change the CV title to match the target role. If False, use the exact title from the Master CV.
- Professional Summary (Modify: {modify_summary}): If True, AGGRESSIVELY rewrite the summary to highlight relevance to the JD, mirroring their tone and keywords. If False, keep the exact original.
- Technical Skills (Modify: {modify_skills}): If True, forcefully reorder, inject, and highlight skills that are explicitly requested in the JD. If False, keep the exact original.
- Professional Experience (Modify: {modify_exp}): If True, AGGRESSIVELY REWRITE the bullet points. Do not just copy the original. Reframe your achievements, metrics, and responsibilities to sound exactly like what the Job Description is asking for. If False, use the exact original bullets.

Master CV:
{cv_text}

Job Description:
{jd_text}

Target Role: {role}
Company: {company}
Language: {language}

CRITICAL: Output the CV in STRICT JSON format exactly matching this schema (no extra text, no markdown):
{{
  "title": "Your Tailored CV Title Here (e.g. Forward Deployed Engineer | Data Science)",
  "summary": "Your tailored or original professional summary here...",
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "location": "Location",
      "dates": "Start - End",
      "highlights": [
        "Bullet point 1",
        "Bullet point 2"
      ]
    }}
  ]
}}
"""

COVER_LETTER_PROMPT = """
You are an expert career consultant. Write a professional cover letter based on the provided CV and Job Description.

CV:
{cv_text}

Job Description:
{jd_text}

Target Role: {role}
Company: {company}
Language: {language}

Output just the raw cover letter text, properly formatted. No JSON, no markdown code blocks, just the text.
"""
