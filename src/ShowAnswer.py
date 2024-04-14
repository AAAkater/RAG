import math
import matplotlib.pyplot as plt
from langchain_community.docstore.document import Document


test = {
    "query": "Is there any content about girls?",
    "result": "Yes, all the provided images are about girls with different characteristics like hair color, eye color, and accessories like cat ears.",
    "source_documents": [
        Document(
            page_content="an image of a girl with long white hair and blue eyes [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/cry.png"},
        ),
        Document(
            page_content="an image of a girl with long blue hair and a white dress [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/bkg.png"},
        ),
        Document(
            page_content="an image of a girl with pink hair and a cat ears [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/miao.png"},
        ),
        Document(
            page_content="an image of a girl with long hair and a cat ears [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/angry.png"},
        ),
        Document(
            page_content="an image of a girl with long hair and a cat ears [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/cry.png"},
        ),
        Document(
            page_content="an image of a girl with long hair and a cat ears [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/cry2.png"},
        ),
        Document(
            page_content="an image of a girl with long hair and a cat ears [SEP]",
            metadata={"image_path": "/Users/yangming/code/python/RAG/imgs/cry3.png"},
        ),
    ],
}


def show(LLM_answer: dict[str, list[Document]]):

    print(f"query:{LLM_answer['query']}")
    print(f"result:{LLM_answer['result']}")
    num_images = len(LLM_answer["source_documents"])
    num_rows = math.ceil(num_images / 5)
    num_cols = min(num_images, 5)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 3 * num_rows))

    for i, doc in enumerate(LLM_answer["source_documents"]):

        image_path = doc.metadata["image_path"]
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

    show(LLM_answer=test)
