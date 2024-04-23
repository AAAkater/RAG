import os
import hashlib
from PIL import Image
import glob


def convert_to_jpg(image_path):
    if not image_path.lower().endswith('.jpg'):
        img = Image.open(image_path)
        rgb_img = img.convert('RGB')
        new_path = image_path.rsplit('.', 1)[0] + '.jpg'
        rgb_img.save(new_path)
        os.remove(image_path)
        return new_path
    else:
        return image_path


def rename_to_sha256(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
    new_file_path = os.path.join(
        os.path.dirname(file_path), readable_hash + '.jpg')
    os.rename(file_path, new_file_path)


def prepare(directory):
    for image_path in glob.glob(directory + '/**/*.*', recursive=True):
        jpg_image_path = convert_to_jpg(image_path)
        rename_to_sha256(jpg_image_path)
