import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

from langchain_core.vectorstores import VectorStoreRetriever
from src.LLM.Gpt3 import Gpt3
from src.Storage.Milvus import Milvus
from langchain_community.docstore.document import Document

retriever: VectorStoreRetriever = Milvus().as_retriever
llm = Gpt3(db_retriever=retriever)
app = FastAPI()
test = {
    "input": "hello",
    "chat_history": [],
    "context": [
        Document(
            page_content='The image shows a close-up view of a traffic light mounted on a wall. The traffic light is composed of three distinct lights: a red light at the top, a yellow light in the middle, and a green light at the bottom. The red light is positioned on the left side, the yellow light is in the middle, and the green light is on the right side. The traffic light is set against a white background, and the text "福" is visible, which appears to be a foreign language.',
            metadata={
                "id": "5b877e2933bc550c5b871e6119c6f22c8427d2d2761b5b72aa2bbe3c67df4051"
            },
        ),
        Document(
            page_content="The image presents a vibrant assortment of fruits, including a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of grapes, a pineapple, a bunch of",
            metadata={
                "id": "954da5c69fdeaa8d4a1691e1413757ecfde5ab5a0cfa003da3dbfa2944a26f21"
            },
        ),
        Document(
            page_content="The image features a young girl with blue eyes and blonde hair, dressed in a blue dress and a white hat. She is holding a bouquet of flowers in her hands, and there are blue butterflies fluttering around her. The background is a light blue color, with pink and white flowers scattered throughout, creating a serene and whimsical atmosphere.",
            metadata={
                "id": "2b5f7308e043e3605c90c83f851d900d63a38b6641ca77733eec4f2376cb17b6"
            },
        ),
        Document(
            page_content='The image depicts a breathtaking mountain range with snow-capped peaks and a deep blue lake in the foreground. The mountains, with their varying heights and shapes, create a stunning backdrop for the lake. The sky above is a light blue, dotted with clouds, adding to the overall beauty of the scene. The image is taken from a high vantage point, providing a comprehensive view of the landscape. The text "日本語" is visible, which may indicate the language of the image or the photographer.',
            metadata={
                "id": "2c467b63377395fcc01f84567296b67146e7e5dfebb682127f40af3dd81a734d"
            },
        ),
        Document(
            page_content="A hand is holding a pink and white ice cream cone with a scoop of vanilla ice cream and a dollop of whipped cream. The ice cream is topped with a pink and white marshmallow. The hand is positioned in front of a blurred green field, suggesting a peaceful outdoor setting.",
            metadata={
                "id": "d8ad22fbfa5cadeb0c40c92c959c17189ba9be9d475bc8f6174f1fb58ceec2ba"
            },
        ),
    ],
    "answer": "Hello! How can I assist you today?",
}


@app.get("/query")
def get_answer(desc: str):
    result = llm.invoke(input=desc)
    answer = result["answer"]
    image_ids: list[str] = [doc.metadata["id"] for doc in result["context"]]
    data = {"answer": answer, "ids": image_ids}
    return JSONResponse(content=data)


@app.get("/image")
def get_image(id: str):
    image_folder = "./images/"
    image_filename = f"{id}.jpg"
    image_path = f"{image_folder}{image_filename}"

    if os.path.isfile(image_path) == False:
        return {"message": "Image not found."}

    return FileResponse(image_path, media_type="image/jpeg")


@app.post("/clear")
def clear_context() -> JSONResponse:
    llm.clear_history()
    data: dict[str, str] = {"message": "上下文已清除"}
    return JSONResponse(content=data)
