from pprint import pp
from typing import List, Tuple

from app.utils.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from langchain_community.vectorstores.milvus import Milvus
from langchain_core.documents.base import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStoreRetriever

# embedding_function = Embedding()


class Retriever(VectorStoreRetriever):

    def __init__(self, table_names: List[str]):
        self.embedding_function = Embedding()
        self.table_names: list[str] = table_names
        self.top_k = 5
        self.stores = [
            Milvus(
                embedding_function=self.embedding_function,
                collection_name=table_name,
                connection_args={
                    "host": "localhost",
                    "port": "19530",
                },
                primary_field="id",
                text_field="desc",
                vector_field="desc_vec",
                metadata_field="metadata",
            )
            for table_name in table_names
        ]

    def _get_relevant_documents(self, query: str):
        query_vector = self.embedding_function.embed_query(query)
        results = []
        for store in self.stores:
            result: List[Tuple[Document, float]] = (
                store.similarity_search_with_score_by_vector(
                    embedding=query_vector, k=self.top_k
                )
            )
            results.extend(result)
        results.sort(key=lambda x: x[1])
        return results[: self.top_k]

    def as_retriever(self):
        def retriever_function(query):
            documents = []
            results: List[Tuple[Document, float]] = self._get_relevant_documents(query)
            for result, distance in results:
                doc = Document(
                    page_content=result.metadata.get("content", ""),
                    metadata={"id": result.id, "distance": distance, **result.metadata},
                )
                documents.append(doc)
            return documents

        return retriever_function

    # def as_retriever(self):
    #     images_collection = Milvus(
    #         embedding_function=self.__embedding_model,
    #         collection_name=self.collection_names[0],
    #         connection_args={"uri": self.uri},
    #         primary_field="id",
    #         text_field="desc",
    #         vector_field="desc_vec",
    #     )
    #     return images_collection.as_retriever(search_type="mmr", search_kwargs={"k": 5})


if __name__ == "__main__":

    # images_collection = Milvus(
    #     embedding_function=Embedding(),
    #     collection_name="image",
    #     connection_args={
    #         "host": "localhost",
    #         "port": "19530",
    #     },
    #     primary_field="id",
    #     text_field="desc",
    #     vector_field="desc_vec",
    # )

    # res = images_collection.similarity_search("flowers")

    # pp(res)

    retriever = Retriever(table_names=["image", "document", "audio", "video"])

    res = retriever._get_relevant_documents("flower")

    pp(res)
