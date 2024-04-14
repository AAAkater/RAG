import os
from typing import Any, List
import chromadb
from chromadb.api import ClientAPI
from langchain_community.vectorstores import Chroma
from langchain_community.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


class vecdb:
    path: str = os.path.abspath(path="./database/")
    client: ClientAPI = chromadb.PersistentClient(path)
    collection_name: str = "langchain"

    def __init__(self, collection_name: str) -> None:
        self.collection = self.client.get_or_create_collection(collection_name)

    def select(self) -> None:
        print(f"行数:{self.collection.count()}")
        table = self.collection.get(include=["documents", "metadatas"])
        ids: List[str] = table["ids"]
        metadatas: Any = table["metadatas"]
        documents: Any = table["documents"]
        i = 1
        for id, metadata, document in zip(ids, metadatas, documents):
            print(f"序号:{i}")
            print(f"{id=}")
            print(f"{metadata['image_path']=}")
            print(f"{document=}")
            print()
            i += 1

    def drop_table(self):
        self.client.delete_collection(self.collection_name)

    def add(self, doc: Document):
        text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=5)

        splits: List[Document] = text_splitter.split_documents(documents=[doc])
        try:
            vectordb = Chroma.from_documents(
                documents=splits,
                embedding=OpenAIEmbeddings(),
                persist_directory=self.path,
            )
            # 保存到本地
            vectordb.persist()
        except Exception as e:
            print("载入数据库失败")
            print(e)

    def similarity_search(self, query: str):
        db = Chroma(
            embedding_function=OpenAIEmbeddings(),
            persist_directory=self.path,
        )
        return db.similarity_search(query)

    @staticmethod
    def retriever(vecdb_path: str):
        db = Chroma(
            embedding_function=OpenAIEmbeddings(),
            persist_directory=vecdb_path,
        )
        return db.as_retriever(search_type="mmr", search_kwargs={"k": 10})


if __name__ == "__main__":
    # print(vecdb.path)
    print(vecdb.path)

    # doc = Document(
    #     page_content="xyz",
    #     metadata={"image_path": "F:\\Desktop\\vsc\\python\\RAG\\imgs\\bkg.png"},
    # )
    collection = vecdb(collection_name="langchain")
    # collection.add(doc)
    # collection.select()
    ans = collection.similarity_search(
        "give me some information about the traffic light"
    )

    print(len(ans))
    print(ans)
