"""
清空临时文件目录
"""
from src.CONFIG import TMP_ROOT_FOLDER
from src.utils import sub_call_hook, file_helper

if __name__ == "__main__":
    # cmd = ["rm", "-rf", TMP_ROOT_FOLDER]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(TMP_ROOT_FOLDER)
