import streamlit as st
import base64
import os

def display_pdf(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("PDF file not found.")

def render():
    st.header("✉️ Cover Letter Preview")
    
    tex_content = st.session_state.get("latest_cl_tex", "")
    pdf_path = st.session_state.get("latest_cl_pdf", None)
    cl_text = st.session_state.get("latest_cl_text", "")
    
    if not tex_content and not pdf_path:
        st.info("Your generated Cover Letter will appear here. Go to 'Tailor Mode' to generate one.")
        return
        
    col1, col2 = st.columns(2)
    with col1:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", data=f, file_name="AI-Powered_Job_Application_Engine_saved_Cover_Letter.pdf", mime="application/pdf")
        else:
            st.warning("⚠️ PDF compilation failed or not run. You can still download the LaTeX source.")
            
    with col2:
        if tex_content:
            st.download_button("⬇️ Download .tex", data=tex_content, file_name="AI-Powered_Job_Application_Engine_saved_Cover_Letter.tex", mime="text/plain")
        
    st.divider()
    
    # Display the raw text as well
    with st.expander("View/Edit Raw Text", expanded=False):
        st.text_area("Cover Letter Text", height=300, value=cl_text)
        
    if pdf_path and os.path.exists(pdf_path):
        display_pdf(pdf_path)
    else:
        st.info("Upload the downloaded .tex file to an online editor like [Overleaf](https://www.overleaf.com) to generate your PDF.")
