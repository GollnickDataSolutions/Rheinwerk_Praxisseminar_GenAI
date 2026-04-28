#%% Pakete
import os
import requests
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
print(load_dotenv())
from rich.console import Console
from rich.markdown import Markdown
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
console = Console()

# %% Testen, ob der API Key verfügbar ist
print(os.getenv("TAVILY_API_KEY"))

#%% Tools
search_tool = TavilySearch(max_results=3, topic="news")

@tool
def count_letters(word: str, letter: str):
    """ zählt die Vorkommen eines Buchstabens innerhalb eines Wortes
    Args:
        word: das Wort, dessen Buchstaben gezählt werden sollen
        letter: der Buchstabe, der gezählt werden soll
    """
    return word.lower().count(letter)

#%% get weather function
@tool
def get_weather(lat: float, long: float):
    """ fetches temperature information for a given latitude and longitude
    Args:
        lat: Latitude of the city
        long: Longitude of the city
    Returns:
        Temperature in Degree Celsius
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m"
    res = requests.get(url).json()
    return res["current"]["temperature_2m"]

    

# TEST
# get_weather(lat=52, long=14)
# count_letters("erdbeere", "e")

#%% Modellinstanz erstellen
model = ChatOpenRouter(
    model="google/gemini-3-flash-preview",
    temperature=0,
    top_p=0.8,
    max_completion_tokens=1000
)


#%% Agent
agent = create_agent(
    model=model, 
    tools=[search_tool, count_letters, get_weather], 
    system_prompt="Wenn du die Antwort nicht in deinen Modellgewichten hast, nutze ein passendes Tool. Wenn du ein Tool aufrufst, vertraue immer dem Tool-Ergebnis und gib es exakt so weiter, und Gib die quellen inkl. URL mit aus. Falls du ein Tool verwendest, gib den Grund an, warum du das getan hast.")

#%% Teste das Modell (zeige, dass das Modell keine aktuellen Infos hat)
# user_query="Was ist der Stand am 28.04.2026 bzgl. der Straße von Hormus?"
user_query="Wie warm ist es aktuell in Hamburg"
# res = model.invoke(user_query)

#%% Teste den Agenten
res = agent.invoke({"messages": [("user", user_query)]})
#%%
console.print(Markdown(res["messages"][-1].content))

# %%
