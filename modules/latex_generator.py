import os
import json
import ast
from modules import utils

def generate_latex_cv(cv_data, template_type, page_length="1-Page"):
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
    
    parsed_exp = []
    for exp in exp_data:
        if isinstance(exp, str):
            try:
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
            pt = utils.escape_latex(str(point))
            experience_latex += f"    \\item {pt}\n"
        experience_latex += "\\end{itemize}\n\n"

    # Dynamic Personal Details
    name = utils.escape_latex(cv_data.get("name", "Your Name"))
    title = utils.escape_latex(cv_data.get("title", "Professional Title"))
    
    contact_list = cv_data.get("contact", [])
    contact_str = " $\\vert$ ".join([utils.escape_latex(str(c)) for c in contact_list])
    
    # Process Education
    education_latex = ""
    edu_data = cv_data.get("education", [])
    for edu in edu_data:
        degree = utils.escape_latex(edu.get("degree", ""))
        institution = utils.escape_latex(edu.get("institution", ""))
        dates = utils.escape_latex(edu.get("dates", ""))
        location = utils.escape_latex(edu.get("location", ""))
        education_latex += f"\\role{{{degree}}}{{{institution}}}{{{dates}}}{{{location}}}\n\\vspace{{2pt}}\n"

    # Process Certifications
    certs_list = cv_data.get("certifications", [])
    if isinstance(certs_list, str):
        try:
            certs_list = ast.literal_eval(certs_list)
        except:
            certs_list = [certs_list]
    certs_latex = "\\begin{itemize}[label={}]\n"
    for cert in certs_list:
        certs_latex += f"    \\item {utils.escape_latex(str(cert))}\n"
    certs_latex += "\\end{itemize}\n"

    # Process Languages
    langs_list = cv_data.get("languages", [])
    if isinstance(langs_list, str):
        try:
            langs_list = ast.literal_eval(langs_list)
        except:
            langs_list = [langs_list]
    langs_str = " $\\vert$ ".join([utils.escape_latex(str(l)) for l in langs_list])

    # Dynamic Page Formatting
    if page_length == "1-Page":
        margin = "1.0cm"
        itemsep = "0pt"
        topsep = "1pt"
    else:
        margin = "2.0cm"
        itemsep = "3pt"
        topsep = "4pt"

    # Injecting into the user's specific LaTeX Template
    tex = r"""\documentclass[a4paper,10pt]{article}

% ---------- PACKAGES ----------
\usepackage[margin=""" + margin + r"""]{geometry}
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

\setlist[itemize]{leftmargin=1.2em, itemsep=""" + itemsep + r""", topsep=""" + topsep + r"""}

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
    {\LARGE \textbf{""" + name + r"""}}\\[3pt]
    {\large """ + title + r"""}\\[5pt]
    \small
    """ + contact_str + r"""
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
""" + education_latex + r"""

% ========================= CERTIFICATIONS =========================
\section{Certifications}
""" + certs_latex + r"""

% ========================= LANGUAGES =========================
\section{Languages}
""" + langs_str + r"""

\end{document}
"""
    return tex

def generate_latex_cl(cl_data):
    if isinstance(cl_data, str):
        cl_data = {"name": "Your Name", "contact": [], "body": cl_data}
        
    cl_text = cl_data.get("body", "")
    # Handle basic line breaks
    cl_text = cl_text.replace('\n', '\n\n')
    safe_text = utils.escape_latex(cl_text)
    
    name = utils.escape_latex(cl_data.get("name", "Your Name"))
    contact_list = cl_data.get("contact", [])
    contact_str = " $\\cdot$ ".join([utils.escape_latex(str(c)) for c in contact_list])
    
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
    {\LARGE \textbf{""" + name + r"""}}\\[5pt]
    """ + contact_str + r"""
\end{center}

\vspace{1em}

""" + safe_text + r"""

\end{document}
"""
    return tex
