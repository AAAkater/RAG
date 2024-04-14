from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA


class LLM_model:
    def __init__(self, db_retriever) -> None:
        self.llm = ChatOpenAI(temperature=0)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=db_retriever,
            return_source_documents=True,
        )

    def invoke(self, input):
        return self.qa_chain.invoke(f"give me some information about the {input}")
