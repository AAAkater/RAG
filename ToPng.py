import sys
from PIL import Image
import os

# 指定图像文件所在的目录
directory = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'imgs')

# 获取目录中所有文件的列表
file_list = os.listdir(directory)

# 遍历目录中的文件
for file_name in file_list:
    # 获取文件的完整路径
    file_path = os.path.join(directory, file_name)

    # 检查文件是否为图像文件
    if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.gif', '.bmp', 'webp')):
        # 打开图像文件
        image = Image.open(file_path)

        # 将图像转换为PNG格式
        png_file_path = os.path.splitext(file_path)[0] + '.png'
        image.save(png_file_path, 'PNG')
        # 关闭图像文件
        image.close()

        os.remove(file_path)

        print(f"转换成功并删除原始图像: {file_name} -> {os.path.basename(png_file_path)}")
