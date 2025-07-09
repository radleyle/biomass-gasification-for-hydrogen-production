from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

def get_embedding_function():
    # Option 1: OpenAI embeddings (best for scientific content)
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Good balance
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # Best quality
    
    # Option 2: AWS Bedrock embeddings 
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    
    # Option 3: Local Ollama embeddings (current - fast but lower quality)
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    return embeddings