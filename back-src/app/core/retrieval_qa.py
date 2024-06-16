from pprint import pp
from typing import Any, Dict, List

from app.core.crud import database
from app.utils.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.docstore.document import Document
from langchain_community.vectorstores.milvus import Milvus
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables.base import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


class Retrieval:
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    def __init__(self, db_retriever) -> None:
        self._llm = ChatOpenAI(temperature=0)
        self.chat_history = {}

        # 检索模板
        self.history_aware_retriever: Runnable[Any, List[Document]] = (
            create_history_aware_retriever(
                llm=self._llm,
                retriever=db_retriever,
                prompt=ChatPromptTemplate.from_messages(
                    messages=[
                        SystemMessagePromptTemplate.from_template(
                            template=self.contextualize_q_system_prompt
                        ),
                        MessagesPlaceholder(variable_name="chat_history"),
                        HumanMessagePromptTemplate.from_template(template="{input}"),
                    ]
                ),
            )
        )
        # 对话模板
        self.document_chain: Runnable[Dict[str, Any], Any] = (
            create_stuff_documents_chain(
                llm=self._llm,
                prompt=ChatPromptTemplate.from_messages(
                    messages=[
                        SystemMessagePromptTemplate.from_template(
                            template=self.qa_system_prompt
                        ),
                        MessagesPlaceholder(variable_name="chat_history"),
                        HumanMessagePromptTemplate.from_template(template="{input}"),
                    ]
                ),
            )
        )
        # 构建RAG对话链
        self.rag_chain = create_retrieval_chain(
            retriever=self.history_aware_retriever,
            combine_docs_chain=self.document_chain,
        )

        # 引入聊天历史
        self.conversational_rag_chain = RunnableWithMessageHistory(
            runnable=self.rag_chain,
            get_session_history=self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def invoke(self, input: str):
        result = self.conversational_rag_chain.invoke(
            {"input": input}, config={"configurable": {"session_id": "test"}}
        )
        return result

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.chat_history:
            self.chat_history[session_id] = InMemoryHistory()
        return self.chat_history[session_id]

    def clear_history(self):
        """清空历史记录"""
        self.chat_history.clear()


retrieval = Retrieval(db_retriever=database.as_retriever)


if __name__ == "__main__":

    # res = retrieval.invoke("What are the yellow flowers?")
    # print(res)
    images_collection = Milvus(
        embedding_function=Embedding(),
        collection_name="audio",
        connection_args={
            "host": "localhost",
            "port": "19530",
        },
        primary_field="id",
        text_field="desc",
        vector_field="desc_vec",
    )
    retriever = images_collection.as_retriever(
        search_type="mmr", search_kwargs={"k": 5}
    )

    retrieval = Retrieval(retriever)
    res = retrieval.invoke("How GPS works")

    # pp(res)

    for doc in res["context"]:
        pp(doc.metadata["metadata"])
