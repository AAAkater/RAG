import math
from typing import Any, Dict, List

import matplotlib.pyplot as plt
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.docstore.document import Document
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


class Gpt3:
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is.\
    """

    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\
    chat history:\
    {context}
    """

    def __init__(self, db_retriever) -> None:
        self.llm = ChatOpenAI(temperature=0)
        self.chat_history = {}

        # 检索模板
        self.history_aware_retriever: Runnable[Any, List[Document]] = (
            create_history_aware_retriever(
                llm=self.llm,
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
                llm=self.llm,
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
        self.chat_history.clear()

    def show_images(self, result: dict[str, list[Document]]):
        """显示被检索到的图片

        Args:
            result (dict[str, list[Document]]): LLM返回的信息
        """
        num_images = len(result["source_documents"])
        num_rows = math.ceil(num_images / 5)
        num_cols = min(num_images, 5)

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 3 * num_rows))

        for i, doc in enumerate(result["source_documents"]):
            image_path = f"./imgs/{doc.metadata['id']}.jpg"
            if num_rows == 1:
                ax = axes[i % num_cols]  # 获取当前子图对象（一行情况）
            else:
                ax = axes[i // num_cols, i % num_cols]
            image = plt.imread(image_path)
            ax.imshow(image)
            ax.axis("off")

        if num_images < num_rows * num_cols:
            for j in range(num_images, num_rows * num_cols):
                if num_rows == 1:
                    fig.delaxes(axes[j])
                else:
                    fig.delaxes(axes[j // num_cols, j % num_cols])

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    llm = ChatOpenAI(temperature=0)
    answer = llm.invoke("你好")
    print(answer)
