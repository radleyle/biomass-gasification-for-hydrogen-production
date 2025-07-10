import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Debug: Check if API key is loaded
#print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

CHROMA_PATH = "chroma"
RESULTS_PATH = "query_results"

PROMPT_TEMPLATE = """
You are a scientific assistant analyzing biomass gasification research papers for experimental data extraction.

CONTEXT DOCUMENTS:
{context}

TASK: Extract specific experimental data that matches the query: {question}

REQUIREMENTS:
1. Focus ONLY on experimental data with numerical values
2. Prioritize data in mol/kg, mmol/g, or clearly convertible units
3. Include experimental conditions (temperature, pressure, time)
4. SEARCH ALL CONTEXT DOCUMENTS for feedstock/biomass type information (may be in different sections)
5. Cite specific sources for each data point

OUTPUT FORMAT:
**Experimental Data Found:**
- Technology: [Steam/CO₂/Plasma/SCW Gasification]
- Feedstock: [SEARCH ALL DOCUMENTS - biomass type, source location if available]
- Conditions: [temperature, pressure, time if available]
- H₂ Yield: [value with units] (Source: [paper name])
- CO Yield: [value with units] (Source: [paper name])
- Other yields: [if relevant]

**Key Findings:**
[2-3 bullet points summarizing the most important experimental results]

**Source Reliability:**
[Brief assessment of data quality and consistency across sources]

**Missing Information:**
[What experimental details are not available]

IMPORTANT: Look through ALL provided context documents for feedstock information - it may be mentioned in materials/methods sections separate from the experimental data. Common feedstocks include: rice husk, bagasse, sawdust, wood chips, agricultural residues, etc.

If no relevant experimental data is found, state: "No experimental gasification data found matching the query criteria."
"""


def main():
    # create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output including full prompt and document previews.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text, verbose=args.verbose)
    
def query_rag(query_text, verbose=False):
    # prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # search the DB for top k results
    results = db.similarity_search_with_relevance_scores(query_text, k=12)
    
    # Show top similarity scores
    print(f"🔍 Query: {query_text}")
    print(f"📊 Found {len(results)} results")
    if results:
        print(f"🎯 Best similarity score: {results[0][1]:.3f} (threshold: 0.5)")
        for i, (doc, score) in enumerate(results[:3]):
            source = doc.metadata.get('id', 'Unknown').split(':')[0].split('/')[-1]
            print(f"   {i+1}. {score:.3f} | {source}")
            
            # Verbose: Show document previews
            if verbose:
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"      Preview: {preview}...")
    
    if len(results) == 0 or results[0][1] < 0.5:
        print("❌ Unable to find relevant results above threshold.")
        return
    
    print("\n🤖 Analyzing with GPT-4...")
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Verbose: Show full prompt
    if verbose:
        print("\n" + "="*50)
        print("📄 FULL PROMPT SENT TO GPT-4")
        print("="*50)
        print(prompt)
        print("="*50)
    
    # Use GPT-4 for scientific data extraction (better accuracy)
    model = ChatOpenAI(model="gpt-4", temperature=0)  # Better for scientific reasoning
    response_text = model.invoke(prompt)
    response_text = response_text.content
    
    # Check if feedstock is missing and try expanded queries
    if "not specified" in response_text.lower() or "biomass type" in response_text.lower():
        print("\n🔄 Feedstock not found, trying expanded queries...")
        expanded_results = try_expanded_queries(db, query_text, verbose)
        
        # If expanded queries don't work, try document-level search
        if not expanded_results or "not specified" in model.invoke(prompt_template.format(
            context="\n\n---\n\n".join([doc.page_content for doc, _score in expanded_results]), 
            question=query_text
        )).content.lower():
            print("🔍 Trying document-level search for feedstock info...")
            additional_chunks = get_document_context(db, results, query_text)
            if additional_chunks:
                # Combine original results with feedstock chunks
                combined_results = results[:8] + additional_chunks[:4]  # 8 + 4 = 12 total
                context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in combined_results])
                prompt = prompt_template.format(context=context_text, question=query_text)
                response_text = model.invoke(prompt).content
                results = combined_results
                print("✅ Added document-level feedstock context!")
        elif expanded_results:
            # Use the expanded query results
            results = expanded_results
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt = prompt_template.format(context=context_text, question=query_text)
            response_text = model.invoke(prompt).content
            print("✅ Found better results with expanded query!")
    
    print("\n" + "="*50)
    print("📋 EXPERIMENTAL DATA ANALYSIS")
    print("="*50)
    print(response_text)
    print("="*50)
    
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    
    # Verbose: Show detailed source list
    if verbose:
        print("\n📚 DETAILED SOURCES:")
        for i, source in enumerate(sources):
            print(f"   {i+1}. {source}")
    
    # Save results to markdown file
    similarity_scores = [(score, doc.metadata.get('id', 'Unknown').split(':')[0]) for doc, score in results]
    save_query_result(query_text, results, response_text, similarity_scores)
    
    return response_text

def try_expanded_queries(db, original_query, verbose=False):
    """Try expanding the query with common feedstock terms."""
    common_feedstocks = ["rice husk", "bagasse", "sawdust", "wood chips", "corn stover", "wheat straw", "biomass"]
    
    best_results = None
    best_score = 0
    
    for feedstock in common_feedstocks:
        expanded_query = f"{feedstock} {original_query}"
        results = db.similarity_search_with_relevance_scores(expanded_query, k=20)  # Increased from k=12
        
        if results and results[0][1] > best_score:
            best_score = results[0][1]
            best_results = results
            if verbose:
                print(f"   Trying: {expanded_query} → Score: {results[0][1]:.3f}")
    
    return best_results if best_score > 0.5 else None

def get_document_context(db, results, query_text):
    """Get additional chunks from the same documents to find missing feedstock info."""
    # Get document sources from current results
    doc_sources = set()
    for doc, score in results[:5]:  # Top 5 results
        source_file = doc.metadata.get('id', '').split(':')[0]
        doc_sources.add(source_file)
    
    # Search for feedstock terms in the same documents
    feedstock_terms = ["feedstock", "material", "biomass", "substrate", "raw material", "obtained from"]
    additional_chunks = []
    
    for term in feedstock_terms:
        term_results = db.similarity_search_with_relevance_scores(term, k=30)
        for doc, score in term_results:
            source_file = doc.metadata.get('id', '').split(':')[0]
            if source_file in doc_sources and score > 0.3:  # Same document, decent similarity
                additional_chunks.append((doc, score))
    
    # Remove duplicates and sort by score
    seen_ids = set()
    unique_chunks = []
    for doc, score in additional_chunks:
        doc_id = doc.metadata.get('id', '')
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            unique_chunks.append((doc, score))
    
    # Return top additional chunks
    unique_chunks.sort(key=lambda x: x[1], reverse=True)
    return unique_chunks[:10]
    
def save_query_result(query_text, results, response_text, similarity_scores):
    """Save query results to a markdown file for documentation and analysis."""
    
    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_PATH, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = query_text.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
    filename = f"{timestamp}_{safe_query}.md"
    filepath = os.path.join(RESULTS_PATH, filename)
    
    # Create markdown content
    content = f"""# RAG Query Result

## Query Information
- **Query**: {query_text}
- **Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Database**: {CHROMA_PATH}
- **Results Found**: {len(results)}

## Similarity Scores
"""
    
    for i, (score, source) in enumerate(similarity_scores[:5]):
        content += f"- **{i+1}.** Score: {score:.3f} | Source: {source}\n"
    
    content += f"""
## GPT-4 Analysis

{response_text}

## Source Details
"""
    
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    for i, source in enumerate(sources):
        content += f"- {i+1}. {source}\n"
    
    content += f"""
## Raw Context (First 3 Documents)
"""
    
    for i, (doc, score) in enumerate(results[:3]):
        content += f"""
### Document {i+1} (Score: {score:.3f})
**Source**: {doc.metadata.get('id', 'Unknown')}

```
{doc.page_content[:500]}...
```
"""
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📁 Results saved to: {filepath}")
    return filepath
    
if __name__ == "__main__":
    main()