import os
import sys
import matplotlib.pyplot as plt

# 图片文件夹路径
image_folder: str = "/Users/yangming/code/python/RAG/imgs"

# 获取图片文件列表
image_paths: list[str] = [
    os.path.join(image_folder, filename)
    for filename in os.listdir(image_folder)
    if filename.endswith((".jpg", ".jpeg", ".png"))
]

num_images = len(image_paths)
num_rows = (num_images - 1) // 5 + 1
num_cols = min(num_images, 5)

# 创建子图
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))

for i, ax in enumerate(axes.flatten()):
    if i < num_images:
        # 读取图片
        image = plt.imread(image_paths[i])

        # 显示图片
        ax.imshow(image)
        ax.axis("off")
    else:
        # 隐藏多余的子图
        ax.axis("off")

# 调整子图间距
plt.tight_layout()

# 显示图像
plt.show()
