import streamlit as st
import pandas as pd

def render():
    st.header("📁 Application History")
    
    # Placeholder Data
    data = {
        "Date": ["2026-07-20", "2026-07-19"],
        "Company": ["TechCorp", "InnovateAI"],
        "Role": ["Senior Software Engineer", "AI Developer"],
        "Score": ["85%", "92%"],
        "Status": ["Applied", "Draft"]
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df, use_container_width=True)
    
    st.button("Clear History")
