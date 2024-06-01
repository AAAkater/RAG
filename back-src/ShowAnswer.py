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

test2 = {
    "query": "Is there any content about girls?",
    "result": "Yes, all the provided images are about girls with different characteristics like hair color, eye color, and accessories like cat ears.",
    "source_documents": [
        Document(
            page_content="A wine glass filled with red wine is tilted towards a wine bottle, with the wine flowing out of the bottle and into the glass.",
            metadata={
                "id": "1a026be95740d9fa8b1f81e945f6dd965de516f4f3d015cacc7e84969fa45cb9"
            },
        ),
        Document(
            page_content="A wine glass filled with red wine is tilted towards a wine bottle, with the wine flowing out of the bottle and into the glass.",
            metadata={
                "id": "72016919176409f9e74c85914fce0df9baa053adc71cc985311420282c2673a7"
            },
        ),
        Document(
            page_content="A wine glass filled with red wine is tilted towards a wine bottle, with the wine flowing out of the bottle and into the glass.",
            metadata={
                "id": "f570b10a48caa3325089b1a817883af34a135f3306f1f6bcdd57fa43043cfd46"
            },
        ),
        Document(
            page_content="A wine glass filled with red wine is tilted towards a wine bottle, with the wine flowing out of the bottle and into the glass.",
            metadata={
                "id": "f2e24bc409507c23e37efaa062c7767d4b33bcd4722e8b4bdc96cf7f9e6334dd"
            },
        ),
    ],
}


def show(LLM_answer: dict[str, list[Document]]):

    print(f"query:{LLM_answer['query']}\n")
    print(f"result:{LLM_answer['result']}")
    num_images = len(LLM_answer["source_documents"])
    num_rows = math.ceil(num_images / 5)
    num_cols = min(num_images, 5)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 3 * num_rows))

    for i, doc in enumerate(LLM_answer["source_documents"]):

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

    show(LLM_answer=test2)
