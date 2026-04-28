#%% Pakete
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

#%% Embedding Model
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

#%% FAISS DB
faiss_db = FAISS.load_local(
    folder_path="weltliteratur", 
    embeddings=embedding_model,
    allow_dangerous_deserialization=True)
# %% Query the DB
query = "Wer ist Rumpelstilzchen?"
res = faiss_db.similarity_search(query, k=3)

#%% Show the results
for doc in res:
    print(doc.page_content)
    print("-"*20)

#%%