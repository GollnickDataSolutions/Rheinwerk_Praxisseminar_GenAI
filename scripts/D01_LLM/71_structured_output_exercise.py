#%% packages
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
load_dotenv('.env')
from langchain_core.pydantic_v1 import BaseModel, Field

#%% structured output
sentiment_categories = ['happy', 'sad', 'angry', 'neutral', 'excited']
sentiment_categories_str = ", ".join(sentiment_categories)

class SentimentResponse(BaseModel):
    tonality: list[str] = Field(description=f"a list of tonality categories that can only be {sentiment_categories_str}", 
                                allowed_values=sentiment_categories
                                )
    

#%% set up prompt template

prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are an AI assistant that returns the tonality of a sentence. No babbling! Make sure your output is a valid JSON object with the following fields: tonality. The tonality can only be {sentiment_categories_str}."),
    ("user", "Translate this sentence: '{input}' into {target_language}"),
])

# %% model
model = ChatOpenAI(model="gpt-4o-mini", 
                   temperature=0)

# %% chain
chain = prompt | model | JsonOutputParser(pydantic_object=SentimentResponse)

# %% invoke chain
# user_prompt = "I am super happy today."  # happy
# user_prompt = "I could cry."  # sad
# user_prompt = "I cannot wait to see you again."  # excited
# user_prompt = "I hate it when people are late!"  # angry
user_prompt = "The sky is blue today."  # neutral

res = chain.invoke({"input": user_prompt, "target_language": "German"})
res
# %% input: a sentence
# output: {'tonality': ['happy', 'sad', 'angry', 'neutral', 'excited']}
