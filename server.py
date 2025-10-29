# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from dotenv import load_dotenv
from books import books
import pickle
import uvicorn

app = FastAPI()

load_dotenv()

# ----- LangChain Setup -----
def load_vector_store():
    return Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory="my_books_db",
        collection_name="sample",
    )

def set_retriever(vector_store, k):
    with open("data.pkl", "rb") as f:
        docs = pickle.load(f, encoding="utf-8")
    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = k
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return EnsembleRetriever(retrievers=[bm25, vector_retriever], weights=[0.5, 0.5])

def create_prompt():
    return PromptTemplate(
        template="""
        You are a helpful teacher.
        Use the help of context to answer the question.
        If the context is not exactly insufficient (can come in NEET paper), answer with your knowledge.
        If the context is entirely insufficient (cannot come in NEET paper), say 'out of syllabus'.
        After your answer, also give the source and page label of the context used (most similar one).
        End your answer with three related previous NEET questions that have come previously and ask if the student needs answer for them.
        {context}
        Question: {question}
        """,
        input_variables=["context", "question"],
    )

def retrieve_book(doc):
    codename = doc.metadata['source']
    try:
        chapter = int(codename[-6:-4])
    except:
        chapter = 1  # default if conversion fails

    # Determine which book we're dealing with
    if codename[2:6] == 'kebo':
        key = 'kebo'
    elif codename[2:6] == 'lebo':
        key = 'lebo'
    else:
        key = codename[2:7]

    # Safe fallback for invalid or out-of-range chapter index
    chapters = books[key]['chapters']
    if not isinstance(chapter, int) or chapter >= len(chapters) or chapter < 0:
        chapter = 0 if len(chapters) > 0 else 0

    bookname = books[key]['name'] + ' ' + chapters[chapter]
    return bookname

def format_docs(retrieved_docs):
    return "\n\n".join(
        f"{doc.page_content}\nsource: {retrieve_book(doc)}\npage: {doc.metadata['page']}"
        for doc in retrieved_docs
    )

# ---- Initialization ----
k = 5
model = "gpt-4o-mini"
temperature = 0.2

vector_store = load_vector_store()
retriever = set_retriever(vector_store, k)
llm = ChatOpenAI(model=model, temperature=temperature)
prompt = create_prompt()
parser = StrOutputParser()

chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough(),
}) | prompt | llm | parser


# ---- Request Model ----
class QueryRequest(BaseModel):
    query: str


# ---- API Endpoint ----
@app.post("/ask")
def ask(request: QueryRequest):
    response = chain.invoke(request.query)
    return {"answer": response}


# ---- Run the Server ----
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
