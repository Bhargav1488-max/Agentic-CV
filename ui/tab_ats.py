import streamlit as st
import plotly.graph_objects as go
import json
from modules.llm_engine import generate_text

def analyze_ats():
    provider = st.session_state.get("selected_provider")
    model = st.session_state.get("selected_model")
    api_key = st.session_state.get("api_key")
    
    cv_text = st.session_state.get("latest_cv_tex", "")
    jd_text = st.session_state.get("latest_jd_text", "")
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) algorithm.
    Analyze the following Resume against the Job Description.
    Provide a JSON output strictly in this format without any markdown code blocks or extra text:
    {{
        "score": <integer from 0 to 100>,
        "matched_keywords": ["keyword1", "keyword2"],
        "missing_keywords": ["keyword3"],
        "recommendations": ["rec1", "rec2"]
    }}
    
    Job Description:
    {jd_text}
    
    Resume (LaTeX format):
    {cv_text}
    """
    
    try:
        response = generate_text(provider, model, prompt, api_key, temperature=0.1)
        
        # Clean markdown code blocks if the LLM adds them
        text = response.strip()
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        text = text.strip()
        
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx+1]
            data = json.loads(json_str)
            st.session_state["ats_data"] = data
            return True
        else:
            st.error("Failed to parse ATS response into JSON.")
            return False
    except Exception as e:
        st.error(f"Error during ATS analysis: {str(e)}")
        return False

def render():
    st.header("📊 ATS Match Analysis")
    
    if "latest_cv_tex" not in st.session_state or not st.session_state["latest_cv_tex"]:
        st.warning("⚠️ Please generate a tailored CV first in the 'Tailor Mode' tab before analyzing.")
        return
        
    st.info("Click below to run a deep AI-powered semantic ATS match between your Tailored CV and the Job Description.")
        
    if st.button("🚀 Calculate Real ATS Score", type="primary"):
        with st.spinner(f"Running ATS algorithm using {st.session_state.get('selected_model')}..."):
            if analyze_ats():
                st.success("ATS Analysis Complete!")
            
    if "ats_data" in st.session_state:
        data = st.session_state["ats_data"]
        score = data.get("score", 0)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "ATS Match Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "green" if score >= 80 else "orange" if score >= 60 else "red"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Matched Keywords")
            for kw in data.get("matched_keywords", []):
                st.write(f"- {kw}")
                
        with col2:
            st.subheader("❌ Missing Keywords")
            for kw in data.get("missing_keywords", []):
                st.write(f"- {kw}")
                
        st.subheader("💡 Recommendations to Improve")
        for rec in data.get("recommendations", []):
            st.write(f"- {rec}")
