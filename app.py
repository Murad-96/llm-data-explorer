# app.py

import streamlit as st
import pandas as pd
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import matplotlib.pyplot as plt
import io
from dotenv import load_dotenv

# Set up OpenAI API key (best to load from env or st.secrets)
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

st.title("📊 LLM-Powered Data Explorer")
st.write("Upload a CSV file and ask questions about your data!")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of dataset:", df.head())

    # Create Pandas Agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

    # User question input
    user_question = st.text_input("Ask a question about the data:")

    if user_question:
        with st.spinner("Thinking..."):
            response = agent.run(user_question)
            st.write("### Answer:")
            st.write(response)

            # Append to chat history
            st.session_state.chat_history.append({
                "question": user_question,
                "response": response
            })

    # Auto Summary Report
    st.write("---")
    st.write("### 📄 Auto Summary Report")

    # 1️⃣ First: user selects style
    summary_style = st.selectbox(
        "Choose summary style:",
        ["Basic", "Data Analyst", "Business User"]
    )

    # 2️⃣ Then: user clicks button to run
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            if summary_style == "Basic":
                summary_prompt = "Summarize this dataset. Provide key statistics, any missing data, trends, and anything unusual."
            elif summary_style == "Data Analyst":
                summary_prompt = (
                    "Please analyze this dataset and generate a detailed summary. "
                    "Include the following: 1) number of rows and columns, 2) columns with missing data, "
                    "3) descriptive statistics (mean, median, std dev), 4) correlations between numeric columns, "
                    "5) any trends or patterns, 6) any outliers or anomalies."
                )
            else:
                summary_prompt = (
                    "Explain this dataset in simple business terms. What does this data show? "
                    "What are the key trends or insights a business user should know? "
                    "Are there any risks, anomalies, or unusual patterns?"
                )

            # Run agent
            summary_response = agent.run(summary_prompt)
            st.write("### Summary:")
            st.write(summary_response)


    # Basic chart generation
    st.write("---")
    st.write("### Generate Chart")
    chart_type = st.selectbox("Choose chart type:", ["None", "Bar", "Line", "Histogram", "Scatter"])

    if chart_type != "None":
        x_column = st.selectbox("X-axis:", df.columns)
        y_column = st.selectbox("Y-axis:", df.columns)

        fig, ax = plt.subplots()

        if chart_type == "Bar":
            ax.bar(df[x_column], df[y_column])
        elif chart_type == "Line":
            ax.plot(df[x_column], df[y_column])
        elif chart_type == "Histogram":
            ax.hist(df[x_column])
        elif chart_type == "Scatter":
            ax.scatter(df[x_column], df[y_column])

        st.pyplot(fig)

        # Save chart to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        # Download chart button
        st.download_button(
            label="Download Chart as PNG",
            data=buf,
            file_name=f"chart_{uploaded_file.name}.png",
            mime="image/png"
        )

    # Chat History Download
    st.write("---")
    st.write("### 💾 Download Chat History")

    if st.session_state.chat_history:
        # Build JSON
        import json
        import datetime

        chat_record = {
            "dataset_name": uploaded_file.name,
            "history": st.session_state.chat_history,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Convert to bytes
        json_bytes = json.dumps(chat_record, indent=4).encode('utf-8')

        st.download_button(
            label="Download Chat History as JSON",
            data=json_bytes,
            file_name=f"chat_history_{uploaded_file.name}.json",
            mime="application/json"
        )
    else:
        st.info("No chat history yet. Ask a question first!")

