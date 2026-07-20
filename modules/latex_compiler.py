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
        return pdf_path, None
    except FileNotFoundError:
        return None, "LaTeX compiler ('pdflatex') not found. Please install [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/windows.html) and ensure it is in your system PATH, or use Docker."
    except subprocess.CalledProcessError as e:
        error_output = e.stdout.decode('utf-8', errors='ignore') if e.stdout else str(e)
        return None, f"LaTeX compilation error:\n```text\n{error_output[-1000:]}\n```"
    except Exception as e:
        return None, f"LaTeX compilation failed: {e}"
