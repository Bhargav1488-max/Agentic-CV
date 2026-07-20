import os
import shutil
import subprocess
import platform


def _is_running_in_docker():
    """Check if the current process is running inside a Docker container."""
    # Check for .dockerenv file (most common)
    if os.path.exists("/.dockerenv"):
        return True
    # Check cgroup for docker/container references
    try:
        with open("/proc/1/cgroup", "r") as f:
            return "docker" in f.read() or "containerd" in f.read()
    except (FileNotFoundError, PermissionError):
        return False


def _compile_local(tex_path, output_dir, output_filename):
    """Compile LaTeX using the locally installed pdflatex."""
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"{output_filename}.tex"],
            cwd=output_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pdf_path = os.path.join(output_dir, f"{output_filename}.pdf")
        return pdf_path, None
    except subprocess.CalledProcessError as e:
        error_output = e.stdout.decode("utf-8", errors="ignore") if e.stdout else str(e)
        return None, f"LaTeX compilation error:\n```text\n{error_output[-1000:]}\n```"
    except Exception as e:
        return None, f"LaTeX compilation failed: {e}"


def _compile_via_docker(tex_path, output_dir, output_filename):
    """Compile LaTeX by running pdflatex inside a Docker container.

    Uses the project's own Docker image (agentic-cv-app) which already has
    TeX Live installed.  Falls back to the public `texlive/texlive:latest`
    image if the project image isn't available.
    """
    # Resolve to absolute path so Docker volume mount works on Windows too
    abs_output_dir = os.path.abspath(output_dir)

    # On Windows, Docker Desktop needs forward-slash paths for -v mounts
    if platform.system() == "Windows":
        abs_output_dir = abs_output_dir.replace("\\", "/")

    # Try the project image first, then a public TeX Live image
    images = ["agentic-cv-app:latest", "texlive/texlive:latest"]

    for image in images:
        try:
            result = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-v", f"{abs_output_dir}:/work",
                    "-w", "/work",
                    image,
                    "pdflatex", "-interaction=nonstopmode", f"{output_filename}.tex",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            pdf_path = os.path.join(output_dir, f"{output_filename}.pdf")
            if os.path.exists(pdf_path):
                return pdf_path, None
            return None, "LaTeX compiled but PDF was not generated."
        except subprocess.CalledProcessError as e:
            error_output = e.stdout.decode("utf-8", errors="ignore") if e.stdout else str(e)
            return None, f"LaTeX compilation error (Docker):\n```text\n{error_output[-1000:]}\n```"
        except FileNotFoundError:
            # Docker CLI not found – can't use this strategy
            return None, (
                "LaTeX compiler ('pdflatex') not found locally and Docker is not "
                "available.\n\n"
                "**To fix this, do one of the following:**\n"
                "- Install [MiKTeX](https://miktex.org/download) or "
                "[TeX Live](https://tug.org/texlive/windows.html) and add to PATH\n"
                "- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) "
                "and run `docker compose build`"
            )
        except Exception:
            # Try the next image
            continue

    return None, "Could not compile LaTeX: no working Docker image found."


def compile_latex(tex_content, output_filename="output"):
    """Compile LaTeX content to PDF.

    Strategy:
    1. If pdflatex is available locally (or we are inside Docker), use it directly.
    2. Otherwise, delegate to a Docker container that has TeX Live installed.
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    tex_path = os.path.join(output_dir, f"{output_filename}.tex")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    # Path 1: pdflatex is installed locally (always true inside Docker)
    if shutil.which("pdflatex"):
        return _compile_local(tex_path, output_dir, output_filename)

    # Path 2: no local pdflatex – try Docker
    return _compile_via_docker(tex_path, output_dir, output_filename)
