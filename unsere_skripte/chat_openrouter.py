#%% Pakete
import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
print(load_dotenv())
from rich.console import Console
from rich.markdown import Markdown
console = Console()

# %% Testen, ob der API Key verfügbar ist
print(os.getenv("OPENROUTER_API_KEY"))

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
model = ChatOpenRouter(
    model="google/gemini-3-flash-preview",
    temperature=0,
    top_p=0.8,
    max_completion_tokens=1000
)

#%% Chain erstellen
chain = prompt_template | model

# %% Anfrage an die Chain stellen
res = chain.invoke({'thema': 'Benzinpreis'})

# %% Chatantwort
console.print(Markdown(res.content))

#%% sonstigen Metadateninformationen
# res.model_dump()