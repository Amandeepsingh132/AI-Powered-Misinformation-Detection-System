from fastapi import FastAPI
import requests
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from newspaper import Article
import nltk

# Download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

app = FastAPI()

# Load models (only once at startup)
sbert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def search_fact_check_api(query, api_key):
    """Call the Google Fact Check API."""
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {"query": query, "key": api_key, "languageCode": "en"}
    response = requests.get(url, params=params)
    return response.json().get("claims", [])

@app.get("/fact-check")
async def fact_check(query: str, api_key: str):
    """Fact-check endpoint."""
    fact_check_results = search_fact_check_api(query, api_key)
    if not fact_check_results:
        return {"message": "No fact-check results found."}

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
            summary = "No article available."
            if url != "No URL available.":
                try:
                    article = Article(url)
                    article.download()
                    article.parse()
                    article_text = article.text
                    summary = summarizer(article_text[:1024], max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
                except:
                    summary = "Error scraping article."

            best_match = {
                "claim_text": claim_text,
                "rating": review.get("textualRating", "No rating available."),
                "explanation": review.get("reviewBody") or review.get("title", "No explanation available."),
                "source": review.get("publisher", {}).get("name", "Unknown source"),
                "url": url,
                "summary": summary,
                "similarity": similarity_score
            }

    return best_match or {"message": "No highly similar fact-checks found."}
