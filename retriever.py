import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from embedder import embed_texts, embed_query

class HybridRetriever:
    def __init__(self, documents):
        self.docs = documents
        self.tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized)

        self.embeddings = embed_texts(documents)
        dim = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def search(self, query, k=5):

        bm25_scores = self.bm25.get_scores(query.split())
        bm25_top = np.argsort(bm25_scores)[::-1][:k]


        q_emb = embed_query(query)
        _, dense_top = self.index.search(np.array([q_emb]), k)

        dense_top = dense_top[0]


        combined = list(set(bm25_top.tolist() + dense_top.tolist()))

        results = [self.docs[i] for i in combined]
        return results