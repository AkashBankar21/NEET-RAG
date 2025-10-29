# 📘 NEET RAG Helper

A **Retrieval-Augmented Generation (RAG)** powered study assistant designed specifically for **NEET exam preparation**. The system allows students to query their syllabus directly and receive accurate, textbook-grounded answers with source references.

Built with a **client-server architecture**, it uses **FastAPI** for backend processing and **Streamlit** for an interactive frontend interface.

---

## ✨ Features

* 🔍 **Source Referencing** — Displays the exact **book name, chapter, and page number** for every answer.
* 🚫 **Out-of-Syllabus Detection** — Identifies and flags queries that fall outside the NEET syllabus.
* ⚡ **RAG Pipeline (Retrieval + Generation)** — Combines **semantic document retrieval** with **language model-based response generation** for accurate, context-aware answers.
* 💻 **Client–Server Architecture** —

  * **FastAPI (Backend)**: Handles retrieval, generation, and data processing.
  * **Streamlit (Frontend)**: Provides an intuitive and lightweight user interface for querying and displaying results.
* 🧠 **Local Deployment** — Can be run entirely on a local machine; no cloud resources required.

---

## 🧩 System Architecture

```
                ┌───────────────────┐
                │     Streamlit     │
                │   (Client UI)     │
                └────────┬──────────┘
                         │ REST API calls (HTTP)
                ┌────────┴──────────┐
                │     FastAPI       │
                │   (Backend API)   │
                ├────────┬──────────┤
                │  RAG Pipeline     │
                │  (Retriever + LLM)│
                └────────┴──────────┘
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/neet-rag-helper.git
cd neet-rag-helper
```

### 2. Add Environment Variables

Create a `.env` file in the root directory and add your OpenAI key:

```env
OPENAI_API_KEY="your-api-key"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the **Server (FastAPI)**

```bash
python server.py
```

This will start the FastAPI backend on a local port (default: `http://127.0.0.1:8000`).

### 5. Run the **Client (Streamlit UI)**

```bash
streamlit run client.py
```

The Streamlit app will automatically connect to the FastAPI server via REST API endpoints.

---

## 🛠 Tech Stack

| Layer          | Technology      | Description                                      |
| -------------- | --------------- | ------------------------------------------------ |
| **Frontend**   | Streamlit       | Interactive local web UI for queries and display |
| **Backend**    | FastAPI         | API server for retrieval and generation          |
| **Core Logic** | LangChain + RAG | Document retrieval and language model generation |
| **LLM API**    | OpenAI API      | Used for context-aware responses                 |
| **Language**   | Python          | Primary development language                     |

---

## 📌 Notes

* Ensure **Python 3.8+** is installed.
* If you encounter dependency issues, create a new virtual environment before installing requirements.
* Both backend (`server.py`) and frontend (`client.py`) must be running simultaneously for full functionality.

---
