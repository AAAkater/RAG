# 基于多模态大模型读取图像内容构建文本描述库用于检索

![alt text](image.png)

## 1.环境配置

docker配置

```bash
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start #启动docker
bash standalone_embed.sh stop #关闭
```

后端配置

```bash
cd RAG
pip install -r requirements.txt
uvicorn main:app --reload #运行
```

前端配置

```bash
cd front-src
pnpm install
pnpm dev #运行
```
