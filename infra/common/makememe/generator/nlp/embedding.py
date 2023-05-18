import os
import openai
from typing import List
import numpy as np
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('../.env'))
from common.content_generator import ContentGenerator

openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text: str) -> List[float]:
    contentGen = ContentGenerator()
    return contentGen.get_embedding(text)


def semantic_search(documents, meme_description, pprint=True):
    # Get embeddings for all documents
    document_embeddings = [get_embedding(x) for x in documents]
    
    # Get embedding for meme_description
    meme_embedding = get_embedding(meme_description)
    
    # Calculate similarities for all document embeddings
    similarities = [cosine_similarity(x, meme_embedding) for x in document_embeddings]
    
    # Combine documents, embeddings, and similarities
    combined = list(zip(documents, document_embeddings, similarities))

    # Sort by similarity
    sorted_combined = sorted(combined, key=lambda x: x[2], reverse=True)

    # Get the document with highest similarity
    res = sorted_combined[0][0]

    print('semantic_search results:', res)

    return res

