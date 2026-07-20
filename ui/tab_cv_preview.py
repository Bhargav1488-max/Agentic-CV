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
    
    tex_content = st.session_state.get("latest_cv_tex", "")
    pdf_path = st.session_state.get("latest_cv_pdf", None)
    
    if not tex_content and not pdf_path:
        st.info("Your generated CV will appear here. Go to 'Tailor Mode' or 'Manual Build' to generate one.")
        return
        
    col1, col2 = st.columns(2)
    
    with col1:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", data=f, file_name="Tailored_CV.pdf", mime="application/pdf")
        else:
            st.warning("⚠️ PDF compilation failed or not run. You can still download the LaTeX source.")
            
    with col2:
        if tex_content:
            st.download_button("⬇️ Download .tex", data=tex_content, file_name="Tailored_CV.tex", mime="text/plain")
        
    st.divider()
    
    if pdf_path and os.path.exists(pdf_path):
        display_pdf(pdf_path)
    else:
        st.info("Upload the downloaded .tex file to an online editor like [Overleaf](https://www.overleaf.com) to generate your PDF.")
