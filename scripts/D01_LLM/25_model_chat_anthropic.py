#%% packages
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))
import os

# %% create a model instance
MODEL_NAME = "claude-3-haiku-20240307"
model = ChatAnthropic(model=MODEL_NAME, 
                      api_key=os.getenv("CLAUDE_API_KEY"))

#%% model inference
user_prompt = "What is the most recent information you have and what is its date?"

res = model.invoke(user_prompt)
# %%
from pprint import pprint
pprint(res.content)

# %%
res.model_dump()
# %%
