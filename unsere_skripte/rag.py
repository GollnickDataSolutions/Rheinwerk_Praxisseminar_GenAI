
#%% Pakete
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
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

#%% Vektor DB als Retriever
def rag(query: str) -> str:
    retriever = faiss_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    res = retriever.invoke(query)

    # Kontextinformationen vorverarbeiten
    # gegeben: [Document(page_content=...), ...]
    # gesucht: "page_content1; page_content2; ..."
    context_info = "; ".join([doc.page_content for doc in res])

    # LLM instanz erstellen
    model = ChatOpenRouter(model="google/gemini-3-flash-preview")

    # Prompt Template
    messages = [
        ("system", """
        Du beantwortest Fragen des Nutzers.
        Dafür erhältst du zusätzlichen Kontext.
        Beantworte ausschließlich auf Basis des Kontextes, der dir übergeben wird und sage 'Ich weiß es nicht' wenn der Kontext die Beantwortung nicht möglich macht.
        Antworte kurz und bündig innerhalb eines Satzes.
        """),
        ("user", "Benutzeranfrage: {user_query}, Kontextinformationen: {context_info}")
    ]
    prompt_template = ChatPromptTemplate.from_messages(messages)
    #  Chain erstellen
    chain = prompt_template | model
    #  Chain aufrufen
    model_response = chain.invoke({"user_query": query, "context_info": context_info})

    return model_response.content
# %%
rag(query="wer ist Gretel?")