from typing import Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image


# 选择MLLM模型
class Moondream:
    _model_id = "vikhyatk/moondream2"  # 模型id
    _revision = "2024-04-02"  # 模型版本
    _model: Any = None  # 模型
    _tokenizer: Any = None  # 分词器
    prompt: str = "Descirbe this image: "

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
            raise RuntimeError(f"MLLM 初始化失败：{e}")

    def answer(self, image_path: str) -> str:
        """输入图片让MLLM返回相关消息

        Args:
            image_path (str): 图片路径

        Returns:
            str: 返回图像描述
        """

        image = self._model.encode_image(Image.open(fp=image_path))
        answer = self._model.answer_question(
            image, self.prompt, self._tokenizer)

        return answer


if __name__ == "__main__":
    """
    测试
    """
    try:
        mllm = Moondream()
        print(mllm.answer(r"River-Village-in-a-Rainstorm.jpg"))
    except RuntimeError as e:
        print(e)
