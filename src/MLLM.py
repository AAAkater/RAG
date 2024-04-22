from typing import Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.docstore.document import Document
from PIL import Image


# 选择MLLM模型
class moondream:
    _model_id = "vikhyatk/moondream2"  # 模型id
    _revision = "2024-04-02"  # 模型版本
    _model: Any = None  # 模型
    _tokenizer: Any = None  # 分词器
    prompt: str = "Generate a summary of this image"

    def __init__(self):
        try:
            self._model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self._model_id,
                trust_remote_code=True,
                revision=self._revision,
                torch_dtype=torch.float16,
            ).to("cuda")
            self._tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=self._model_id, revision=self._revision
            )
        except Exception as e:
            raise RuntimeError(f"MLLM初始化失败:{e}")

    def answer(self, image_path: str) -> Document:
        """输入图片让MLLM返回相关消息

        Args:
            image_path (str): 图片路径

        Returns:
            Document: 返回文档
        """

        image = self._model.encode_image(Image.open(fp=image_path))
        answer = self._model.answer_question(image, self.prompt, self._tokenizer)
        doc = Document(page_content=answer, metadata={"image_path": image_path})
        return doc

    def answer_print(self, image_path: str):
        """输入图片让MLLM返回相关消息并打印

        Args:
            image_path (str): 图片路径
        """
        image = self._model.encode_image(Image.open(fp=image_path))
        answer = self._model.answer_question(image, self.prompt, self._tokenizer)
        print(f"{image_path=}")
        print(f"query:{self.prompt}", end="\n\n")
        print(f"answer:{answer}")


if __name__ == "__main__":
    """
    测试
    """
    try:
        mllm = moondream()
    except RuntimeError as e:
        print(e)
    else:
        print(f"MLLM初始化成功")
        mllm.answer_print(image_path="./imgs/girls/angry.png")
