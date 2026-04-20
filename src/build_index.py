from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from config import *

def load_document(path):
    loader = TextLoader(path, encoding="utf-8")
    documents = loader.load()
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    return vectordb


if __name__ == "__main__":
    docs = load_document(FAQ_DOCUMENT_PATH)
    chunks = chunk_documents(docs)

    print(f"Se generaron {len(chunks)} fragmentos")

    vectordb = build_vector_store(chunks)

    print(f"Base vectorial creada en {PERSIST_DIR} ({len(vectordb)} documentos)")