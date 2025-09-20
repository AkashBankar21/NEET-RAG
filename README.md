# 📘 NEET RAG Helper

A Retrieval-Augmented Generation (RAG) based study assistant built for NEET preparation. The system allows students to query their syllabus directly and get precise answers grounded in the textbook. Key features include:

* **Source Referencing**: Displays the exact page number from the textbook for every answer.
* **Out-of-Syllabus Detection**: Identifies and flags queries that fall outside the NEET syllabus.
* **Local Deployment**: Built with **Streamlit**, enabling a lightweight and interactive UI that runs locally without requiring cloud resources.
* **Retrieval + Generation**: Uses a combination of document retrieval (keyword/semantic search) and language model generation to provide accurate, context-aware responses.

This tool helps students save time, avoid misinformation, and focus on the most relevant study material.


## How to Run -
1. create a .env file in the folder where you pulled this repo, with OPENAI_API_KEY = "your-api-key"
2. in cmd use 'streamlit run default.py' to run
