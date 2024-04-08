

from langchain_community.vectorstores import chroma
from langchain_openai import OpenAIEmbeddings


vecdb_path = 'F:\\Desktop\\vsc\\python\\RAG\\vecdb'


sent = "你好"

# vecdb = chroma.Chroma(
#     collection_name=sent,
#     embedding_function=OpenAIEmbeddings(),
#     persist_directory=vecdb_path
# )

# vecdb = chroma.Chroma(

# ).afrom_documents()
