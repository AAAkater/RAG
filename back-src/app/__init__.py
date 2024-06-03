import os
import sys
from pprint import pprint

# 获取当前文件所在的目录路径
package_path = os.path.dirname(os.path.realpath(__file__))

# 将包路径添加到 sys.path
sys.path.append(package_path)


# pprint(sys.path)
