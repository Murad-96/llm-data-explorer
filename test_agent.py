# test_agent.py

import pandas as pd
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load your dataset
df = pd.read_csv("./data/example.csv")

# Initialize LLM
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# Create agent
agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True) #TODO: sandbox in production instead)

# Example query
query = "What is the average of column 'sales'?"
response = agent.run(query)

print("Response:", response)

