from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


class gpt3:
    def __init__(self, db_retriever) -> None:

        self.llm = ChatOpenAI(
            temperature=0,
            # openai_api_base="https://api.nextapi.fun/v1",
            # openai_api_key="ak-wByeadNm0Hxt6M6VaHBBYusiYPaQYDEYZzlybBzBSU7xJysf",
        )
        self.qa_chain = load_qa_with_sources_chain(
            llm=self.llm,
            chain_type="stuff",
            retriever=db_retriever,
            return_source_documents=True,
        )

    def invoke(self, input):
        prompt1: str = f"How many {input} are there?"
        prompt2: str = f"give me some information about the {input}"
        return self.qa_chain.invoke(prompt2)


if __name__ == "__main__":
    llm = ChatOpenAI(
        temperature=0,
        openai_api_base="https://api.nextapi.fun/v1",
        openai_api_key="ak-wByeadNm0Hxt6M6VaHBBYusiYPaQYDEYZzlybBzBSU7xJysf",
    )
    answer = llm.invoke("你好")
    print(answer)