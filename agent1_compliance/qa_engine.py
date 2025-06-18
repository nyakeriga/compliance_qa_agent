# agent1_compliance/qa_engine.py

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
import os

def answer_question(question):
    documents_path = "media/documents"
    loader = DirectoryLoader(documents_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(docs, embeddings)

    retriever = vector_store.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), retriever=retriever)

    result = qa.run(question)
    return result

