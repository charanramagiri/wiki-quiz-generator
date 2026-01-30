import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    if "wikipedia.org/wiki/" not in url:
        raise ValueError("Invalid Wikipedia URL")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise Exception("Failed to fetch page")

    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    title = soup.find("h1").get_text()

    # Content container
    content = soup.find("div", {"id": "mw-content-text"})

    paragraphs = content.find_all("p")
    headers = content.find_all(["h2", "h3"])

    # Clean paragraphs
    text_content = []
    for p in paragraphs:
        if p.get_text(strip=True):
            text_content.append(p.get_text())

    full_text = "\n".join(text_content)

    # Sections
    sections = []
    for h in headers:
        span = h.find("span", class_="mw-headline")
        if span:
            sections.append(span.get_text())

    summary = text_content[0] if text_content else ""

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "full_text": full_text
    }
