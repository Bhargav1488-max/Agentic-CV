import re

def escape_latex(text):
    if not text:
        return ""
    # Map of special LaTeX characters to their escaped versions
    latex_special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    # Regex to match any of the special characters
    regex = re.compile('|'.join(re.escape(str(key)) for key in latex_special_chars.keys()))
    return regex.sub(lambda match: latex_special_chars[match.group(0)], text)

def sanitize_filename(filename):
    return re.sub(r'(?u)[^-\w.]', '', filename.strip().replace(' ', '_'))
