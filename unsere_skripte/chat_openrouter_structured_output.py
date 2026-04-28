#%% Pakete
import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
print(load_dotenv())
from rich.console import Console
from rich.markdown import Markdown
console = Console()

#%% output parser
class Movie(BaseModel):
    title: str
    director: str = Field(
        description="Der Regisseur des Films", 
        examples=["Cameron, James", "Nolan, Christopher"])
    main_actors: list[str]
    release_year: int
    confidence: str = Field(description="die zahl gibt an, wie sicher das Modell ist, dass der Film exakt zur Beschreibung passt.", examples=["87 %", "43 %"])

class Movies(BaseModel):
    movies: list[Movie]

output_parser = JsonOutputParser(pydantic_object=Movies)
console.print(output_parser.get_format_instructions())

# %% Testen, ob der API Key verfügbar ist
print(os.getenv("OPENROUTER_API_KEY"))

#%% Promptvorlage erstellen
messages = [
    ("system", """
        Du bist Filmexperte und bekommst vom Nutzer die Handlung beschrieben.
        Gib die 5 relevantesten Filme zurück.
        Halte dich konkret an die Formatanweisungen {format_anweisung}

    """),
    ("user", "Handlung: {handlung}")
]
prompt_template = ChatPromptTemplate.from_messages(messages).partial(format_anweisung=output_parser.get_format_instructions())
prompt_template

#%% Modellinstanz erstellen
model = ChatOpenRouter(
    model="google/gemini-3-flash-preview",
    temperature=0,
    top_p=0.8,
    max_completion_tokens=1000
)

#%% Chain erstellen
chain = prompt_template | model | output_parser

# %% Anfrage an die Chain stellen
res = chain.invoke({'handlung': 'ein fisch sucht seinen Sohn'})

# %% Chatantwort
for m in res["movies"]:
    print(m["title"])
    print(m["director"])
    print(m["main_actors"])
    print(m["confidence"])
    print("-"*20)
