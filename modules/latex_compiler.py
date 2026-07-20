import os
import subprocess

def compile_latex(tex_content, output_filename="output"):
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    tex_path = os.path.join(output_dir, f"{output_filename}.tex")
    pdf_path = os.path.join(output_dir, f"{output_filename}.pdf")
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)
        
    try:
        # Run pdflatex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"{output_filename}.tex"],
            cwd=output_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return pdf_path
    except Exception as e:
        print(f"LaTeX compilation failed: {e}")
        return None
