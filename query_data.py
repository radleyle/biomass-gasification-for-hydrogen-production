import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from get_embedding_function import get_embedding_function
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Debug: Check if API key is loaded
#print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

CHROMA_PATH = "chroma"

# PROMPT_TEMPLATE = """
# You are a scientific assistant analyzing biomass gasification research papers.

# Extract and summarize the following ONLY IF the paper includes:
# - A biomass feedstock (preferably wood chips or similar lignocellulosic material),
# - A gasifying agent that matches one of these: steam, CO₂, supercritical water, or plasma/oxygen,
# - Syngas output that includes H₂ and CO (not pure combustion or pyrolysis),
# - Yield data for hydrogen (H₂), carbon monoxide (CO), and char or ash (if present).

# Required output format:
# - Gasification Technology: [e.g., Steam Gasification]
# - Feedstock: [e.g., wood chips]
# - Gasifying agent: [e.g., steam]
# - Temperature & Pressure: [if available]
# - Hydrogen yield: [e.g., 35% or 9.2 mol/kg]
# - Carbon monoxide yield: [e.g., 8.1 mol/kg]
# - Char yield: [e.g., 0.15 kg/kg biomass or 'not reported']
# - Reference/citation: [e.g., Author (Year)]

# If the paper does not match these criteria, respond with: "No matching data found."
# """

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)
    
def query_rag(query_text):
    # prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # search the DB for top k results
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0 or results[0][1] < 0.5:
        print("Unable to find relevant results.")
        return
    
    #context_text = "\n\n".join([f"Document {i+1}:\n{result[0].page_content}" for i, result in enumerate(results)])
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    
    # model = ChatOpenAI(model="gpt-4", temperature=0)
    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)
    #response_text = response.content
    print(response_text)
    
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_responses = f"Responses: {response_text}\nSources: {sources}"
    print(formatted_responses)
    return response_text
    
if __name__ == "__main__":
    main()