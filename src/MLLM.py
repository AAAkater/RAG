from typing import Any
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.docstore.document import Document
from PIL import Image


# 选择MLLM模型
class MLLM_model:
    _model_id = "vikhyatk/moondream2"
    _revision = "2024-04-02"
    _model: Any = None
    _tokenizer: Any = None
    question: str = "Generate a summary of this image"

    def __init__(self):
        try:
            self._model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self._model_id,
                trust_remote_code=True,
                revision=self._revision,
            )
            self._tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=self._model_id, revision=self._revision
            )
        except Exception as e:
            print("连接MLLM失败 网络不稳定")
            print(e)
        else:
            print("连接MLLM成功")

    def answer(self, image_path: str) -> Document:
        """输入图片让MLLM返回相关消息

        Args:
            image_path (str): 图片路径

        Returns:
            Document: 返回文档
        """

        image = self._model.encode_image(Image.open(fp=image_path))
        answer = self._model.answer_question(image, self.question, self._tokenizer)
        doc = Document(page_content=answer, metadata={"image_path": image_path})
        return doc


if __name__ == "__main__":
    print(MLLM_model.question)
