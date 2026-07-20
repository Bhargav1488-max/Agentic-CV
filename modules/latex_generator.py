import os
import json
import ast
from modules import utils

def generate_latex_cv(cv_data, template_type):
    summary = utils.escape_latex(cv_data.get("summary", ""))
    
    # Process Skills
    skills_list = cv_data.get("skills", [])
    if isinstance(skills_list, str):
        try:
            skills_list = ast.literal_eval(skills_list)
        except:
            skills_list = [skills_list]
    skills_str = ", ".join([utils.escape_latex(str(s)) for s in skills_list])
    
    # Process Experience
    experience_latex = ""
    exp_data = cv_data.get("experience", [])
    
    # Sometimes LLM wraps dicts in strings inside the list, try to parse
    parsed_exp = []
    for exp in exp_data:
        if isinstance(exp, str):
            try:
                # Replace single quotes with double quotes for valid json, or use literal_eval
                exp = ast.literal_eval(exp)
            except:
                pass
        if isinstance(exp, dict):
            parsed_exp.append(exp)
            
    for job in parsed_exp:
        title = utils.escape_latex(job.get("title", ""))
        company = utils.escape_latex(job.get("company", ""))
        dates = utils.escape_latex(job.get("dates", ""))
        location = utils.escape_latex(job.get("location", ""))
        
        experience_latex += f"\\role{{{title}}}{{{company}}}{{{dates}}}{{{location}}}\n\\begin{{itemize}}\n"
        
        highlights = job.get("highlights", [])
        if isinstance(highlights, str):
            try:
                highlights = ast.literal_eval(highlights)
            except:
                highlights = [highlights]
                
        for point in highlights:
            # We don't want to double escape if LLM used \textbf{}, so we are careful
            # but utils.escape_latex should handle basic chars like % & $
            pt = utils.escape_latex(str(point))
            experience_latex += f"    \\item {pt}\n"
        experience_latex += "\\end{itemize}\n\n"

    title = utils.escape_latex(cv_data.get("title", "AI Engineer | Multi-Agent Systems & RAG"))

    # Injecting into the user's specific LaTeX Template
    tex = r"""\documentclass[a4paper,10pt]{article}

% ---------- PACKAGES ----------
\usepackage[margin=1.5cm]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{xcolor}

% ---------- COLORS ----------
\definecolor{primary}{RGB}{20,20,20}

% ---------- SECTION FORMATTING ----------
\titleformat{\section}
  {\large\bfseries\color{primary}}
  {}{0em}{}[\vspace{-0.6em}\rule{\textwidth}{0.6pt}\vspace{-0.2em}]
\titlespacing{\section}{0pt}{8pt}{4pt}

\setlist[itemize]{leftmargin=1.2em, itemsep=1pt, topsep=2pt}

\pagestyle{empty}
\setlength{\parindent}{0pt}

% ---------- CUSTOM COMMANDS ----------
\newcommand{\role}[4]{%
  \textbf{#1} \hfill \textbf{#3}\\
  \textit{#2} \hfill \textit{#4}\\[2pt]
}

\begin{document}

% ========================= HEADER =========================
\begin{center}
    {\LARGE \textbf{Bhargav Chollangi}}\\[3pt]
    {\large """ + title + r"""}\\[5pt]
    \small
    Paris, France $\vert$ \href{mailto:chollangibhargav5@gmail.com}{chollangibhargav5@gmail.com} $\vert$ +33 7 45 56 88 80\\
    \href{https://linkedin.com/in/bhargav-chollangi-47871b271}{linkedin.com/in/bhargav-chollangi} $\vert$
    \href{https://github.com/Bhargav1488-max}{github.com/Bhargav1488-max}\\[2pt]
    \textbf{Work Authorization:} France Talent Passport (Passeport Talent) work visa -- No sponsorship required
\end{center}

% ========================= SUMMARY =========================
\section{Professional Summary}
""" + summary + r"""

% ========================= SKILLS =========================
\section{Technical Skills}
\begin{itemize}[label={}]
    \item """ + skills_str + r"""
\end{itemize}

% ========================= EXPERIENCE =========================
\section{Professional Experience}

""" + experience_latex + r"""
% ========================= EDUCATION =========================
\section{Education}
\role{MSc in International Marketing and Data Analytics }{Paris School Of Business, France}{Jan 2023 -- Aug 2023}{Paris, France}
\vspace{2pt}
\role{Bachelor of Engineering in Computer Science}{}{2017 -- 2021} {India}

% ========================= CERTIFICATIONS =========================
\section{Certifications}
\begin{itemize}[label={}]
    \item Microsoft Certified: Azure Data Engineer Associate (Databricks)
    \item Microsoft Certified: Azure Network Engineer Associate (AZ-700)
    \item DeepLearning.AI: AI For Everyone (Coursera) $\vert$ Hugging Face: Transformers Course $\vert$ edX: Intro to DevOps
\end{itemize}

% ========================= LANGUAGES =========================
\section{Languages}
English (Bilingual) $\vert$ Telugu (Native) $\vert$ Hindi (Native) $\vert$ French (B1)

\end{document}
"""
    return tex

def generate_latex_cl(cl_text):
    # Handle basic line breaks
    cl_text = cl_text.replace('\n', '\n\n')
    safe_text = utils.escape_latex(cl_text)
    
    tex = r"""\documentclass[a4paper,11pt]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{1em}

\begin{document}

\begin{center}
    {\LARGE \textbf{Bhargav Chollangi}}\\[5pt]
    Paris, France $\cdot$ +33 7 45 56 88 80 $\cdot$ chollangibhargav5@gmail.com
\end{center}

\vspace{1em}

""" + safe_text + r"""

\end{document}
"""
    return tex
