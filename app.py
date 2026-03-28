import streamlit as st
from news_utils import extract_article_text
from summarizer import summarize_article, classify_news_source
from vector_store import add_to_db, get_similar_articles

st.set_page_config(page_title="News Insight", layout="wide")

st.title("📰 News Summarizer + Credibility Checker")

# Always show something on screen
st.write("👉 Enter a news article URL below and click Analyze")

url = st.text_input("Enter a news article URL:")

if st.button("Analyze Article"):
    if not url:
        st.warning("⚠️ Please enter a URL")
    else:
        try:
            with st.spinner("Extracting article..."):
                title, content = extract_article_text(url)

            if not content:
                st.error("❌ Could not extract article.")
            else:
                st.success(f"✅ Extracted: {title}")

                with st.spinner("Summarizing..."):
                    summary = summarize_article(content)

                with st.spinner("Analyzing credibility..."):
                    credibility = classify_news_source(content)

                st.subheader("📝 Summary")
                st.info(summary)

                st.subheader("🔍 Credibility")
                st.success(credibility)

                # Save to DB
                add_to_db(title, content)

                st.subheader("📚 Similar Articles")
                related = get_similar_articles(content)

                if related:
                    for doc in related:
                        st.markdown(
                            f"""
                            <div style='background-color:#f0f8ff;padding:10px;border-radius:10px;margin-bottom:10px;'>
                            <strong>{doc.metadata.get('title','No Title')}</strong><br>
                            {doc.page_content[:300]}...
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No similar articles found.")

        except Exception as e:
            st.error(f"🚨 Error: {e}")