import datetime
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "vikhyatk/moondream2"
revision = "2024-04-02"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)


folder_path = "F:\\Desktop\\vsc\\python\\RAG\\imgs"
i = 0
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', ".webp")):
        try:

            image = Image.open(file_path)

            enc_image = model.encode_image(image)
            print(f"序号={i} {filename=}")
            i += 1
            print(model.answer_question(
                enc_image, "Generate a summary of this image", tokenizer))
            print("-"*10)
            image.close()

        except Exception as e:
            print(f"无法处理文件: {file_path}")
            print(e)
# starttime = datetime.datetime.now()
# image = Image.open(
#     "RAG/imgs/cry2.jpg")
# enc_image = model.encode_image(image)
# print(model.answer_question(enc_image, "生成这个图像的摘要", tokenizer))
# endtime = datetime.datetime.now()
# print(f"耗时{endtime - starttime}秒").seconds
