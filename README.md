# AI News Summarizer Agent

## Overview

This project is an AI-powered news summarizer agent built using **FastAPI**, **LangChain**, **Pinecone**, **Google Generative AI Embeddings**, and **NewsAPI**. The goal of this agent is to summarize news articles based on user queries and store relevant information in a persistent memory for future reference.

## Features

- **News Summarization**: The agent fetches the latest news articles from NewsAPI and provides concise summaries.
- **Memory Recall**: Stores previous user queries in Pinecone for future retrieval to enhance the user's experience.
- **Integration with Google Generative AI**: Utilizes Google’s generative AI to provide the news summaries.

## Requirements

Make sure you have the following libraries installed:

- FastAPI
- LangChain
- Pinecone
- Google Generative AI Embeddings
- Requests
- Python-dotenv

To install the required libraries, run:

```bash
pip install -r requirements.txt
