import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def scrape_wikipedia(url: str):
    # Basic checks
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # Title
    title_tag = soup.find(id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else ""
    # Content extraction: main article body
    content_div = soup.find(id="mw-content-text")
    if not content_div:
        # fallback: take largest <p> content
        paragraphs = soup.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs[:10])
        return title, text
    # remove tables, sup, reference marks
    for tag in content_div(["table", "sup", "style", "script", "noscript"]):
        tag.decompose()
    # Collect text paragraphs
    paragraphs = content_div.find_all(["p", "h2", "h3"])
    text_parts = []
    sections = []
    for p in paragraphs:
        if p.name in ("h2", "h3"):
            heading = p.get_text(strip=True)
            sections.append(heading)
        else:
            t = p.get_text(" ", strip=True)
            # remove citation bracket numbers like [1]
            t = re.sub(r"\[\d+\]", "", t)
            if t:
                text_parts.append(t)
    cleaned = "\n\n".join(text_parts)
    return title, cleaned
