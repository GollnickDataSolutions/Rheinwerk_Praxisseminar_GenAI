#%% packages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
load_dotenv('.env')
from langchain_core.pydantic_v1 import BaseModel, Field

#%% structured output
class TranslationResponse(BaseModel):
    translated_text: str = Field(description="the translated text")
    detected_language: str =  Field(description="the source language of the input text")

#%% set up prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that translates a source language into other languages. No babbling! Make sure your output is a valid JSON object with the following fields: translated_text, detected_language."),
    ("user", "Translate this sentence: '{input}' into {target_language}"),
])

# %% model
model = ChatOpenAI(model="gpt-4o-mini", 
                   temperature=0)

# %% chain
chain = prompt | model | JsonOutputParser(pydantic_object=TranslationResponse)

# %% invoke chain
res = chain.invoke({"input": "I love programming.", "target_language": "German"})
res
# %% input: a sentence
# output: {'tonality': ['warm', 'aggressive', 'depressed']}
