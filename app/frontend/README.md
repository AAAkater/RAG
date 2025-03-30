# 多模态RAG前端

## 1.运行

```bash
cd font-src # 切入工作目录
pnpm install # 下载依赖
pnpm dev # 运行
```

## 2.GIT规范

基于develop分支创建feature/branch-name分支

```bash
git checkout -b feature/branch-name develop
```

合并自己的功能分支到develop分支

```bash
git checkout develop #切换到develop分支
git merge feature/branch-name #合并分支
```

!!! 注意
    请不要对master分支进行任何合并或者提交操作
