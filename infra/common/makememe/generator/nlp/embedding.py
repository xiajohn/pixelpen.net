import os, json
import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('../.env'))


openai.api_key = os.getenv("OPENAI_API_KEY")

def test_embedding(): 
  df_thing = pd.DataFrame({ "stuff": np.array(['some', 'random', 'stuff'])})

  thing1 = get_embedding('something', engine='text-embedding-ada-002')
  thing2 = get_embedding('lots of things', engine='text-embedding-ada-002')
  something = cosine_similarity(thing1, thing2)
  print(something)

def semantic_search(documents, meme_description, pprint=True):
  df = pd.DataFrame({ "documents": np.array(documents)})
  df['document_embeddings'] = df.documents.apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
  meme_embedding = get_embedding(meme_description, engine='text-embedding-ada-002')
  df['similarities'] = df.document_embeddings.apply(lambda x: cosine_similarity(x, meme_embedding))
  # get the highest similarity
  res = df.sort_values(by='similarities', ascending=False).iloc[0].documents
  print('semantic_search results:', res)
  
  return res

