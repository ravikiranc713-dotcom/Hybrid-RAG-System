from fastapi import FastAPI
from retriever import HybridRetriever
from reranker import rerank
from llm import generate_answer
from chunking import recursive_chunk

app = FastAPI()


with open("data/docs.txt") as f:
    raw_text = f.read()

chunks = recursive_chunk(raw_text)
retriever = HybridRetriever(chunks)

@app.get("/query")
def query(q: str):

    docs = retriever.search(q, k=8)

    top_docs = rerank(q, docs, top_k=3)

    context = "\n\n".join(top_docs)

    answer = generate_answer(q, context)

    return {
        "query": q,
        "answer": answer,
        "sources": top_docs
    }