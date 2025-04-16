import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_latest_news(query):
    try:
        # Construct the URL for the NewsAPI request
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
        logging.debug(f"Making request to NewsAPI with query: {query}")

        # Make the request to the API
        response = requests.get(url)
        
        # Check for a successful response
        if response.status_code != 200:
            raise ValueError(f"NewsAPI request failed with status code {response.status_code}")
        
        # Parse the response JSON
        data = response.json()

        # Check if 'articles' is in the response
        articles = data.get("articles", [])
        if not articles:
            logging.warning(f"No articles found for query: {query}")
        
        return [{"title": article["title"], "description": article["description"]} for article in articles]
    
    except requests.exceptions.RequestException as e:
        logging.exception("❌ Network-related error while calling NewsAPI")
        return {"error": f"Network error: {e}"}
    
    except ValueError as e:
        logging.exception(f"❌ Error in NewsAPI response: {e}")
        return {"error": f"Error: {e}"}
    
    except Exception as e:
        logging.exception(f"❌ Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}
