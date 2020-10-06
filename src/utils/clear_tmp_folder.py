"""
用于递归删除文件、文件夹
"""
import os

from src.utils import sub_call_hook, file_helper
from src.CONFIG import PROJ_LIST, TMP_FOLDER, CHECKOUT_FOLDER, TMP_LOG_FOLDER, TMP_TEST_FOLDER


def clear_tmp_all():
    file_helper.rm(TMP_FOLDER)


def clear_tmp_checkout():
    file_helper.rm(CHECKOUT_FOLDER)


def clear_tmp_log():
    file_helper.rm(TMP_LOG_FOLDER)


def clear_tmp_test():
    file_helper.rm(TMP_TEST_FOLDER)
