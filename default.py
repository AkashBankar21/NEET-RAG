from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain.retrievers import MultiQueryRetriever
from langchain.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
import pickle


def load_vector_store():
    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory="my_books_db",
        collection_name="sample",
    )
    return vector_store


def set_retriever(vector_store, k):
    with open("data.pkl", "rb") as f:  # open file in binary read mode
        docs = pickle.load(f, encoding="utf-8")

    bm25_retriever = BM25Retriever.from_documents(docs)  # keyword-based
    bm25_retriever.k = 5

    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5],
    )

    return retriever


def set_chatbot(model, temperature):
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm


def set_parser():
    parser = StrOutputParser()
    return parser


def create_prompt():
    prompt = PromptTemplate(
        template="""
      You are a helpful teacher.
      Use the help of context to answer the question.
      If the context is not exactly insufficient (can come in NEET paper), answer with your knowledge. but if the context is entirely insufficient
      (cannot come in NEET paper),
      then say 'out of syallbus'.
      after your answer, also give the source and page label of the context, which is used.

      {context}
      Question: {question}
    """,
        input_variables=["context", "question"],
    )
    return prompt


def format_docs(retrieved_docs):
    context_text = "\n\n".join(
        doc.page_content
        + " \nsource : "
        + doc.metadata["source"]
        + " \npage number : "
        + str(doc.metadata["page"])
        for doc in retrieved_docs
    )
    return context_text


def set_chain(retriever, prompt, llm, parser):
    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )
    main_chain = parallel_chain | prompt | llm | parser
    return main_chain


def generation(chain, query):
    answer = chain.invoke(query)
    return answer


def load_app(chain):
    st.title("NEET Helper")
    st.divider()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages
    for role, text in st.session_state.messages:
        st.chat_message(role).write(text)

    # Input box for new message
    if query := st.chat_input("What do you need help with?"):
        # Save user message
        st.session_state.messages.append(("user", query))
        st.chat_message("user").write(query)

        # Generate assistant reply
        answer = generation(chain, query)
        answer = f"Echo: {answer}"
        st.session_state.messages.append(("assistant", answer))
        st.chat_message("assistant").write(answer)
        st.badge("Success", icon=":material/check:", color="green")


def main():
    k = 5
    model = "gpt-4o-mini"
    temperature = 0.2
    load_dotenv()
    vector_store = load_vector_store()
    retriever = set_retriever(vector_store, k)
    llm = set_chatbot(model, temperature)
    prompt = create_prompt()
    parser = set_parser()
    chain = set_chain(retriever, prompt, llm, parser)
    load_app(chain)


if __name__ == "__main__":
    main()
