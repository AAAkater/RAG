import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# from langchain_community.chains import RetrievalQA

vecdb_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "vecdb"
)


# 连接数据库
db = Chroma(persist_directory=vecdb_directory, embedding_function=OpenAIEmbeddings())

print(db._collection.count())
question = "Is there any content about girls?"

# docs = db.similarity_search(question, k=3)
# print(len(docs))
# for doc in docs:
#     print(doc.page_content)


llm = ChatOpenAI(temperature=0)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(),
    return_source_documents=True,
)


ans = qa.invoke(question)
print(ans["query"])
print(ans["result"])

for doc in ans["source_documents"]:
    print(f"{doc.metadata}")
