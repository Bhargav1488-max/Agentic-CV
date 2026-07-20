import streamlit as st
import base64
import os

def display_pdf(file_path):
    # Opening file from file path
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # Embedding PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("PDF file not found.")

def render():
    st.header("📄 CV Preview")
    
    if "latest_cv_pdf" not in st.session_state or not st.session_state["latest_cv_pdf"]:
        st.info("Your generated CV will appear here. Go to 'Tailor Mode' or 'Manual Build' to generate one.")
        return
        
    pdf_path = st.session_state["latest_cv_pdf"]
    tex_content = st.session_state.get("latest_cv_tex", "")
    
    col1, col2 = st.columns(2)
    with col1:
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF", data=f, file_name="Tailored_CV.pdf", mime="application/pdf")
    with col2:
        st.download_button("⬇️ Download .tex", data=tex_content, file_name="Tailored_CV.tex", mime="text/plain")
        
    st.divider()
    
    display_pdf(pdf_path)
