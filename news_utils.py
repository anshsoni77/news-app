import requests
from readability import Document
from bs4 import BeautifulSoup

def extract_article_text(url):
    response = requests.get(url)
    doc = Document(response.text)
    title = doc.title()
    summary_html = doc.summary()

    soup = BeautifulSoup(summary_html, 'html.parser')
    text = soup.get_text()

    return title, text
