#%% pakete
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler

#%% Token Usage Callback Handler
class TokenUsageCallback(BaseCallbackHandler):
    def __init__(self):
        self.token_usage = {}
    
    def on_llm_end(self, response, **kwargs):
        """Capture token usage when LLM finishes"""
        if hasattr(response, 'llm_output') and response.llm_output:
            if 'token_usage' in response.llm_output:
                self.token_usage = response.llm_output['token_usage']

#%% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
        Du bist ein Witzeerzähler und bekommst ein Thema vorgegeben.
        Erstelle bitte 3 Witze und gib die Wahrscheinlichkeit dazu an.
        Gib nur Witze mit Wahrscheinlichkeit kleiner 10 Prozent
    """),
    ("user", "Thema: <<{thema}>>")
])


# %% Modellinstanz
MODEL_NAME="llama-3.3-70b-versatile"
model = ChatGroq(model=MODEL_NAME)

#%% Chain erstellen
chain = prompt_template | model | StrOutputParser()

# %% chain invocation
topic = "Messi und Ronaldo"

# Create callback handler to track token usage
token_callback = TokenUsageCallback()

# Invoke chain with parser and callback
output = chain.invoke({"thema": topic}, config={"callbacks": [token_callback]})

#%% Ergebnis
from pprint import pprint
print("Output (parsed):")
pprint(output)
print("\nToken Usage:")
print(f"  Prompt tokens: {token_callback.token_usage.get('prompt_tokens', 0)}")
print(f"  Completion tokens: {token_callback.token_usage.get('completion_tokens', 0)}")
print(f"  Total tokens: {token_callback.token_usage.get('total_tokens', 0)}")


# %%
