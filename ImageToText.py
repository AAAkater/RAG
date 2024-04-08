import datetime
import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image


# 初始化MLLM模型
model_id = "vikhyatk/moondream2"
revision = "2024-04-02"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)


# 存放图像的文件夹的路径
folder_path = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), 'imgs')
# 存放图像摘要的文件夹的路径
docs_directory = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), 'docs')

# 遍历imgs文件夹下的所有图片
i = 0
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', ".webp")):
        try:
            image = Image.open(file_path)
            enc_image = model.encode_image(image)
            print(f"图像({i}) -{filename=}")
            i += 1
            # 询问图像摘要
            question = "Generate a summary of this image"
            answer = model.answer_question(enc_image, question, tokenizer)
            # 写入摘要
            txt_file_path = os.path.join(
                docs_directory, f"{os.path.splitext(filename)[0]}.txt")
            with open(txt_file_path, 'w', encoding="utf-8") as file:
                file.write(answer)
            image.close()
        except Exception as e:
            print(f"无法处理图像({i}) - {filename =}")
            print(f"{file_path =}")
            print(e)
        print("-"*10)
