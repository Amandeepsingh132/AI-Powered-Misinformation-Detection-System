# AI-Powered-Misinformation-Detection-System
Built an AI-driven fact-checking system using NLP and deep learning to verify claims against trusted sources. Integrated SBERT for semantic similarity, BART for AI summarization, and Google Fact Check AP for real-time verification. Developed an interactive Streamlit web app with Newspaper3k for article extraction.


✨ Features

✅ Fact-Checking API – Uses Google Fact Check API to verify claims

✅ Semantic Search – Implements SBERT for similarity matching

✅ AI Summarization – Uses BART to summarize fact-checked articles

✅ Web App – Built with Streamlit for easy user interaction

✅ News Scraping – Extracts full articles using Newspaper3k

✅ MLOps Ready – MLflow integration for model tracking (future enhancement)




🛠️ Tech Stack

- Python 🐍

- NLP (SBERT, Transformers)

- Google Fact Check API

- Streamlit (for UI)

- Newspaper3k (for article extraction)

- MLflow (for MLOps)

Run the app:
- streamlit run app.py


🎯 Usage

- Enter a claim (e.g., "Is 5G technology harmful to human health?").
- Input: 

 ![2](https://github.com/user-attachments/assets/139c4363-4310-4114-8ea9-c074b84245cb)

- output:
![1](https://github.com/user-attachments/assets/146bf9a3-c378-4841-b942-1ebf5187f6d2)


- The system searches for fact-checks, analyzes the claim, and provides a verdict.

- If an article is found, the AI summarizes it for quick reading.



📌 Future Enhancements

🔹 Claim Matching – Improve fact-checking with BERT-based claim verification.

🔹 Bias & Sentiment Analysis – Detect news source bias.

🔹 MLOps Pipeline – Automate model retraining & versioning with MLflow.
