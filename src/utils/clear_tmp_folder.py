"""
用于递归删除文件、文件夹
"""
import os

from src.utils import sub_call_hook, file_helper
from src.CONFIG import PROJ_LIST


def clear(tmp_fold_addr: str):
    """
    @Deprecated
    :param tmp_fold_addr:
    :return:
    """
    # 清除目标位置的文件
    for project_id in PROJ_LIST:
        # cmd = ["rm", "-rf", tmp_fold_addr + os.sep + project_id]
        # sub_call_hook.serial(" ".join(cmd))
        file_helper.rm(tmp_fold_addr + os.sep + project_id)
    # cmd = ["rm", "-rf", tmp_fold_addr + "/logs"]
    # sub_call_hook.serial(" ".join(cmd))
    file_helper.rm(tmp_fold_addr + "/logs")
