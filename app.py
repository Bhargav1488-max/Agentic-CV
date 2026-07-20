import streamlit as st
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
        "2. Manual Build", 
        "3. 📊 ATS Match", 
        "4. 📄 CV Preview", 
        "5. ✉️ Cover Letter", 
        "6. 📁 History"
    ])
    
    with tabs[0]:
        tab_tailor.render()
        
    with tabs[1]:
        tab_manual.render()
        
    with tabs[2]:
        tab_ats.render()
        
    with tabs[3]:
        tab_cv_preview.render()
        
    with tabs[4]:
        tab_cover_letter.render()
        
    with tabs[5]:
        tab_history.render()

if __name__ == "__main__":
    main()
