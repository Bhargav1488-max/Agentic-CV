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
    
    if "latest_cl_pdf" not in st.session_state or not st.session_state["latest_cl_pdf"]:
        st.info("Your generated Cover Letter will appear here. Go to 'Tailor Mode' to generate one.")
        return
        
    pdf_path = st.session_state["latest_cl_pdf"]
    tex_content = st.session_state.get("latest_cl_tex", "")
    cl_text = st.session_state.get("latest_cl_text", "")
    
    col1, col2 = st.columns(2)
    with col1:
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download CL PDF", data=f, file_name="Cover_Letter.pdf", mime="application/pdf")
    with col2:
        st.download_button("⬇️ Download CL .tex", data=tex_content, file_name="Cover_Letter.tex", mime="text/plain")
        
    st.divider()
    
    # Display the raw text as well
    with st.expander("View/Edit Raw Text", expanded=False):
        st.text_area("Cover Letter Text", height=300, value=cl_text)
        
    display_pdf(pdf_path)
