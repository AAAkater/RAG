import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# 存放图像的文件夹的路径
imgs_directory = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "imgs")


# 图片路径列表
image_paths = [
    os.path.join(imgs_directory, "cry.png"),
    os.path.join(imgs_directory, "cry2.png"),
    os.path.join(imgs_directory, "cry3.png"),
    os.path.join(imgs_directory, "ye.png"),
]

# 创建子图
fig, axes = plt.subplots(nrows=2, ncols=2)

# 加载并显示每个图片
for i, path in enumerate(image_paths):
    img = mpimg.imread(path)
    row = i // 2  # 计算行索引
    col = i % 2  # 计算列索引
    axes[row, col].imshow(img)
    axes[row, col].axis("off")  # 可选：关闭坐标轴

# 调整子图布局
plt.tight_layout()

# 显示窗口
plt.show()
