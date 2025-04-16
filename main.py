from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent import summarize_article
from memory_tool import save_memory_to_pinecone, retrieve_memory_from_pinecone
from newsapi import NewsApiClient
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# Load NewsAPI
news_api_key = os.getenv("NEWS_API_KEY")
if not news_api_key:
    raise RuntimeError("❌ NEWS_API_KEY is missing.")
news_api = NewsApiClient(api_key=news_api_key)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI News Summarizer API!"}

@app.post("/ask")
def ask_news_summary(request: QueryRequest):
    logging.debug("🔥 /ask endpoint hit")
    try:
        user_query = request.query
        logging.info(f"🔍 User Query: {user_query}")

        # Retrieve memory
        previous_interest = retrieve_memory_from_pinecone(user_query)
        logging.info(f"🧠 Memory: {previous_interest}")

        query_to_use = previous_interest if previous_interest else user_query
        response = news_api.get_everything(q=query_to_use, language='en', sort_by='relevancy')

        if response.get("status") != "ok":
            raise HTTPException(status_code=500, detail=f"NewsAPI error: {response.get('message')}")

        articles = response.get('articles', [])
        if not articles:
            raise HTTPException(status_code=404, detail="No news found.")

        summaries = []
        for article in articles[:3]:
            content = article.get('content') or article.get('description') or article.get('title')
            if content:
                summary = summarize_article(content)
                summaries.append({"title": article['title'], "summary": summary})

        # Save memory
        save_memory_to_pinecone(user_query)
        return {"results": summaries}

    except Exception as e:
        logging.exception("❌ Error during news summary process")
        return {"error": f"Something went wrong: {e}. Check logs."}
