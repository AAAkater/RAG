import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()


@app.get("/query")
def get_answer(desc: str):
    image_ids: list[str] = ["12", "afssas", "gssc"]
    answer = "这是回答"

    data = {"answer": answer, "ids": image_ids}
    return JSONResponse(content=data)


@app.get("/image")
def get_image(image_id: str):
    image_folder = "./images/"
    image_filename = f"{image_id}.jpg"
    image_path = f"{image_folder}{image_filename}"

    if os.path.isfile(image_path) == False:
        return {"message": "Image not found."}

    return FileResponse(image_path, media_type="image/jpeg")
