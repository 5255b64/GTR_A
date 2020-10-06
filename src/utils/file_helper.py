"""
文件、文件夹操作
"""
import os
import shutil

from src.utils import sub_call_hook, logger


def check_path_exists(path: str):
    """
    判断路径是否存在
    若不存在则生成对应路径
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def check_file_exists(addr: str):
    """
    判断文件是否存在
    若不存在则生成其上级路径
    # 并且生成空白文件
    :param addr:
    :return:
    """
    if not os.path.isfile(addr):
        if not os.path.isdir(addr):
            temp = addr.split("/")
            temp.remove(temp[-1])
            addr2 = "/".join(temp)
            if not os.path.isdir(addr2):
                os.makedirs(addr2)
            # 生成空白文件
            # with open(addr, 'w') as f:
            #     f.write("")
        else:
            raise Exception("已存在路径 无法创建文件：\t" + addr)


def getallfile(path):
    """
    获取子文件
    :param path:
    :return:
    """
    allfile = []
    allfilelist = os.listdir(path)
    for file in allfilelist:
        filepath = os.path.join(path, file)
        # 判断是不是文件夹
        if os.path.isdir(filepath):
            allfile.extend(getallfile(filepath))
        else:
            allfile.append(filepath)
    return allfile


def cp(src: str, dest: str):
    if not os.path.exists(src):
        logger.log_err("复制的源文件不存在:\t" + src)
        return False

    if os.path.exists(dest):
        logger.log_err("复制的目标文件已存在 不进行覆盖:\t" + dest)
        return False

    if os.path.isfile(src):
        check_file_exists(dest)
        shutil.copy(src, dest)
    else:
        # check_path_exists(dest)
        shutil.copytree(src, dest)
    return True


def rm(src: str):
    if os.path.exists(src):
        if os.path.isfile(src):
            os.remove(src)
        else:
            shutil.rmtree(src)


def mv(src: str, dest: str):
    if cp(src, dest):
        rm(src)


if __name__ == "__main__":
    print(getallfile("/tmp/tmp_root_folder/xxx"))
    # check_file_exists("/tmp/123/321")
