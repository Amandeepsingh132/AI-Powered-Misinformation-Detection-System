📰 AI-Powered Fact-Checking System
Built an AI-driven fact-checking system using NLP and deep learning to verify claims against trusted sources. Integrated SBERT for semantic similarity, BART for AI summarization, and Google Fact Check API for real-time verification. Developed an interactive Streamlit web app with Newspaper3k for article extraction. The backend is powered by FastAPI and the entire system is containerized using Docker and deployed on AWS EC2 for scalable performance.

✨ Features
✅ Fact-Checking API – Uses Google Fact Check API to verify claims
✅ Semantic Search – Implements SBERT for similarity matching
✅ AI Summarization – Uses BART to summarize fact-checked articles
✅ Web App – Built with Streamlit for easy user interaction
✅ FastAPI Backend – Efficient and scalable API management
✅ Dockerized Deployment – Portable and consistent environment setup
✅ EC2 Hosting – Hosted on AWS EC2 for global accessibility
✅ News Scraping – Extracts full articles using Newspaper3k
✅ MLOps Ready – MLflow integration for model tracking (future enhancement)

🛠️ Tech Stack
Python 🐍

NLP (SBERT, Transformers)

FastAPI (for backend)

Google Fact Check API

Streamlit (for UI)

Newspaper3k (for article extraction)

Docker (for containerization)

AWS EC2 (for deployment)

MLflow (for MLOps)

🚀 Deployment Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/username/repo.git
cd repo
Build Docker image:

bash
Copy
Edit
docker build -t fact-checker-app .
Run Docker container:

bash
Copy
Edit
docker run -d -p 8000:8000 fact-checker-app
Access the Streamlit UI:

arduino
Copy
Edit
http://localhost:8501
Deploy on AWS EC2:

Spin up an EC2 instance.

SSH into the instance and pull the Docker image from your repository.

Run the Docker container as above.

Configure security groups to open necessary ports (8000 for FastAPI and 8501 for Streamlit).

🎯 Usage
Input: Enter a claim (e.g., "Is 5G technology harmful to human health?").

 ![2](https://github.com/user-attachments/assets/139c4363-4310-4114-8ea9-c074b84245cb)


Output:
![1](https://github.com/user-attachments/assets/146bf9a3-c378-4841-b942-1ebf5187f6d2)

The system searches for fact-checks, analyzes the claim, and provides a verdict.

If an article is found, the AI summarizes it for quick reading.

📌 Future Enhancements
🔹 Claim Matching – Improve fact-checking with BERT-based claim verification.
🔹 Bias & Sentiment Analysis – Detect news source bias.
🔹 MLOps Pipeline – Automate model retraining & versioning with MLflow.
