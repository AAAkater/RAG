from PIL import Image
import os


def to_png(images_path):

    directory = images_path

    file_list = os.listdir(images_path)
    # 遍历目录中的文件
    for file_name in file_list:
        file_path = os.path.join(images_path, file_name)

        # 检查文件是否为图像文件
        if os.path.isfile(file_path) and file_name.lower().endswith(
            (".jpg", ".jpeg", ".gif", ".bmp", "webp")
        ):

            image = Image.open(file_path)

            # 将图像转换为PNG格式
            png_file_path = os.path.splitext(file_path)[0] + ".png"
            image.save(png_file_path, "PNG")
            # 关闭图像文件
            image.close()

            os.remove(file_path)

            print(
                f"转换成功并删除原始图像: {file_name} -> {os.path.basename(png_file_path)}"
            )


if __name__ == "__main__":
    path = "./imgs/"
    to_png(path)
