import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers.pipelines.base import Pipeline


class WhisperLargeV3:
    model_id = "openai/whisper-large-v3"

    def __init__(self) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.__model = AutoModelForSpeechSeq2Seq.from_pretrained(
            pretrained_model_name_or_path=self.model_id,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        ).to(device)
        self.__processor = AutoProcessor.from_pretrained(
            pretrained_model_name_or_path=self.model_id
        )
        self.pipe: Pipeline = pipeline(
            task="automatic-speech-recognition",
            model=self.__model,
            tokenizer=self.__processor.tokenizer,
            feature_extractor=self.__processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

    def answer(self, audio_path: str) -> str:
        """输入音频让MLLM返回相关消息,限英文

        Args:
            audio_path (str): 音频路径

        Returns:
            str: 返回图像描述
        """
        result = self.pipe(
            audio_path,
            # return_timestamps=True,
            generate_kwargs={"language": "english"},
        )
        return result["text"]


def test_main(path: str):
    mllm = WhisperLargeV3()
    res = mllm.answer(path)
    print(res)


if __name__ == "__main__":
    test_main(r"F:\下载文件\sample1.flac")
