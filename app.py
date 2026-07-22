import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from ui import sidebar
from ui import tab_tailor, tab_manual, tab_ats, tab_cv_preview, tab_cover_letter, tab_history

st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide"
)

def main():
    st.title("💼 AI Job Application Assistant")
    
    # Render Sidebar
    sidebar.render_sidebar()
    
    # Main Tabs
    tabs = st.tabs([
        "1. Tailor Mode", 
        "2. 📄 CV Preview", 
        "3. ✉️ Cover Letter"
    ])
    
    with tabs[0]:
        tab_tailor.render()
        
    with tabs[1]:
        tab_cv_preview.render()
        
    with tabs[2]:
        tab_cover_letter.render()
        
if __name__ == "__main__":
    main()
