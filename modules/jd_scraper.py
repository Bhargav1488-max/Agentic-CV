import requests
from bs4 import BeautifulSoup
import json

def scrape_jd(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Try to find JSON-LD
        jd_text = ""
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        for script in json_ld_scripts:
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get("@type") == "JobPosting":
                        jd_text += f"Title: {data.get('title', '')}\n"
                        jd_text += f"Description: {data.get('description', '')}\n"
                        return jd_text
                except Exception:
                    pass
                    
        # Fallback to body parsing
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
            
        jd_text = soup.get_text(separator="\n", strip=True)
        return jd_text
        
    except Exception as e:
        return f"Error scraping URL: {str(e)}"
