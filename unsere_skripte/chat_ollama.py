#%% Pakete
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
print(load_dotenv())
from rich.console import Console
from rich.markdown import Markdown
console = Console()


#%% Promptvorlage erstellen
messages = [
    ("system", """
        Du bist ein Comedian im Stile von Heinz Erhard.
        Du erstellst einen Witz zu einem Thema, welches vom Nutzer übergeben wird.
        Antworte in max. 4 Sätzen.
    """),
    ("user", "Thema: {thema}")
]
prompt_template = ChatPromptTemplate.from_messages(messages)

#%% Modellinstanz erstellen
model = ChatOllama(
    model="gemma3:4b",
    temperature=0
)

#%% Chain erstellen
chain = prompt_template | model

# %% Anfrage an die Chain stellen
res = chain.invoke({'thema': 'Benzinpreis'})

# %% Chatantwort
console.print(Markdown(res.content))

#%% sonstigen Metadateninformationen
# res.model_dump()