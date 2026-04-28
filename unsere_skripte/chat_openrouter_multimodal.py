#%% Pakete
import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
print(load_dotenv())
from rich.console import Console
from rich.markdown import Markdown
console = Console()
import base64

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

#%% Bild codieren als Base64-string
image_path = "kiki.jpg"
img_encoded = encode_image(image_path)

# %% Testen, ob der API Key verfügbar ist
print(os.getenv("OPENROUTER_API_KEY"))

#%% Promptvorlage erstellen
messages = [
    ("system", """
        Du bist ein Fotoexperte, der Fragen zu Bildern beantworten kann.
        Antworte kurz und bündig.
    """),
    {
            "role": "user",
            "content": [
                {"type": "text", "text": "{query}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_encoded}",
                    },
                },
            ],
    }
]
prompt_template = ChatPromptTemplate.from_messages(messages)

#%% Modellinstanz erstellen
model = ChatOpenRouter(
    model="google/gemini-2.5-flash-lite",
    temperature=0,
    top_p=0.8,
    max_completion_tokens=1000
)

#%% Chain erstellen
chain = prompt_template | model

# %% Anfrage an die Chain stellen
res = chain.invoke({'query': 'Was ist auf dem Bild zu sehen?'})

# %% Chatantwort
console.print(Markdown(res.content))

#%% sonstigen Metadateninformationen
# res.model_dump()