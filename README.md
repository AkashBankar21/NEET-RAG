# 📘 NEET RAG Helper

A Retrieval-Augmented Generation (RAG) based study assistant built for NEET preparation. The system allows students to query their syllabus directly and get precise answers grounded in the textbook.  

## ✨ Features
- **Source Referencing**: Displays the exact page number from the textbook for every answer.  
- **Out-of-Syllabus Detection**: Identifies and flags queries that fall outside the NEET syllabus.  
- **Local Deployment**: Built with **Streamlit**, enabling a lightweight and interactive UI that runs locally without requiring cloud resources.  
- **Retrieval + Generation**: Combines document retrieval (keyword/semantic search) with language model generation to provide accurate, context-aware responses.  

This tool helps students save time, avoid misinformation, and focus on the most relevant study material.  

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/neet-rag-helper.git
   cd neet-rag-helper
````

2. Create a `.env` file in the root directory and add your OpenAI key:

   ```env
   OPENAI_API_KEY="your-api-key"
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Streamlit app:

   ```bash
   streamlit run default.py
   ```

---

## 🛠 Tech Stack

* **Python**
* **Streamlit**
* **LangChain / RAG pipeline**
* **OpenAI API**

---

## 📌 Note

* Make sure you have Python 3.8+ installed.
* If you face dependency issues, try creating a fresh virtual environment before installing requirements.

