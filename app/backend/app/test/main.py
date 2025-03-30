from pprint import pp

from app.utils.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)


file_path = r"F:\Desktop\vsc\python\RAG\back-src\app\metadata\document\baichuan.pdf"
loader = PyPDFLoader(file_path)
pages = loader.load_and_split(text_splitter)

pp(len(pages))


# for i, page in enumerate(pages):
#     if i == 10:
#         break
#     pp(page.page_content)


Embedding_model = Embedding()
embeddings = Embedding_model.embed_document([page.page_content for page in pages[0:10]])

for embedding in embeddings:
    print(len(embedding))
