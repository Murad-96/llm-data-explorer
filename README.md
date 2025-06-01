# llm-data-explorer

📄 Auto Summary & API Access
The app supports automated summary generation using pre-defined LLM prompts. Users can click "Generate Summary" in the UI or access the functionality via a REST API:

/summarize endpoint: Accepts a CSV file upload and returns a JSON summary
Built using FastAPI for easy integration into other services
Summary includes: dataset statistics, missing data, correlations, trends, anomalies
This enables automation and integration with external systems, making the app suitable for both interactive use and backend pipelines.