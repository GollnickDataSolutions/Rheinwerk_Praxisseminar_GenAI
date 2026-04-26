#%% packages
import os
from autogen import ConversableAgent
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
 
#%% LLM config
from langchain.chat_models import ChatOpenAI
 
llm_config = {
    "config_list": [
        {"model": "gpt-4o-mini",
         "temperature": 0.8,
         "api_key": os.getenv("OPENAI_API_KEY")}
    ]
}
 
 
 
jack_flat_earther = ConversableAgent(
    name="jack_flat_earther",
    llm_config=llm_config,
    system_message="""
Du glaubst fest, dass die Erde flach ist. Du versuchst, andere von Deiner Meinung zu überzeugen. Mit jeder Antwort wirst Du wütender, frustrierter und aggressiver. Je wütender Du bist, desto mehr '!11!!' integrierst Du in Deine Nachrichten.
""",
    human_input_mode="NEVER"
)
 
#%% set up the agent: Alice, the scientist
alice_scientist = ConversableAgent(
    name="alice_scientist",
    llm_config=llm_config,
    system_message="""
    Du bist eine erfahrene Wissenschaftlerin, Du heißt Ricarda Dawkins. Antworte vollständig rational, wie Richard Dawkins es machen würde. Du provozierst mit Deiner Rationalität. Du verstehst keine Gefühle, aber gehst auf wissenschaftliche Argumente ein.
    """,
    human_input_mode="NEVER"
)
 
 
#%% start the conversation
result = jack_flat_earther.initiate_chat(
    recipient=alice_scientist,
    message="Hallo, wie weit ist es bis zum Rand der Erde von Hamburg?",
    max_turns=10
)
# %%
