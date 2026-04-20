import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

from config import *
from evaluator import evaluate_response

def load_vector_store():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    return vectordb


def retrieve_chunks(vectordb, query):
    results = vectordb.similarity_search(query, k=TOP_K)
    return results


def generate_answer(question, docs):
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template("""
Eres un asistente de recursos humanos. Responde SOLO con la información del contexto siguiente.
Si el contexto no basta para responder con seguridad, dilo con claridad.

Contexto:
{context}

Pregunta:
{question}
""")

    llm = ChatOpenAI(model=CHAT_MODEL)

    response = llm.invoke(
        prompt.format_messages(context=context, question=question)
    )

    return response.content


def run_query(question):
    vectordb = load_vector_store()

    docs = retrieve_chunks(vectordb, question)
    answer = generate_answer(question, docs)

    result = {
        "pregunta_usuario": question,
        "respuesta_sistema": answer,
        "fragmentos_relacionados": [doc.page_content for doc in docs],
    }

    return result


if __name__ == "__main__":
    q = input("Escribe tu pregunta: ")
    res = run_query(q)

    print(json.dumps(res, indent=2, ensure_ascii=False))
    
    #ev = evaluate_response(q, res["respuesta_sistema"], res["fragmentos_relacionados"])
    #print(f"Evaluación: {ev['puntuacion']} - {ev['motivo']}")