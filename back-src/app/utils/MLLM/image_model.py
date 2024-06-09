from typing import Any

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer


# 选择MLLM模型
class Moondream:
    model_id = "vikhyatk/moondream2"  # 模型id
    revision = "2024-04-02"  # 模型版本
    prompt: str = "Describe this image: "

    def __init__(self):
        try:
            self.__model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=self.model_id,
                trust_remote_code=True,
                revision=self.revision,
                torch_dtype=torch.float16,
            ).to("cuda")
            self.__tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=self.model_id, revision=self.revision
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

        image = self.__model.encode_image(Image.open(fp=image_path))
        answer = self.__model.answer_question(image, self.prompt, self.__tokenizer)

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
