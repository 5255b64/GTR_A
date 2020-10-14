"""
日志系统
"""
import os
import sys
import time

from src.CONFIG import TMP_FOLDER
from utils import file_helper

out_file = "/dev/null"
err_file = "/dev/null"


# continue_file = TMP_FOLDER + os.sep + "continue.log"


def log_out(string: str):
    out_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + string + "\n")
    sys.stdout.write(out_str)
    sys.stderr.write(out_str)
    with open(out_file, 'a') as f:
        f.write(out_str)
    with open(err_file, 'a') as f:
        f.write(out_str)


def log_err(string: str):
    out_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + string + "\n")
    sys.stderr.write(out_str)
    with open(err_file, 'a') as f:
        f.write(out_str)


def set_out(out_f: str):
    global out_file
    out_file = out_f
    # 清空输出文件
    with open(out_file, "w") as f:
        f.truncate()


def set_err(err_f: str):
    global err_file
    err_file = err_f
    # 清空输出文件
    with open(err_file, "w") as f:
        f.truncate()


if __name__ == "__main__":
    set_out("log_out.log")
    log_out("hahaha")


def get_continue_dict(file: str):
    result = dict()
    file_helper.check_file_exists(file, with_blank_file=True)
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            result[line.replace(os.linesep, "")] = 0
            line = f.readline()
    return result


def continue_log(file: str, logger_msg: str):
    with open(file, 'a') as f:
        f.write(logger_msg + os.linesep)
