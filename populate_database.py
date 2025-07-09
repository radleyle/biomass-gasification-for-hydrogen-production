import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function 
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CHROMA_PATH = "chroma"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the directory containing PDF files.")
    args = parser.parse_args()
    if args.reset:
        print("Resetting the database...")
        clear_database()
        
    # create (or update) the database
    documents = load_documents(args.data_path)
    print(f"Loaded {len(documents)} documents from {args.data_path}")
    if documents:
        print(f"Sample document: {documents[0].metadata}")
        chunks = split_documents(documents)
        add_to_chroma(chunks)
    else:
        print("No documents found in the specified path.")
    
def load_documents(data_path):
    print(f"Loading documents from: {data_path}")
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    return chunks

def add_to_chroma(chunks: list[Document]):
    # load the existing database
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    
    # calculate page IDs
    chunks_with_ids = calculate_chunk_ids(chunks)
    
    # add or update the documents
    existing_items = db.get(include=[]) # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    
    # only add documents that don't exist in the DB
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
            
    if len(new_chunks):
        print(f"Adding {len(new_chunks)} new documents to the database...")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add.")
        
def calculate_chunk_ids(chunks):
    # this will create IDs like "data/testing/scw/1.pdf:6:2"
    # Page Source : Page Number : Chunk Index
    
    last_page_id = None
    current_chunk_index = 0
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        
        # if the page ID is the same as the last one, increment the index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
            
        # calculate the chunk ID
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        
        # add it to the page meta-data
        chunk.metadata["id"] = chunk_id
        
    return chunks
            
    
def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    print(f"Database cleared: {CHROMA_PATH}")
    
if __name__ == "__main__":
    main()
