#%% Pakete
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from dotenv import load_dotenv
load_dotenv()
# %% 1. Lade eine einzelne txt Datei
file_path = "data/grimm.txt"
loader = TextLoader(
    file_path=file_path, 
    # encoding="utf-8",
    autodetect_encoding=True
    )
docs = loader.load()
# %%
# docs[0].page_content
docs[0].metadata

#%% 2. Lade alle Dateien innerhalb eines Ordners (gleicher Dateityp)
dir_path = "data/"
loader = DirectoryLoader(
    path=dir_path,
    loader_cls=TextLoader,
    loader_kwargs={"autodetect_encoding": True}
)
docs = loader.load()
print(docs)

#%% Übung: ladet eines der beiden Dokumente direkt aus dem Netz

#%% 
import os
def load_document(file_path: str):
    # 1. extrahiere die Dateiendung aus dem Dateinamen
    _, ext = os.path.splitext(file_path)
    # 2. wähle den richtigen Loader, je nach Endung
    if ext == ".txt":
        return TextLoader(
            file_path=file_path, 
            # encoding="utf-8",
            autodetect_encoding=True
            )
    elif ext==".pdf":
        return PyMuPDF4LLMLoader(file_path, mode="page")

from langchain_pymupdf4llm import PyMuPDF4LLMLoader
dir_path = "data/"
loader = DirectoryLoader(
    path=dir_path,
    loader_cls=load_document,
    glob="*.txt"
)
docs = loader.load()
docs

# %%
# docs[1].metadata

#%% Data Chunking / Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=800)
# %%
docs_splitted = splitter.split_documents(docs)
len(docs_splitted)

#%% Embeddings
embedding_model = OpenAIEmbeddings()

sentences = [
    'The cat lounged lazily on the warm windowsill.',
    'A feline relaxed comfortably on the sun-soaked ledge.',
    'The kitty reclined peacefully on the heated window perch.',
    'Quantum mechanics challenges our understanding of reality.',
    'The chef expertly julienned the carrots for the salad.',
    'The vibrant flowers bloomed in the garden.',
    'Las flores vibrantes florecieron en el jardín. ',
    'Die lebhaften Blumen blühten im Garten.'
]

sentences_embed = embedding_model.embed_documents(sentences)
# %%
len(sentences_embed[0])

from langchain_community.vectorstores.utils import cosine_similarity

# %%
sim_mat = cosine_similarity(sentences_embed, sentences_embed)
import seaborn as sns
sns.heatmap(sim_mat, xticklabels=sentences, yticklabels=sentences, annot=True)

#%%
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
# sentences_embed = embedding_model.embed_documents(sentences)

# %%
from langchain_community.vectorstores import FAISS
faiss_db = FAISS.from_documents(documents=docs_splitted, embedding=embedding_model)
# %%
faiss_db.save_local(folder_path="weltliteratur")