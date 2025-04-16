from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import logging
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")
environment = os.getenv("PINECONE_ENV")

if not all([api_key, index_name, environment]):
    raise RuntimeError("❌ Pinecone API environment variables are missing.")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# List the indexes and check if the given index exists
existing_indexes = [i.name for i in pc.list_indexes()]

# Create index if it doesn't exist
if index_name not in existing_indexes:
    logging.info(f"Creating new index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=768,  # Ensure this matches the embedding dimension
        metric="cosine"
    )

# Connect to the index (make sure it's of type pinecone.Index)
index = pc.Index(index_name)

# Initialize embeddings - Replace 'models/embedding-001' with a valid model name
embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-001",  # Replace with the correct embedding model
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# LangChain wrapper for Pinecone
vectorstore = LangchainPinecone(index=index, embedding=embeddings, text_key="text")

def save_memory_to_pinecone(user_query):
    try:
        logging.debug(f"💾 Saving query to Pinecone: {user_query}")
        vectorstore.add_texts([user_query])
        logging.info("Query saved successfully!")
    except Exception as e:
        logging.exception("❌ Error saving memory to Pinecone")

def retrieve_memory_from_pinecone(user_query):
    try:
        logging.debug(f"🔍 Searching Pinecone for: {user_query}")
        results = vectorstore.similarity_search(user_query, k=1)
        return results[0].page_content if results else None
    except Exception as e:
        logging.exception("❌ Error retrieving memory from Pinecone")
        return None





