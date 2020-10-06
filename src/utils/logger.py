"""
日志系统
"""
import sys
import time

out_file = "/dev/null"
err_file = "/dev/null"


def out(string: str):
    out_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + string + "\n")
    sys.stdout.write(out_str)
    sys.stderr.write(out_str)
    with open(out_file, 'a') as f:
        f.write(out_str)
    with open(err_file, 'a') as f:
        f.write(out_str)


def err(string: str):
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
    out("hahaha")
