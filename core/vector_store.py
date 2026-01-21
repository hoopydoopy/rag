from typing import List, Dict
import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self._data: List[Dict] = []

    def add(self, embedded_chunks: List[Dict]) -> None:
        vectors = np.array(
            [c["embedding"] for c in embedded_chunks],
            dtype="float32",
        )

        self.index.add(vectors)
        self._data.extend(embedded_chunks)

    def search(self, query_embedding: List[float], k: int = 5) -> List[Dict]:
        query = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query, k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self._data[idx])

        return results

    def __len__(self) -> int:
        return len(self._data)
