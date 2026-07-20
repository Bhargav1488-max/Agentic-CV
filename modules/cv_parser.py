from pypdf import PdfReader
import docx
import io

def parse_cv(uploaded_file):
    if not uploaded_file:
        return ""
        
    text = ""
    filename = uploaded_file.name.lower()
    
    try:
        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                    
        elif filename.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
                
    except Exception as e:
        print(f"Error parsing CV: {e}")
        
    return text
