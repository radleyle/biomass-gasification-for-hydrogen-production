from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    # get embedding for a word
    embedding_function = OpenAIEmbeddings()
    vector = embedding_function.embed_query("gasification")
    print(f"Vector for 'gasification': {vector}")
    print(f"Vector length: {len(vector)}")
    
    # compare vector of two words
    evaluator = load_evaluator("pairwise_embedding_distance")
    words = ("gasification", "energy")
    # for i in range(len(words)):
    #     for j in range(i + 1, len(words)):
    #         score = evaluator.evaluate_strings(
    #             words[i], words[j], vector_a=vector, vector_b=vector
    #         )
    #         # use x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1]) if want to compare two strings only
    #         # if the score is close to 1, then the two words are similar
    #         print(f"Similarity between '{words[i]}' and '{words[j]}': {score}")
    x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
    print(f"Similarity between '{words[0]}' and '{words[1]}': {x}")
            
if __name__ == "__main__":
    main()