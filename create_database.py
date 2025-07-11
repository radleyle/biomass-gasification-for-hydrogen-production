from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil

# Load environment variables from .env file
load_dotenv()

# Debug: Check if API key is loaded
print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

openai.api_key = os.environ["OPENAI_API_KEY"]

CHROMA_PATH = "chroma"
DATA_PATH = "data/docling_md/testing/scw"

def main():
    try:
        generate_data_store()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    
def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)
    
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)
    
    return chunks

def save_to_chroma(chunks: list[Document]):
    # clear out the datavase first
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    # create a new db from the documents
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")
    
if __name__ == "__main__":
    main()