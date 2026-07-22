import streamlit as st
import json
import re
import os
import shutil
from pathlib import Path
from modules import cv_parser, jd_scraper, prompts, llm_engine, latex_generator, latex_compiler

def clean_json_response(text):
    """Utility to clean up markdown formatting if the LLM returns json wrapped in code blocks."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def save_to_downloads(file_path, target_filename, role, company):
    """Save a file directly to the user's Downloads folder inside role_company subfolder."""
    if not file_path or not os.path.exists(file_path):
        return
        
    role_safe = re.sub(r'[^A-Za-z0-9_\-]', '_', str(role).strip() or "Unknown_Role")
    comp_safe = re.sub(r'[^A-Za-z0-9_\-]', '_', str(company).strip() or "Unknown_Company")
    
    downloads_dir = Path.home() / "Downloads"
    app_dir = downloads_dir / "AI-Powered_Job_Application_Engine_saved_CV"
    job_dir = app_dir / f"{role_safe}_{comp_safe}"
    
    os.makedirs(job_dir, exist_ok=True)
    
    dest_path = job_dir / target_filename
    shutil.copy(file_path, dest_path)
    
    return str(dest_path)

def render():
    st.header("Tailor CV to Job Description")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Upload Master CV")
        uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
        
    with col2:
        st.subheader("2. Job Description")
        jd_input_mode = st.radio("Input Method", ["Paste Text", "URL Scraping"])
        
        jd_text_input = ""
        jd_url = ""
        if jd_input_mode == "Paste Text":
            jd_text_input = st.text_area("Paste JD here", height=200)
        else:
            jd_url = st.text_input("Job Posting URL")
            if st.button("Scrape URL"):
                scraped = jd_scraper.scrape_jd(jd_url)
                st.session_state["jd_text_scraped"] = scraped
                st.success("JD Scraped successfully!")
                
        # Final JD text resolution
        if jd_input_mode == "Paste Text":
            final_jd_text = jd_text_input
        else:
            final_jd_text = st.session_state.get("jd_text_scraped", "")
            
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        job_role = ""
        company = ""
        
        generate_cv = st.checkbox("Generate Tailored CV", value=True)
        generate_cl = st.checkbox("Generate Cover Letter", value=True)
        
    with col_b:
        st.write("Sections to Tailor (uncheck to keep original):")
        modify_title = st.checkbox("CV Title", value=True)
        modify_summary = st.checkbox("Professional Summary", value=True)
        modify_skills = st.checkbox("Technical Skills", value=True)
        modify_exp = st.checkbox("Professional Experience", value=True)
        run_reality = st.checkbox("Show Reality Check Analysis", value=True)
        
    if st.button("🚀 Generate Applications", type="primary"):
        total_in_tokens = 0
        total_out_tokens = 0
        if not uploaded_file:
            st.error("Please upload a CV first.")
            return
            
        if not final_jd_text:
            st.error("Please provide a Job Description.")
            return
            
        provider = st.session_state.get("selected_provider")
        model = st.session_state.get("selected_model")
        api_key = st.session_state.get("api_key")
        
        if not provider or not api_key:
            st.error("Please configure the LLM Provider and API Key in the sidebar.")
            return
            
        st.info("Parsing CV...")
        cv_text = cv_parser.parse_cv(uploaded_file)
        
        if run_reality:
            with st.spinner("Analyzing Reality Check..."):
                rc_prompt = prompts.REALITY_CHECK_PROMPT.format(cv_text=cv_text, jd_text=final_jd_text)
                response_text, in_tok, out_tok = llm_engine.generate_text(provider, model, rc_prompt, api_key)
                total_in_tokens += in_tok
                total_out_tokens += out_tok
                
                if response_text.startswith("Error"):
                    st.error(response_text)
                else:
                    try:
                        clean_json = clean_json_response(response_text)
                        rc_data = json.loads(clean_json)
                        
                        st.session_state["extracted_role"] = rc_data.get("target_role_extracted", "Unknown_Role")
                        st.session_state["extracted_company"] = rc_data.get("target_company_extracted", "Unknown_Company")
                        
                        st.subheader("📊 Reality Check Results")
                        mcol1, mcol2, mcol3 = st.columns(3)
                        mcol1.metric("Match Percentage", rc_data.get("match_percentage", "N/A"))
                        mcol2.write(f"**Experience:** {rc_data.get('minimum_experience', 'N/A')}")
                        mcol3.write(f"**Role:** {rc_data.get('target_role_extracted')} @ {rc_data.get('target_company_extracted')}")
                        
                        st.info(f"**Your Superpower:** {rc_data.get('your_superpower', '')}")
                        
                        missing = rc_data.get('critical_missing_skills', [])
                        if missing:
                            st.warning(f"**Critical Missing Skills:** {', '.join(missing)}")
                        else:
                            st.success("**No critical skills missing!**")
                            
                    except json.JSONDecodeError:
                        st.error("Failed to parse Reality Check. Raw output:")
                        st.write(response_text)
                        
        if st.session_state.get("latest_jd_text") != final_jd_text:
            st.session_state.pop("extracted_role", None)
            st.session_state.pop("extracted_company", None)
            
        st.session_state["latest_jd_text"] = final_jd_text
        lang = st.session_state.get("language", "English")
        temp = st.session_state.get("temperature", 0.7)
        template_type = st.session_state.get("template", "Modern")
        
        if generate_cv:
            with st.spinner(f"Tailoring CV using {model}..."):
                # Format prompt
                cv_prompt = prompts.TAILOR_CV_PROMPT.format(
                    cv_text=cv_text,
                    jd_text=final_jd_text,
                    role=job_role,
                    company=company,
                    language=lang,
                    modify_title=str(modify_title),
                    modify_summary=str(modify_summary),
                    modify_skills=str(modify_skills),
                    modify_exp=str(modify_exp)
                )
                
                # Call LLM
                response_text, in_tok, out_tok = llm_engine.generate_text(provider, model, cv_prompt, api_key, temperature=temp)
                total_in_tokens += in_tok
                total_out_tokens += out_tok
                
                # Check for errors
                if response_text.startswith("Error"):
                    st.error(response_text)
                else:
                    st.success("CV Data Generated! Compiling LaTeX...")
                    try:
                        clean_json = clean_json_response(response_text)
                        cv_data = json.loads(clean_json)
                        
                        # Generate LaTeX
                        page_length = st.session_state.get("page_length", "1-Page")
                        latex_code = latex_generator.generate_latex_cv(cv_data, template_type, page_length)
                        st.session_state["latest_cv_tex"] = latex_code
                        
                        # Extract role and company (prioritize session_state from reality check, then cv_data)
                        extracted_role = st.session_state.get("extracted_role") or cv_data.get("target_role_extracted", "Unknown_Role")
                        extracted_company = st.session_state.get("extracted_company") or cv_data.get("target_company_extracted", "Unknown_Company")
                        st.session_state["extracted_role"] = extracted_role
                        st.session_state["extracted_company"] = extracted_company
                        
                        # Compile
                        pdf_path, error_msg = latex_compiler.compile_latex(latex_code, output_filename="tailored_cv")
                        if pdf_path:
                            st.session_state["latest_cv_pdf"] = pdf_path
                            saved_pdf = save_to_downloads(pdf_path, "Resume.pdf", extracted_role, extracted_company)
                            st.success(f"PDF compiled and saved to: {saved_pdf}")
                        else:
                            st.error(error_msg)
                            
                    except json.JSONDecodeError as e:
                        st.error("Failed to parse LLM response into JSON. The LLM might not have returned proper JSON format.")
                        st.code(response_text)
                        
        if generate_cl:
            with st.spinner(f"Generating Cover Letter using {model}..."):
                cl_prompt = prompts.COVER_LETTER_PROMPT.format(
                    cv_text=cv_text,
                    jd_text=final_jd_text,
                    role=job_role,
                    company=company,
                    language=lang
                )
                
                response_text, in_tok, out_tok = llm_engine.generate_text(provider, model, cl_prompt, api_key, temperature=temp)
                total_in_tokens += in_tok
                total_out_tokens += out_tok
                
                if response_text.startswith("Error"):
                    st.error(response_text)
                else:
                    st.success("Cover Letter Generated! Compiling LaTeX...")
                    
                    # Extract JSON payload
                    clean_json = clean_json_response(response_text)
                    try:
                        cl_data = json.loads(clean_json)
                    except json.JSONDecodeError:
                        cl_data = {"name": "Your Name", "contact": [], "body": response_text}
                        
                    latex_code = latex_generator.generate_latex_cl(cl_data)
                    st.session_state["latest_cl_tex"] = latex_code
                    st.session_state["latest_cl_text"] = cl_data.get("body", response_text)
                    
                    extracted_role = st.session_state.get("extracted_role") or cl_data.get("target_role_extracted", "Unknown_Role")
                    extracted_company = st.session_state.get("extracted_company") or cl_data.get("target_company_extracted", "Unknown_Company")
                    st.session_state["extracted_role"] = extracted_role
                    st.session_state["extracted_company"] = extracted_company
                    
                    pdf_path, error_msg = latex_compiler.compile_latex(latex_code, output_filename="tailored_cl")
                    if pdf_path:
                        st.session_state["latest_cl_pdf"] = pdf_path
                        saved_pdf = save_to_downloads(pdf_path, "cover-letter.pdf", extracted_role, extracted_company)
                        st.success(f"Cover Letter PDF compiled and saved to: {saved_pdf}")
                    else:
                        st.error(error_msg)
        
        # Display token usage
        if total_in_tokens > 0 or total_out_tokens > 0:
            st.info(f"🪙 **Token Usage:** {total_in_tokens:,} Input Tokens | {total_out_tokens:,} Output Tokens")
