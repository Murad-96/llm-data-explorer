# 📊 LLM-Powered Data Explorer
An interactive AI-powered data analysis tool built using LangChain, OpenAI API, Pandas, and Streamlit.
Try it live → https://llm-data-explorer.streamlit.app 🚀

## ✨ Features
✅ Upload CSV dataset
✅ Ask questions about your data (natural language)
✅ Auto-generate Pandas code and compute real answers
✅ Generate visualizations (Bar, Line, Histogram, Scatter)
✅ Auto Summary Report — choose summary style:
* Basic
* Data Analyst
* Business User
✅ Save and download chat history as JSON
✅ Download generated charts as PNG
✅ Optional REST API: /summarize endpoint (FastAPI)

📄 Auto Summary & API Access
The app supports automated summary generation using pre-defined LLM prompts. Users can click "Generate Summary" in the UI or access the functionality via a REST API:

/summarize endpoint: Accepts a CSV file upload and returns a JSON summary
Built using FastAPI for easy integration into other services
Summary includes: dataset statistics, missing data, correlations, trends, anomalies
This enables automation and integration with external systems, making the app suitable for both interactive use and backend pipelines.