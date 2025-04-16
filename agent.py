from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("❌ GOOGLE_API_KEY is missing from your .env file or failed to load.")

# Initialize Gemini-Pro chat model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=google_api_key,
    temperature=0.7
)

def summarize_article(article_text):
    try:
        logging.debug(f"Starting summarization for the article: {article_text[:100]}...")  # Log first 100 chars for debug
        response = llm.invoke(article_text)
        
        if not response or not hasattr(response, 'content'):
            raise ValueError("Received invalid response from the Gemini model.")
        
        logging.debug(f"Summarization response: {response.content[:100]}...")  # Log first 100 chars of the response
        return response.content
    except Exception as e:
        logging.exception(f"❌ Error during summarization: {e}")
        return "Could not summarize due to an internal error."
