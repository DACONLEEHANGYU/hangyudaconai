from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field
from typing import List, Any
import threading

class MultiRetriever(BaseRetriever):
    vector_stores: List[VectorStore] = Field(default_factory=list)

    def __init__(self, vector_stores: List[VectorStore], **kwargs: Any):
        super().__init__(**kwargs)
        self.vector_stores = vector_stores

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
        results = []
        threads = []
        lock = threading.Lock()

        def retrieve(vector_store):
            docs, scores = zip(
                *vector_store.similarity_search_with_score(query, k=4)
            )
            for doc, score in zip(docs, scores):
                doc.metadata["score"] = score

            with lock:
                results.extend(docs)

        for vector_store in self.vector_stores:
            thread = threading.Thread(target=retrieve, args=(vector_store,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sorted(results, key=lambda x: x.metadata['score'])[:4]

    async def _aget_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
        # Optional: Implement async version if necessary
        raise NotImplementedError("Async retrieval not implemented for MultiRetriever")
