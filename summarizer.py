import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
from dotenv import load_dotenv
import openai
from transformers import pipeline


# load_dotenv()  # Load from .env

# # client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def summarize_article(text):
#     prompt = f"Summarize the following article in 5 bullet points:\n\n{text}"
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.5,
#         max_tokens=400,
#     )
#     return response.choices[0].message.content.strip()

# def classify_news_source(text):
#     prompt = "Classify the tone and credibility of this article as one of the following: 'Credible', 'Biased', 'Potentially Fake'.\n\n" + text
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#     )
#     return response.choices[0].message.content.strip()


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_article(text):
    # Trim if too long
    if len(text) > 1024:
        text = text[:1024]
    result = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return "\n".join([s['summary_text'] for s in result])

def classify_news_source(text):
    if "killed" in text or "fake" in text:
        return "Potentially Fake"
    elif "according to" in text or "report" in text:
        return "Credible"
    else:
        return "Biased"