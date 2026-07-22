REALITY_CHECK_PROMPT = """
You are a highly critical, strict, and realistic technical recruiter and ATS system.
Your job is to ruthlessly evaluate if this candidate is genuinely a strong fit for this exact role. 

CRITICAL INSTRUCTIONS FOR EVALUATION:
- DO NOT sugarcoat the match percentage. If the candidate is a Cybersecurity Engineer applying for a Business Strategy Consulting role, the match should be VERY LOW (e.g., 20-30%) because the core day-to-day functions do not align.
- Only give 80%+ if they have the EXACT title or perform the EXACT same core duties required in the JD.
- Look closely at mandatory requirements (consulting experience, specific languages, strategy background).
- Identify brutally honest missing skills.

CV:
{cv_text}

Job Description:
{jd_text}

Analyze the match and return a STRICT JSON output matching exactly this schema:
{{
  "match_percentage": "85%",
  "minimum_experience": "Required: X years. You have: Y years. (✅ Meets / ❌ Does not meet)",
  "critical_missing_skills": ["Skill 1", "Skill 2"],
  "your_superpower": "One sentence identifying the candidate's strongest unique selling point for this role.",
  "target_role_extracted": "Extracted Job Role from JD",
  "target_company_extracted": "Extracted Company Name from JD"
}}
"""

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
  "target_role_extracted": "Extracted Job Role from JD (e.g. SOC Analyst)",
  "target_company_extracted": "Extracted Company Name from JD (e.g. Microsoft)",
  "name": "Your Name",
  "contact": ["email@example.com", "Phone Number", "LinkedIn/GitHub", "Location"],
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
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "University/School",
      "dates": "Start - End",
      "location": "Location"
    }}
  ],
  "certifications": ["Cert 1", "Cert 2"],
  "languages": ["Lang 1", "Lang 2"]
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

CRITICAL: Output the result in STRICT JSON format exactly matching this schema:
{{
  "target_role_extracted": "Extracted Job Role from JD",
  "target_company_extracted": "Extracted Company Name from JD",
  "name": "Your Name (extracted from CV)",
  "contact": ["email@example.com", "Phone", "Location"],
  "body": "The complete raw text of the cover letter..."
}}
"""
