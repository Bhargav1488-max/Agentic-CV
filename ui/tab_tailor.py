import streamlit as st
import json
import re
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
    
    st.subheader("3. Tailoring Options")
    col_a, col_b = st.columns(2)
    with col_a:
        job_role = st.text_input("Target Job Role")
        company = st.text_input("Target Company")
        
        generate_cv = st.checkbox("Generate Tailored CV", value=True)
        generate_cl = st.checkbox("Generate Cover Letter", value=True)
        
    with col_b:
        st.write("Sections to Tailor (uncheck to keep original):")
        modify_title = st.checkbox("CV Title", value=True)
        modify_summary = st.checkbox("Professional Summary", value=True)
        modify_skills = st.checkbox("Technical Skills", value=True)
        modify_exp = st.checkbox("Professional Experience", value=True)
    
    if st.button("🚀 Generate Applications", type="primary"):
        if not uploaded_file:
            st.error("Please upload a CV first.")
            return
            
        if not final_jd_text:
            st.error("Please provide a Job Description.")
            return
            
        st.session_state["latest_jd_text"] = final_jd_text
        
        # Verify provider and key are set
        provider = st.session_state.get("selected_provider")
        model = st.session_state.get("selected_model")
        api_key = st.session_state.get("api_key")
        lang = st.session_state.get("language", "English")
        temp = st.session_state.get("temperature", 0.7)
        template_type = st.session_state.get("template", "Modern")
        
        if not provider or not api_key:
            st.error("Please configure the LLM Provider and API Key in the sidebar.")
            return
            
        st.info("Parsing CV...")
        cv_text = cv_parser.parse_cv(uploaded_file)
        
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
                response_text = llm_engine.generate_text(provider, model, cv_prompt, api_key, temperature=temp)
                
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
                        
                        # Compile
                        pdf_path, error_msg = latex_compiler.compile_latex(latex_code, output_filename="tailored_cv")
                        if pdf_path:
                            st.session_state["latest_cv_pdf"] = pdf_path
                            st.success("PDF compiled successfully! Check the CV Preview tab.")
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
                
                response_text = llm_engine.generate_text(provider, model, cl_prompt, api_key, temperature=temp)
                
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
                    
                    pdf_path, error_msg = latex_compiler.compile_latex(latex_code, output_filename="tailored_cl")
                    if pdf_path:
                        st.session_state["latest_cl_pdf"] = pdf_path
                        st.success("Cover Letter PDF compiled successfully! Check the Cover Letter tab.")
                    else:
                        st.error(error_msg)
