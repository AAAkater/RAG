

import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import chroma
embedding = OpenAIEmbeddings()

sents = [
    '我喜欢小狗',
    "我喜欢小动物",
    "心情很差"
]

embs = []
for sent in sents:
    embs.append(embedding.embed_query(sent))

print(np.dot(embs[2], embs[1]))

print(embs[0])
