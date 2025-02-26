import streamlit as st
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sentence_transformers import SentenceTransformer, util
from newspaper import Article
from transformers import pipeline

# Set page configuration
st.set_page_config(page_title="AI Fact Checker", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .result-container {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Hard-coded API key (replace with your actual API key)
API_KEY = ""  # Replace this with your actual API key

# Download NLTK resources only if not already downloaded
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    return True

# Load ML models
@st.cache_resource
def load_models():
    sbert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return sbert_model, summarizer

# Call the functions
download_nltk_resources()
sbert_model, summarizer = load_models()

# Title
st.title("AI Fact Checker")
st.write("Verify claims with AI-powered fact-checking")

def extract_keywords(query):
    """Extract keywords by removing stopwords & punctuation."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(query.lower())
    keywords = [word for word in words if word not in stop_words and word not in string.punctuation]
    return " ".join(keywords)

def search_fact_check_api(query, api_key):
    """Search Google Fact Check API for claim reviews."""
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {"query": query, "key": api_key, "languageCode": "en"}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get("claims", [])
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return []

def scrape_and_summarize(url):
    """Scrape the article from the fact-checking website and summarize it."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        article_text = article.text

        # AI Summarization (truncate to 1024 tokens max)
        summary = summarizer(article_text[:1024], max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
        return summary
    except Exception as e:
        return f"Error scraping article: {str(e)}"

def fact_check(query, api_key):
    """Enhanced fact check with semantic search and summarization."""
    with st.spinner("🔍 Searching for fact checks..."):
        # Search API
        fact_check_results = search_fact_check_api(query, api_key)
        
        # If no results, try with keywords
        if not fact_check_results:
            refined_query = extract_keywords(query)
            fact_check_results = search_fact_check_api(refined_query, api_key)
        
        if not fact_check_results:
            return "No fact-check results found."
        
        # Semantic search with SBERT
        query_embedding = sbert_model.encode(query, convert_to_tensor=True)
        
        best_match = None
        highest_score = 0.0

        for claim in fact_check_results:
            claim_text = claim.get("text", "No claim text available.")
            claim_embedding = sbert_model.encode(claim_text, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(query_embedding, claim_embedding).item()
            
            if similarity_score > highest_score:
                highest_score = similarity_score
                review = claim.get("claimReview", [{}])[0]
                url = review.get("url", "No URL available.")
                summary = scrape_and_summarize(url) if url != "No URL available." else "No article available."
                
                best_match = {
                    "claim_text": claim_text,
                    "rating": review.get("textualRating", "No rating available."),
                    "explanation": review.get("reviewBody") or review.get("title", "No explanation available."),
                    "source": review.get("publisher", {}).get("name", "Unknown source"),
                    "url": url,
                    "summary": summary,
                    "similarity": similarity_score
                }
        
        if best_match:
            return (
                f"🔎 **Claim:** {best_match['claim_text']}\n\n"
                f"✅ **Rating:** {best_match['rating']}\n\n"
                f"📝 **Explanation:** {best_match['explanation']}\n\n"
                f"📢 **Source:** {best_match['source']}\n\n"
                f"🔗 **More Info:** {best_match['url']}\n\n"
                f"📊 **Similarity Score:** {best_match['similarity']:.2f}\n\n"
                f"📰 **AI-Summarized Fact-Check:** {best_match['summary']}"
            )
        else:
            return "No highly similar fact-checks found."

# Main query input
query = st.text_input("Enter a claim to fact-check", placeholder="e.g., Did Ronaldo win the FIFA World Cup?")

# Process the query when button is clicked
if st.button("Fact Check", type="primary") and query:
    result = fact_check(query, API_KEY)
    
    # Display results
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# Instructions if no query yet
if not query:
    st.info("Enter a claim in the search box above to check its factual accuracy")
    
    # Example queries
    st.markdown("### Example claims to check:")
    st.markdown("- Did Ronaldo win the FIFA World Cup?")
    st.markdown("- Is climate change caused by humans?")
    st.markdown("- Was the COVID-19 vaccine rushed?")
    st.markdown("- Did NASA find evidence of aliens?")