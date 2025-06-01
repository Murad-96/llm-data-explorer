# fastapi_app.py

from fastapi import FastAPI, UploadFile, File
import pandas as pd
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv

import datetime

app = FastAPI()

# Load OpenAI key from env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    # Read CSV into DataFrame
    df = pd.read_csv(file.file)

    # Create agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, 
                                          max_iterations=20, 
                                          allow_dangerous_code=True)

    # Use fixed summary prompt (you can also add variants)
    summary_prompt = (
        "Please analyze this dataset and generate a detailed summary. "
        "Include: number of rows/columns, missing data, statistics, correlations, trends, anomalies."
    )

    # Run agent
    summary_response = agent.run(summary_prompt)

    # Build response JSON
    response_json = {
        "dataset_name": file.filename,
        "summary": summary_response,
        "timestamp": datetime.datetime.now().isoformat()
    }

    return response_json
