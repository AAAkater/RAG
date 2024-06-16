# 多模态RAG

## 仓库下载

```bash
git clone https://github.com/AAAkater/RAG.git
```

## docker配置

```bash
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start #启动docker
bash standalone_embed.sh stop #关闭
```

## 后端配置

```bash
cd back-src
pip install -r requirements.txt
uvicorn main:app --reload #运行
```

## 前端配置

```bash
cd front-src
pnpm install
pnpm dev #运行
```
