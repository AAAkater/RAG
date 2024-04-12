from transformers import AutoModelForCausalLM, AutoTokenizer

# 选择MLLM模型
_model_id = "vikhyatk/moondream2"
_revision = "2024-04-02"

try:
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=_model_id,
        trust_remote_code=True,
        revision=_revision,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=_model_id, revision=_revision
    )
except Exception as e:
    print("连接MLLM失败 网络不稳定")
    print(e)
else:
    print("连接MLLM成功")
